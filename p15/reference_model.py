"""Synthetic P15 user-stop reference model.

This is an in-memory test model, not a production control plane, identity provider,
credential revoker, queue controller, or deployed emergency-stop service.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


@dataclass
class Task:
    task_id: str
    tenant_id: str
    owner_id: str
    parent_id: Optional[str] = None
    state: str = "running"
    grant_active: bool = True
    queued_work: bool = True
    in_flight_external_effect: bool = False
    external_effect_reversible: bool = True
    integration_revocable: bool = True


class StopController:
    """Deterministic model of user authority, containment and truthful status."""

    def __init__(self, tasks: List[Task], *, available: bool = True,
                 identity_available: bool = True):
        self.tasks: Dict[str, Task] = {task.task_id: task for task in tasks}
        self.available = available
        self.identity_available = identity_available
        self._idempotency: Dict[Tuple[str, str], Tuple[Tuple[str, str, bool], dict]] = {}
        self.audit: List[dict] = []

    def _descendants(self, root_id: str) -> List[Task]:
        found = []
        pending = [root_id]
        while pending:
            current = pending.pop()
            for task in self.tasks.values():
                if task.parent_id == current and task not in found:
                    found.append(task)
                    pending.append(task.task_id)
        return found

    def dispatch_allowed(self, task_id: str) -> bool:
        """Fail closed if control state is unavailable or any ancestor is stopped."""
        if not self.available or not self.identity_available or task_id not in self.tasks:
            return False
        task = self.tasks[task_id]
        seen = set()
        while task is not None:
            if task.task_id in seen or task.state != "running" or not task.grant_active:
                return False
            seen.add(task.task_id)
            task = self.tasks.get(task.parent_id) if task.parent_id else None
        return True

    def stop(self, *, actor_id: str, tenant_id: str, task_id: str,
             idempotency_key: str, account_wide: bool = False) -> dict:
        cache_key = (actor_id, idempotency_key)
        request_signature = (tenant_id, task_id, account_wide)
        cached = self._idempotency.get(cache_key)
        if cached is not None:
            cached_signature, cached_event = cached
            if cached_signature == request_signature:
                return cached_event
            return self._event(
                task_id, tenant_id, actor_id, "task", "received", "denied",
                ["Idempotency key was already used for a different stop request."]
            )

        if not self.available:
            return self._event(task_id, tenant_id, actor_id, "task",
                               "not_verified", "not_verified",
                               ["Control plane unavailable; no containment is asserted."])
        if not self.identity_available:
            return self._event(task_id, tenant_id, actor_id, "task",
                               "received", "denied",
                               ["Identity provider unavailable; request not authorized."])

        target = self.tasks.get(task_id)
        if target is None or target.tenant_id != tenant_id or target.owner_id != actor_id:
            return self._event(task_id, tenant_id, actor_id, "task",
                               "received", "denied",
                               ["Task ownership or tenant scope did not authorize this request."])

        if account_wide:
            roots = [t for t in self.tasks.values()
                     if t.tenant_id == tenant_id and t.owner_id == actor_id]
            by_id = {}
            for root in roots:
                by_id[root.task_id] = root
                for child in self._descendants(root.task_id):
                    if child.tenant_id == tenant_id:
                        by_id[child.task_id] = child
            affected = list(by_id.values())
            scope = "user_authority_graph"
        else:
            # Descendants may run under delegated service identities. Their
            # inclusion follows the verified parent relationship, not equality
            # of their local principal ID with the human actor.
            affected = [t for t in [target] + self._descendants(task_id)
                        if t.tenant_id == tenant_id]
            scope = "task"

        residual = []
        for task in affected:
            task.state = "stopped"
            task.grant_active = False
            task.queued_work = False
            if task.in_flight_external_effect and not task.external_effect_reversible:
                residual.append(f"{task.task_id}: external side effect may be irreversible")
            if not task.integration_revocable:
                residual.append(f"{task.task_id}: integration access requires provider-side action")

        state = "complete_with_limitations" if residual else "work_contained"
        result = "partial" if residual else "effective"
        event = self._event(task_id, tenant_id, actor_id, scope, state, result, residual)
        self._idempotency[cache_key] = (request_signature, event)
        return event

    def _event(self, task_id: str, tenant_id: str, actor_id: str, scope: str,
               enforcement_state: str, result: str, residual: List[str]) -> dict:
        event = {
            "event_id": f"evt-{len(self.audit) + 1:04d}",
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "tenant_id": tenant_id,
            "actor_principal_id": actor_id,
            "task_id": task_id,
            "scope": scope,
            "requested_action": "stop",
            "enforcement_state": enforcement_state,
            "result": result,
            "residual_risks": list(residual),
        }
        self.audit.append(event)
        return event

    def resume(self, task_id: str, *, fresh_authorization: bool) -> bool:
        task = self.tasks.get(task_id)
        if task is None or not self.available or not fresh_authorization:
            return False
        if task.state != "paused":
            return False
        task.state = "running"
        return True

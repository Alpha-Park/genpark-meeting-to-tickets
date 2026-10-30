# -*- coding: utf-8 -*-
"""
GenPark Meeting To Tickets Client
Pure Python Standard Library (Zero External Dependencies)
Implements meeting transcript action item extraction with RACI assignment,
Critical Path Method (CPM) project dependency scheduling, and meeting actionability density auditing.
"""

import math
from typing import Dict, Any, List, Optional

class GenParkMeetingToTickets:
    """
    Automated meeting synthesis, action item extraction, and CPM scheduling engine.
    """

    def __init__(self):
        self.action_cues = ["will", "shall", "action item", "take the lead", "responsible for", "by friday", "need to", "must"]

    def extract_action_items_and_raci(
        self,
        transcript_text: str,
        team_members: List[str]
    ) -> Dict[str, Any]:
        """
        Extracts action items from meeting dialog and assigns RACI matrix classifications.
        """
        lines = [line.strip() for line in transcript_text.splitlines() if line.strip()]
        actions = []
        action_counter = 1

        for line in lines:
            line_lower = line.lower()
            if any(cue in line_lower for cue in self.action_cues):
                # Detect assignee from team_members list
                assigned_to = "Unassigned"
                for member in team_members:
                    if member.lower() in line_lower:
                        assigned_to = member
                        break

                actions.append({
                    "ticket_id": f"TICK-{action_counter:03d}",
                    "raw_statement": line,
                    "raci_roles": {
                        "responsible": assigned_to,
                        "accountable": team_members[0] if team_members else "Lead",
                        "consulted": "Domain Specialist",
                        "informed": "Team Stakeholders"
                    },
                    "estimated_duration_days": 2
                })
                action_counter += 1

        return {
            "total_action_items_detected": len(actions),
            "tickets": actions
        }

    def compute_critical_path_schedule(
        self,
        tickets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates Critical Path Method (CPM) metrics across task dependency DAG:
          - Early Start (ES) and Early Finish (EF) (Forward Pass)
          - Late Start (LS) and Late Finish (LF) (Backward Pass)
          - Total Slack: TS = LS - ES
          - Critical Path: Tasks with TS == 0
        """
        if not tickets:
            return {"project_duration_days": 0, "critical_path": [], "scheduled_tasks": []}

        # Build task map
        tasks = {}
        for t in tickets:
            t_id = t.get("ticket_id", "T1")
            dur = max(1, int(t.get("duration_days", 1)))
            deps = t.get("dependencies", [])
            tasks[t_id] = {
                "ticket_id": t_id,
                "name": t.get("name", t_id),
                "duration": dur,
                "dependencies": deps,
                "successors": [],
                "es": 0,
                "ef": 0,
                "ls": 0,
                "lf": 0,
                "slack": 0
            }

        # Populate successors
        for t_id, task in tasks.items():
            for dep in task["dependencies"]:
                if dep in tasks:
                    tasks[dep]["successors"].append(t_id)

        # Topological forward pass (ES, EF)
        # Compute in-degrees
        in_degree = {t_id: len(tasks[t_id]["dependencies"]) for t_id in tasks}
        queue = [t_id for t_id, deg in in_degree.items() if deg == 0]
        topo_order = []

        while queue:
            curr = queue.pop(0)
            topo_order.append(curr)
            curr_task = tasks[curr]
            curr_task["ef"] = curr_task["es"] + curr_task["duration"]

            for succ in curr_task["successors"]:
                tasks[succ]["es"] = max(tasks[succ]["es"], curr_task["ef"])
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    queue.append(succ)

        project_duration = max([tasks[t_id]["ef"] for t_id in tasks], default=0)

        # Backward pass (LF, LS)
        for t_id in reversed(topo_order):
            curr_task = tasks[t_id]
            if not curr_task["successors"]:
                curr_task["lf"] = project_duration
            else:
                curr_task["lf"] = min(tasks[succ]["ls"] for succ in curr_task["successors"])
            curr_task["ls"] = curr_task["lf"] - curr_task["duration"]
            curr_task["slack"] = curr_task["ls"] - curr_task["es"]

        # Critical path identification
        critical_path = [t_id for t_id in topo_order if tasks[t_id]["slack"] == 0]

        return {
            "total_project_duration_days": project_duration,
            "critical_path_task_count": len(critical_path),
            "critical_path_sequence": critical_path,
            "scheduled_tasks": list(tasks.values())
        }

    def audit_meeting_actionability_density(
        self,
        transcript_text: str,
        action_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Audits meeting productivity density:
          Density = (Action Items / Total Spoken Words) * 1000
        """
        words = transcript_text.split()
        word_count = len(words)
        action_count = len(action_items)

        density = round((action_count / max(1, word_count)) * 1000.0, 2)

        if density >= 8.0:
            rating = "HIGHLY_ACTIONABLE_EFFICIENT"
        elif density >= 3.0:
            rating = "MODERATE_STANDARD_SYNC"
        else:
            rating = "LOW_ROI_CONVERSATIONAL_DRIFT"

        return {
            "total_spoken_words": word_count,
            "total_actions_extracted": action_count,
            "actions_per_1000_words": density,
            "actionability_rating": rating
        }

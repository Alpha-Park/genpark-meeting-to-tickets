# -*- coding: utf-8 -*-
from client import GenParkMeetingToTickets

m2t = GenParkMeetingToTickets()

transcript = """
Alice: I will take the lead on the cryptographic payment vault implementation by Friday.
Bob: Sounds great, I shall deploy the canary node manager to staging.
Charlie: We need to ensure unit test coverage reaches 100% before production rollout.
"""

team = ["Alice", "Bob", "Charlie"]

# 1. Action Item Extraction with RACI
actions = m2t.extract_action_items_and_raci(transcript, team)
print(f"Extracted {actions['total_action_items_detected']} action items:")
for t in actions['tickets']:
    print(f"  [{t['ticket_id']}] Responsible={t['raci_roles']['responsible']} -> {t['raw_statement'][:50]}...")

# 2. Critical Path Method (CPM) Scheduling
tickets = [
    {"ticket_id": "T1", "name": "Design Spec", "duration_days": 3, "dependencies": []},
    {"ticket_id": "T2", "name": "Backend DB", "duration_days": 5, "dependencies": ["T1"]},
    {"ticket_id": "T3", "name": "Frontend UI", "duration_days": 4, "dependencies": ["T1"]},
    {"ticket_id": "T4", "name": "Integration Testing", "duration_days": 3, "dependencies": ["T2", "T3"]}
]
cpm = m2t.compute_critical_path_schedule(tickets)
print()
print(f"CPM Schedule: Total Duration={cpm['total_project_duration_days']} days")
print(f"  Critical Path Sequence: {' -> '.join(cpm['critical_path_sequence'])}")
for task in cpm['scheduled_tasks']:
    print(f"  {task['ticket_id']}: ES={task['es']}, EF={task['ef']}, LS={task['ls']}, LF={task['lf']}, Slack={task['slack']}")

# 3. Actionability Density Audit
audit = m2t.audit_meeting_actionability_density(transcript, actions['tickets'])
print()
print(f"Meeting ROI: {audit['actions_per_1000_words']} actions/1000 words ({audit['actionability_rating']})")

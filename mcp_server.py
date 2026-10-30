# -*- coding: utf-8 -*-
"""
GenPark Meeting To Tickets MCP Server
FastMCP standard interface for action item RACI extraction, CPM scheduling, and meeting actionability auditing.
"""

import json
from typing import Dict, Any, List
from client import GenParkMeetingToTickets

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("genpark-meeting-to-tickets")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("genpark-meeting-to-tickets")

m2t = GenParkMeetingToTickets()

@mcp.tool()
def extract_action_items_and_raci(
    transcript_text: str,
    team_members: List[str]
) -> str:
    """
    Extracts action items from meeting dialog and assigns RACI matrix classifications.
    """
    res = m2t.extract_action_items_and_raci(transcript_text, team_members)
    return json.dumps(res, indent=2)

@mcp.tool()
def compute_critical_path_schedule(
    tickets: List[Dict[str, Any]]
) -> str:
    """
    Calculates Critical Path Method (CPM) metrics across task dependency DAG.
    """
    res = m2t.compute_critical_path_schedule(tickets)
    return json.dumps(res, indent=2)

@mcp.tool()
def audit_meeting_actionability_density(
    transcript_text: str,
    action_items: List[Dict[str, Any]]
) -> str:
    """
    Audits meeting productivity and action item density per 1000 words.
    """
    res = m2t.audit_meeting_actionability_density(transcript_text, action_items)
    return json.dumps(res, indent=2)

def main():
    print("Testing Meeting To Tickets:")
    sample = "Alice will take the lead on database schema migration by Friday."
    print(extract_action_items_and_raci(sample, ["Alice", "Bob"]))

if __name__ == "__main__":
    main()

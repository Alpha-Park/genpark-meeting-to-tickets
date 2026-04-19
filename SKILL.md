---
name: genpark-meeting-to-tickets
description: Automatically processes meeting transcripts and generates structured JSON Product Requirement Documents (PRD) and Jira/Linear tickets.
---

# GenPark Meeting to Tickets

Replicates enterprise B2B meeting bots. You feed it a messy Zoom/Lark transcript, and it outputs a clean Product Requirements Document and a batch of ready-to-import Jira or Linear tickets.

## Usage
`openclaw use genpark-meeting-to-tickets --transcript "zoom_sync.txt"`

The agent extracts the context, ignores the small talk, defines the features discussed, and formats JSON outputs matching standard issue-tracking APIs.

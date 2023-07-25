---
title: Team AI
emoji: 🐝 Foraging 🐝
colorFrom: indigo
colorTo: pink
sdk: gradio
sdk_version: 3.34.0
app_file: app.py
pinned: false
duplicated_from: bboeckeler/team-ai-copy-jul-13
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## Where is what?
- `./documents` contains the business and architecture context markdown files
- `./acceptances` and `./tasking` are the two use cases, one for story refinement, one for developer tasks

## Run it locally
Create `.env` file with value for `OPENAI_API_KEY`

`pip install -r requirements.txt`
`python app.py`

## Sample user story
Copy & paste into "User story" field for "Acceptances & Examples"
```
User story: Awareness Layer

Requirement: Display other users’ awareness info(cursor, name and online information) on the whiteboard.

Acceptance Criterion 1: Don’t display local user
Acceptance Criterion 2: When remote user changes cursor location, display the change in animation.
```
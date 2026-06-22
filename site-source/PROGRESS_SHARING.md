# Progress Sharing and Submission Setup

This page explains how students should share progress with the mentor.

Use this page before starting Checkpoint 00.

## Goal

Keep all checkpoint evidence in one organized place so the mentor can review progress without searching through WhatsApp messages, loose screenshots, or random files.

## What to use

Use three places only:

| Place | Purpose |
|---|---|
| Course website | Read instructions only |
| Google Drive folder | Journal, screenshots, diagrams, submissions, mentor comments |
| GitHub repository | Code, commits, project files, README |

Do not submit checkpoint evidence only through WhatsApp.

WhatsApp can be used only to notify the mentor that a checkpoint is submitted.

## Step 1 — Create the main Google Drive folder

Each student must create one main folder in Google Drive.

Folder name format:

```text
StudentName - Engineering Systems Foundation
```

Example:

```text
Anu - Engineering Systems Foundation
```

## Step 2 — Create these folders inside it

Create this exact folder structure:

```text
StudentName - Engineering Systems Foundation/
  00 - Progress Tracker/
  01 - Project Journal/
  02 - Checkpoint Submissions/
  03 - Screenshots and Logs/
  04 - Diagrams/
  05 - Final Demo/
```

Download/copy folder structure template:

- [Google Drive folder structure template](templates/google-drive-folder-template.txt)

## Step 3 — Create checkpoint folders

Inside `02 - Checkpoint Submissions`, create one folder per checkpoint:

```text
02 - Checkpoint Submissions/
  CP00 - Orientation/
  CP01 - System Selection/
  CP02 - Local Computer Files/
  CP03 - Localhost Networking/
  CP04 - Git Version Control/
  CP05 - Signal Simulator Validation/
  CP06 - API HTTP JSON Backend/
  CP07 - Database Persistence/
  CP08 - Dashboard HMI/
  CP09 - Cloud Deployment Logs Env/
  CP10 - Final Demo Hardware Extension/
```

Only work on the checkpoint that is currently unlocked.

## Step 4 — Create the progress tracker sheet

Inside `00 - Progress Tracker`, create a Google Sheet named:

```text
Progress Tracker
```

Columns:

```text
Checkpoint | Status | Submitted date | Mentor comment | Approved? | Next unlocked?
```

Allowed status values:

```text
Not started
In progress
Submitted
Needs rework
Approved
```

Download/copy tracker template:

- [Progress tracker CSV template](templates/progress-tracker-template.csv)

How to use it:

1. Download the CSV file.
2. Upload it to Google Drive.
3. Open with Google Sheets.
4. Rename it to `Progress Tracker`.
5. Keep updating it after every checkpoint.

## Step 5 — Create the project journal

Inside `01 - Project Journal`, create one Google Doc named:

```text
Project Journal
```

Use this document for daily notes, mistakes, searches, and learnings.

Download/copy journal template:

- [Project journal template](templates/project-journal-template.txt)

The journal is not a polished report. It is a learning record.

Write short notes every day:

```text
Date:
What I tried:
What worked:
What failed:
Search terms used:
What I understood:
Next step:
```

## Step 6 — Create a checkpoint submission document

For every checkpoint folder, create one Google Doc named:

```text
CPXX - Submission
```

Example:

```text
CP01 - Submission
```

Use the same template for every checkpoint.

Download/copy submission template:

- [Checkpoint submission Google Doc template](templates/checkpoint-submission-google-doc-template.txt)
- [Checkpoint submission Markdown template](templates/checkpoint-submission-template.html)

## Step 7 — What goes inside each checkpoint folder

Every checkpoint folder should contain:

```text
CPXX - Submission
screenshots/
logs/
diagrams/
links.txt
```

If there is code, also include the GitHub repository link and commit link inside the submission document.

## Step 8 — Sharing permission

Share the main Google Drive folder with the mentor.

Recommended permission:

```text
Mentor: Commenter
Student: Editor
```

Use `Editor` for the mentor only if the mentor needs to directly edit or add notes inside documents.

Do not make the folder public unless the mentor asks for it.

## Step 9 — Student submission process

For every checkpoint, follow this process:

1. Complete the checkpoint instruction.
2. Add screenshots, logs, diagrams, and links to the checkpoint folder.
3. Fill `CPXX - Submission`.
4. Add GitHub repo link or commit link if code was involved.
5. Update `Progress Tracker` status to `Submitted`.
6. Send one message to mentor:

```text
CPXX submitted.
Drive folder: <link>
GitHub repo/commit: <link if applicable>
```

7. Stop and wait for mentor review.
8. If approved, continue after the next checkpoint is unlocked.
9. If marked `Needs rework`, fix the submission and resubmit.

## Mentor review rule

A checkpoint is approved only if the student can explain the work live without reading copied text.

The mentor checks:

- Did the student follow the instruction?
- Is the example copied or only used for understanding?
- Is there evidence?
- Are screenshots/logs included?
- Is the search trail included?
- Can the student explain mistakes and fixes?
- Is the GitHub repo updated when code is involved?

## Simple rule for students

Do not ask: `Where should I send this?`

Send everything through the shared Google Drive folder.

Then notify the mentor with the Drive link.
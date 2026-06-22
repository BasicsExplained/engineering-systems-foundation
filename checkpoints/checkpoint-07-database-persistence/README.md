# Checkpoint 07 — Database and Persistence

## Goal

Understand why databases exist and what persistence means.

## Instruction

Do these tasks in order:

1. Store readings in memory first.
2. Restart the backend and observe what data is lost.
3. Store readings in a local database.
4. Restart again and show that stored data remains.
5. Run at least one query to read saved data.
6. Explain memory versus database storage.
7. Explain why timestamps are useful.
8. Record one database error or confusion and how you searched for it.

## Example

Example only. Do not copy blindly.

```text
Memory storage:
Data disappears when the server restarts.

Database storage:
Data remains after the server restarts.
```

Example table idea:

```text
id | timestamp | signal_name | value | status
```

## Submit

Send these items to the mentor:

1. Proof that memory data disappeared after restart.
2. Proof that database data stayed after restart.
3. Screenshot or output showing saved database records.
4. One query result.
5. Explanation of memory, database, table, row, and timestamp.
6. Search trail for one database issue.

## Done when

This checkpoint is complete when:

- you have shown the difference between memory and persistent storage
- readings are stored in a database
- you can query saved readings
- you can explain what survives a restart and why

## Mentor review

The mentor may ask:

- What happened after restart?
- What is a table?
- What is a row?
- Why is timestamp useful?
- Why should readings be stored permanently?

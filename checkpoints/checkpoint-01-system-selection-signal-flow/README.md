# Checkpoint 01 — System Selection and Signal Flow

## Goal

Choose one simple real-world-inspired system and explain how data moves through it.

You are not coding in this checkpoint. You are only selecting and explaining your system.

## Instruction

Do these tasks in order:

1. Choose one system that produces measurable data.
2. Give the system a short name.
3. Write why you selected it.
4. Identify at least three measurable signals.
5. Draw a simple flow diagram from real-world signal to cloud dashboard.
6. Identify three possible failures.
7. Explain how a user would notice each failure.
8. Explain how an engineer may start debugging each failure.
9. Record your search trail.

## Example

Example only. Do not copy this as your final answer.

System name:

```text
Room Comfort Monitor
```

Possible signals:

```text
temperature
humidity
room occupancy status
```

Simple flow:

```text
room air → sensor reading → data value → local program → API → database → dashboard → user decision
```

Possible failure:

```text
Temperature value is stuck at 0.
User notices the dashboard is unrealistic.
Engineer checks sensor reading, simulator output, API request, database value, and dashboard display.
```

## Submit

Send one short document with these headings:

1. System name
2. Why I selected this system
3. Three measurable signals
4. Signal-to-cloud flow diagram
5. Three possible failures
6. How the user notices each failure
7. How an engineer starts debugging each failure
8. Search trail

## Search trail format

Write the actual searches you used, for example:

```text
what is a sensor signal
engineering system block diagram
how to identify failure modes in engineering system
input processing output engineering system
```

## Done when

This checkpoint is complete when:

- your system is simple and measurable
- your diagram shows a clear data path
- you have at least three signals
- you can explain failures without reading copied text
- your search trail is included

## Mentor review

The mentor may ask:

- What is the real-world input in your system?
- Which values are measured?
- Which values are calculated?
- What can fail?
- How would this later connect to hardware?

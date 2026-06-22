# Checkpoint 10 — Final Demo and Hardware Extension

## Goal

Demonstrate the full Signal-to-Cloud system and explain how it can later connect to real hardware.

## Instruction

Do these tasks in order:

1. Prepare a final demo of your project.
2. Explain your project idea and signal choices.
3. Show your architecture diagram.
4. Show the simulator.
5. Show validation behavior.
6. Show the API/backend.
7. Show database or persistence behavior.
8. Show dashboard or control panel.
9. Show deployment and logs if completed.
10. Explain how real hardware could replace the simulator later.
11. Explain at least three failure modes.
12. Prepare for mentor viva questions.

## Example

Example hardware extension flow:

```text
sensor -> microcontroller or computer -> communication -> API/backend -> database -> dashboard/control panel
```

Example explanation:

```text
The simulator currently produces temperature values.
Later, a real temperature sensor could send values through a microcontroller.
The backend should not trust the value until validation is applied.
```

## Submit

Send these items to the mentor:

1. Final demo link or screen recording.
2. Architecture diagram.
3. Project journal.
4. Debugging evidence from the course.
5. Explanation of simulator, API, database, dashboard, and deployment.
6. Future hardware extension plan.
7. Three failure modes and debugging approach.

## Done when

This checkpoint is complete when:

- the full project can be demonstrated end-to-end
- you can explain every major part without copied text
- your evidence shows learning across the month
- your hardware extension plan is realistic
- you can answer mentor viva questions

## Mentor review

The mentor may ask:

- What is localhost?
- What is a port?
- What is Git?
- What is an API?
- What is JSON?
- What is a database?
- What happens if the server restarts?
- How would real hardware send data to your system?
- What are three ways your system can fail?

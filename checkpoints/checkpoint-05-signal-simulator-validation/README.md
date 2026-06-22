# Checkpoint 05 — Signal Simulator and Validation

## Goal

Create simulated signal data and classify values as normal, warning, critical, or invalid.

## Instruction

Do these tasks in order:

1. Choose at least three signals for your system.
2. Define normal, warning, and critical ranges for each signal.
3. Generate changing simulated values.
4. Generate one invalid or impossible value sometimes.
5. Ignore impossible values instead of storing them as trusted readings.
6. Mark risky values as warning or critical.
7. Log what happened for each reading.
8. Explain why validation is needed before trusting data.

## Example

Example only. Do not copy directly.

```text
Signal: temperature
Normal: 20 to 35
Warning: 36 to 45
Critical: above 45
Invalid: below -20 or above 100
```

Example simulator output:

```text
28.5 -> normal
41.0 -> warning
55.2 -> critical
150.0 -> invalid, not trusted
```

## Submit

Send these items to the mentor:

1. Your signal definitions and range justification.
2. Sample simulator output.
3. Log showing invalid data handled correctly.
4. Explanation of normal, warning, critical, and invalid.
5. Search trail for validation or sensor range decisions.

## Done when

This checkpoint is complete when:

- at least three signals are simulated
- every signal has clear ranges
- invalid values are handled separately
- warning and critical values are identified
- you can explain why validation matters

## Mentor review

The mentor may ask:

- Why did you choose these ranges?
- What is invalid data?
- What should be ignored versus only marked as warning?
- How can bad data affect a system?
- What happens if validation is skipped?

# Checkpoint 09 — Cloud Deployment, Logs, and Environment Variables

## Goal

Understand cloud as infrastructure and learn how to inspect a deployed system.

## Instruction

Do these tasks in order:

1. Deploy at least one part of your system to a cloud or hosting platform.
2. Open the deployed system through a public URL.
3. Find the deployment logs.
4. Add or inspect one environment/config variable.
5. Intentionally create one configuration problem.
6. Fix the problem.
7. Explain the difference between localhost and the deployed service.
8. Record what could cost money in the platform you used.

## Example

Example only. Your platform may be different.

```text
Local:
http://localhost:3000

Cloud:
https://your-project.example-host.com
```

Example configuration idea:

```text
PORT=3000
API_BASE_URL=https://example.com
APP_ENV=production
```

## Submit

Send these items to the mentor:

1. Public URL.
2. Deployment screenshot.
3. Logs screenshot.
4. One environment/config variable example.
5. One deployment problem and root cause.
6. Comparison: local laptop versus cloud service.
7. Search trail for one deployment issue.

## Done when

This checkpoint is complete when:

- at least one part of the system is deployed
- you can open it through a public URL
- you know where to find logs
- you can explain one config variable
- you can explain how cloud differs from localhost

## Mentor review

The mentor may ask:

- Where is your code running now?
- What is a public URL?
- What are logs?
- What can cost money in cloud?
- What is different from localhost?

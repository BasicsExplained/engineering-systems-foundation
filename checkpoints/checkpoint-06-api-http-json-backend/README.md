# Checkpoint 06 — API, HTTP, JSON, Backend

## Goal

Understand how programs communicate using HTTP APIs and JSON.

## Instruction

Do these tasks in order:

1. Create a simple backend for your system.
2. Add a health endpoint.
3. Add an endpoint to receive one reading.
4. Add an endpoint to show the latest reading.
5. Add an endpoint to show reading history.
6. Send simulator readings to the backend.
7. Send one bad request and explain the response.
8. Explain request, response, endpoint, method, and JSON.

## Example

Example endpoint list:

```text
GET /health
POST /reading
GET /latest
GET /history
```

Example JSON reading:

```json
{
  "temperature": 28.5,
  "humidity": 61,
  "status": "normal"
}
```

## Submit

Send these items to the mentor:

1. Screenshot of backend running.
2. Successful API request and response.
3. Failed API request and explanation.
4. Explanation of GET, POST, endpoint, request, response, and JSON.
5. Search trail for one backend/API issue.

## Done when

This checkpoint is complete when:

- the backend runs locally
- at least one reading can be sent to it
- latest and history data can be requested
- you can explain what the backend is responsible for

## Mentor review

The mentor may ask:

- Why is POST used for sending a reading?
- What is JSON?
- What happens when invalid data is sent?
- What is the backend responsible for?
- What is the difference between client and server?

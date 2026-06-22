# Checkpoint 03 — Localhost, Networking, and Ports

## Goal

Understand how a local program becomes reachable through an address and a port.

## Instruction

Do these tasks in order:

1. Run a small local server.
2. Open it using `localhost` from your laptop browser.
3. Open it using `127.0.0.1` from your laptop browser.
4. Find your laptop's LAN IP address.
5. Try opening the server from a phone on the same Wi-Fi.
6. Intentionally create one port conflict.
7. Write what failed and why.
8. Record your search trail.

## Example

Example only. Do not copy blindly.

```text
Laptop browser:
http://localhost:3000
http://127.0.0.1:3000

Phone browser on same Wi-Fi:
http://192.168.1.20:3000
```

If the phone cannot open it, possible causes include firewall, wrong IP, wrong port, server bound only to localhost, or different Wi-Fi network.

## Submit

Send these items to the mentor:

1. Screenshot from laptop browser.
2. Screenshot from phone browser, or explanation if blocked.
3. The LAN IP address you used.
4. Screenshot or log of a port conflict.
5. Explanation of `localhost`, `127.0.0.1`, LAN IP, and port.
6. Search trail.

## Done when

This checkpoint is complete when:

- your local server runs
- you can explain localhost versus LAN IP
- you can explain what a port is
- you intentionally created and understood one network/port problem

## Mentor review

The mentor may ask:

- Why does localhost on your phone not mean your laptop?
- What is a port?
- What does connection refused mean?
- What can block network access?
- Why does the same app work locally but fail from another device?

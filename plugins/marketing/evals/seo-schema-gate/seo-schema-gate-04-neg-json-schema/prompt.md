---
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash]
runs: 3
---

Write a JSON Schema (draft 2020-12) that validates an order payload with an id (uuid string), a list of line items
(sku string, qty integer at least 1) and a currency (ISO 4217 code).

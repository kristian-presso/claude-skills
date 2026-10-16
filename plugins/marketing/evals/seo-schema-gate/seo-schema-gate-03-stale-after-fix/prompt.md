---
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash]
runs: 3
---

Our pricing page's JSON-LD had a trailing comma so it wasn't parsing. We fixed it and redeployed 10 minutes ago.
I checked https://oakfield-venues.example/pricing?nocache=8812 and it STILL shows the old broken JSON, so the fix
didn't work? Also we set Content-Type in our route handler for /feed.xml but it comes back as text/plain. It's a
static (prerendered) Astro build.

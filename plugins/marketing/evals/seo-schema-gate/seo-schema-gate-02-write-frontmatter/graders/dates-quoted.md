---
type: llm
---

Pass only if every date value in the YAML frontmatter produced is quoted (for example published_at: "2026-10-20"),
OR the answer explicitly warns that bare YAML dates must be quoted. Fail if dates are left unquoted with no warning.

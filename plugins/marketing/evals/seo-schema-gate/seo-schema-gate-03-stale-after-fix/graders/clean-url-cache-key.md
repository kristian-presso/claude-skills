---
type: llm
---

Pass only if the answer explains that a cache-busting query string is a different cache key that can return a stale
copy, so the fix should be re-checked on the clean URL (and the CDN purged or given time), rather than concluding the
fix failed. Fail if this is not explained.

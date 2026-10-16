---
type: llm
---

Pass only if the answer flags ALL of: DKIM is missing (no key published); there is no working unsubscribe (it must be in
every message, with one-click List-Unsubscribe headers for bulk); and the DMARC rua address is fine but alignment cannot
pass without DKIM, or SPF plus DKIM both needed for Outlook/Hotmail recipients. Pass if at least DKIM missing AND unsubscribe
off AND the Microsoft/Outlook need for both SPF and DKIM are all mentioned. Fail otherwise.

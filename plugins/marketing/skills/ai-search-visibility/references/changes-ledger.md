# Changes ledger

The method in this skill is stable. The facts below drift faster. Each has a date it was
last checked and where to verify it. Check before stating any of them as current.

| Fact | Last checked | Verify at | Why it drifts |
| --- | --- | --- | --- |
| The AI crawler agent list in `technical-discoverability.md` and the bundled script | October 2026 | Each vendor's crawler documentation (OpenAI, Anthropic, Perplexity, Google, Microsoft, Apple, Common Crawl) | Vendors add, rename and retire agents. A stale name fails silently. |
| `ChatGPTBot` is not a real agent | October 2026 | OpenAI's bots documentation | If OpenAI ever ships an agent with that name, the advice flips. |
| `Google-Extended` controls Gemini use and does not affect Google Search or AI Overviews | October 2026 | Google Search Central, "Google's common crawlers" | Google has restructured AI controls before. |
| Some user-triggered agents do not reliably honour robots.txt | October 2026 | Each vendor's crawler documentation | Policy, not standard. |
| Bing Webmaster Tools AI Performance report is in public preview (launched February 2026) | October 2026 | bing.com/webmasters | Preview features change or graduate. |
| Search Console does not break out AI Overview traffic separately | October 2026 | search.google.com/search-console | Google may add a dedicated report. |
| Which queries trigger AI Overviews, and how sources are chosen | October 2026 | developers.google.com/search/docs/appearance/ai-features | Unpublished and changes continuously. |
| Whether a given assistant searches the web by default | October 2026 | Each product's release notes | Changes per product, tier and release. |
| FAQ and HowTo rich results were restricted in 2023 | October 2026 | Google Search Central, structured data gallery | Rich result eligibility changes. |
| `llms.txt` is a proposal, not a standard all engines read | October 2026 | llmstxt.org | Adoption may change. |
| Most social apps strip the referrer on in-app link clicks | October 2026 | Test with your own analytics | Platform behaviour, not a standard. |

When acting on any specific claim about how an engine selects or shows citations, check
the primary source first.

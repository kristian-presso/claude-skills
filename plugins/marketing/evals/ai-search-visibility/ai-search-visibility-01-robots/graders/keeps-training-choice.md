---
type: llm
---

Pass only if the answer keeps GPTBot (training) blocked or explicitly leaves it as the user's choice, while
recommending allowing search or user-fetch agents (such as OAI-SearchBot, ChatGPT-User, Claude-SearchBot, PerplexityBot).
Fail if it tells the user to allow GPTBot, or blocks everything, or does not separate training from search crawlers.

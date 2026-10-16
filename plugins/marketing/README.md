# marketing

Content and search skills for a small team that cannot afford a content department or a
paid SEO suite.

The angle is being **found and cited**, not only ranked. More of your buyers now ask an
assistant or an answer engine before they ever see a page of blue links. These skills
treat that as the main surface: crawlable first, then answer-shaped, then worth quoting.

Everything runs on a free stack. If you have an SEO tool or a search API connected, the
skills use it. If you do not, they tell you what they could not see rather than guessing.

## Skills

| Skill | Use it when |
| --- | --- |
| **ai-search-visibility** | You want to know why AI assistants and answer engines are not citing your site, or you want a page rewritten so they can quote it. |
| **keyword-research** | You need to decide what to write about next and want a clustered keyword map with intent and gaps, without paying for an SEO tool. |
| **content-atomisation** | You have one long piece and want a sequenced plan, and drafts, for turning it into posts, emails and clips that each stand alone. |
| **linkedin-post** | You want a LinkedIn post that sounds like you, learned from your own past posts rather than a generic template. |
| **seo-schema-gate** | A page is about to go live, or just went live, and you want its meta tags and JSON-LD checked rather than assumed. |

## How they fit together

```text
keyword-research  ->  what to write, and which page owns each topic
       |
   (you write the long piece)
       |
seo-schema-gate   ->  meta and structured data correct before and after publish
ai-search-visibility -> crawlable, answer-shaped, citation-worthy
       |
content-atomisation -> one piece becomes a sequenced set of derivatives
linkedin-post        -> drafts the LinkedIn ones in your voice
```

Each skill also works on its own.

## Install

In Claude Code:

```bash
/plugin marketplace add kristian-presso/claude-skills
/plugin install marketing@claude-skills
```

On claude.ai, upload any single skill folder from `skills/` as a custom skill.

## Feedback

Used one of these? [Tell me what worked and what broke](https://tally.so/r/7XlJbL?source=marketing) - two minutes, every answer read.

## Licence

MIT.

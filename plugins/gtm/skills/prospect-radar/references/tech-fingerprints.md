# Tech fingerprints

Fetch the raw HTML with `curl -sL -A "Mozilla/5.0" <url>` (a web reader that converts to
text strips scripts). Search the HTML for these strings. Record the tool, the matching
string, the URL checked and the date.

## Product and web analytics

| Tool | Look for |
| --- | --- |
| Amplitude | `cdn.amplitude.com`, `api2.amplitude.com` |
| Mixpanel | `cdn.mxpnl.com`, `api-js.mixpanel.com` |
| Heap | `cdn.heapanalytics.com`, `heap-api.com` |
| PostHog | `posthog.com/static`, `i.posthog.com` |
| Google Analytics 4 | `googletagmanager.com/gtag/js`, `google-analytics.com` |
| Google Tag Manager | `googletagmanager.com/gtm.js` |
| Adobe Analytics or Launch | `assets.adobedtm.com`, `omtrdc.net`, `AppMeasurement` |

## Session replay and heatmaps

| Tool | Look for |
| --- | --- |
| FullStory | `fullstory.com/s/fs.js`, `edge.fullstory.com` |
| Hotjar | `static.hotjar.com` |
| Contentsquare | `contentsquare.net` |
| Microsoft Clarity | `clarity.ms` |
| LogRocket | `cdn.logrocket.io`, `lr-ingest.io` |
| Quantum Metric | `quantummetric.com` |

## Experimentation and feature flags

| Tool | Look for |
| --- | --- |
| Optimizely | `cdn.optimizely.com` |
| VWO | `visualwebsiteoptimizer.com` |
| LaunchDarkly | `launchdarkly.com` |
| Statsig | `statsig.com` |

## In-app guides and surveys

| Tool | Look for |
| --- | --- |
| Pendo | `cdn.pendo.io`, `pendo-io-static` |
| Appcues | `fast.appcues.com` |
| WalkMe | `cdn.walkme.com` |
| Userpilot | `js.userpilot.io` |
| Qualtrics site intercept | `siteintercept.qualtrics.com` |

## Customer data platforms

| Tool | Look for |
| --- | --- |
| Segment | `cdn.segment.com` |
| RudderStack | `cdn.rudderlabs.com` |
| Tealium | `tags.tiqcdn.com` |

## Other evidence

- Job posts naming a tool ("experience with Pendo", "Adobe Analytics required") are
  strong evidence of what a team uses today.
- Vendor case studies and logo walls are public evidence of a customer relationship.
- These strings change. If a check never matches across many sites, the string is
  probably stale; note it in `log.md` so the list can be updated.

# Deliverability

## Contents

- Authentication (firm)
- Bulk-sender rules (Google and Yahoo since February 2024, Microsoft since May 2025)
- Domain and volume hygiene (practitioner consensus)
- Diagnosing a sudden drop

As of 16/10/2026. The authentication requirements and bulk-sender rules come from
mailbox-provider documentation and are firm. The volume and warm-up numbers are
practitioners' rules of thumb with no published study behind them, and are labelled so.

Verify before relying on any threshold:

- Google email sender guidelines: support.google.com/a/answer/81126, and the FAQ at
  support.google.com/a/answer/14229414 (checked 16/10/2026)
- Yahoo sender best practices: senders.yahooinc.com/best-practices
- Microsoft, "Strengthening Email Ecosystem: Outlook's New Requirements for High-Volume
  Senders", Microsoft Defender for Office 365 blog on techcommunity.microsoft.com,
  published 02/04/2025, last updated 30/04/2025 (checked 16/10/2026)

## Authentication (firm)

- **SPF and DKIM** on the sending domain. Bulk senders need both; every sender needs at
  least one. DKIM keys must be at least 1024-bit; 2048-bit is recommended.
- **DMARC** with at least `p=none` is required for bulk senders. `p=none` only monitors.
  Providers increasingly expect movement towards `quarantine` or `reject`, so treat
  `p=none` as a starting point.
- **Alignment.** The domain in the visible `From:` header must match the domain that
  passes SPF or the domain that signs DKIM.
- **Infrastructure.** Valid forward and reverse DNS on sending IPs, and TLS in transit.
  Hosted mail platforms handle this for you; self-hosted senders must check it.

Do not confuse email records with the `_acme-challenge` TXT record used for TLS
certificates. It is unrelated to mail authentication.

### Checking it

If the user has a terminal, these show what is published:

```bash
dig +short TXT example-sending-domain.com            # SPF lives here (v=spf1 ...)
dig +short TXT _dmarc.example-sending-domain.com     # DMARC policy
dig +short TXT selector._domainkey.example-sending-domain.com   # DKIM; selector comes from the mail provider
```

Otherwise, send a test message to a personal mailbox and read the authentication results
in the message headers (look for `spf=pass`, `dkim=pass`, `dmarc=pass`).

## Bulk-sender rules (Google and Yahoo since February 2024, Microsoft since May 2025)

- A bulk sender is roughly anyone sending **5,000 or more messages a day** to that
  provider's users. Google's FAQ says the status is permanent once assigned, and that
  from November 2025 non-compliant mail faces temporary and permanent rejections.
- **One-click unsubscribe** (RFC 8058) for marketing mail: a `List-Unsubscribe` header
  pointing at an unsubscribe URL, plus
  `List-Unsubscribe-Post: List-Unsubscribe=One-Click`. Honour requests within about two
  days.
- **Spam complaints:** keep below **0.10%**. At **0.30%** or above, filtering or blocking
  starts. That is about 3 complaints per 1,000 messages. Monitor in the provider's
  postmaster tools.

### Microsoft Outlook.com, Hotmail and Live

From Microsoft's own announcement (published 02/04/2025, updated 30/04/2025; no later
change found on 16/10/2026). It covers Microsoft's consumer service (outlook.com,
hotmail.com, live.com), not business mailboxes on Microsoft 365.

- **Who:** domains sending **more than 5,000 messages a day** to those addresses.
- **Required:** SPF must pass for the sending domain; DKIM must pass; DMARC at least
  `p=none`, aligned with SPF or DKIM (preferably both).
- **Enforcement:** from **05/05/2025** non-compliant mail is **rejected**, not sent to
  Junk, with `550 5.7.515 Access denied, sending domain [SendingDomain] does not meet the
  required authentication level`. The original announcement said Junk first; the 29/04/2025
  update changed it to rejection.
- **Recommended, not yet required:** a valid sender address in the visible From, a
  functional unsubscribe link, regular list hygiene and bounce removal, and transparent
  mailing practices. Microsoft publishes no complaint-rate threshold. Adding yourself to a
  recipient's safe senders list does not bypass enforcement.

Most small cold programmes are nowhere near 5,000 a day, but the same rules are a good
standard to hold to at any volume: they describe what providers reward.

## Domain and volume hygiene (practitioner consensus)

- **Separate sending domain.** Send cold email from a look-alike of the brand domain (for
  example `get-example.com` or `example-team.com`), never the main domain. A reputation
  hit then stays away from invoices, support and normal mail. Point the look-alike's
  website at the main site so it does not look abandoned.
- **Warm-up.** Ramp new domains and inboxes over about 4 to 6 weeks, starting at 5 to 10
  sends a day. This is a rule of thumb. Inbox-placement percentages quoted for warm-up
  (with versus without) come from vendors that sell warm-up or inboxes, with no published
  method, so do not quote them as fact.
- **Per-inbox volume.** About 10 to 20 cold sends per inbox per day is a commonly used
  cautious cap, not a provider limit. No mailbox provider publishes a per-inbox cold
  limit. Warm-up traffic counts towards the cap.
- **Scale sideways.** About 3 to 5 inboxes per domain (rule of thumb), across several domains. Reaching
  1,000 sends a day means many inboxes over several domains, not one inbox pushed hard.
- **List hygiene.** Verify addresses before sending. Remove bounces and long-term
  non-engagers promptly. Bounces and complaints damage reputation fastest.

## Diagnosing a sudden drop

Work down this list in order:

1. **Authentication broke.** Someone edited DNS, changed mail provider, or a DKIM key
   rotated. Re-run the checks above.
2. **Complaint rate rose.** Check postmaster tools. Usually a list or targeting problem,
   not a copy problem.
3. **Bounce rate rose.** An unverified list was imported. Pause, verify, resume.
4. **Volume jumped.** A new campaign doubled an inbox's daily sends overnight. Bring it
   back under the cap.
5. **Content triggers.** Link shorteners, many links, attachments or images in a first
   touch. Strip back to plain text with at most one link.

If reputation is badly damaged, stop cold sending from that domain, keep only warm-up
traffic for two to four weeks, and bring a fresh, warmed domain into rotation meanwhile.

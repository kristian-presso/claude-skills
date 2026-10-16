# The law on unsolicited B2B contact

**Reference, not legal advice.** This is a neutral summary of how the main regimes treat
unsolicited B2B email, as of June 2026 (UK entry re-checked 16/10/2026). Rules and penalty amounts change. Get qualified
advice before running a real programme, and verify current positions at the official
sources named below.

The rule that matters most: **the recipient's location governs**, not the sender's.

## The four main regimes

- **CAN-SPAM (United States).** An opt-out model. Cold email is permitted, but it needs
  honest From, Reply-To and routing information, a working unsubscribe honoured promptly,
  and a physical postal address. Penalties are per message and high (about $53,088 per
  email from January 2025, adjusted for inflation periodically). Verify at the Federal
  Trade Commission (ftc.gov).
- **GDPR (European Union).** Processing personal data needs a lawful basis. For B2B cold
  email that is usually **legitimate interest**, which needs a written balancing
  assessment and is harder to justify if the address was not made public for
  professional contact. Fines up to EUR 20m or 4% of global turnover. Individual EU
  countries also have their own e-privacy rules on electronic marketing, some stricter
  than others. Verify with the relevant national data-protection authority.
- **PECR alongside UK GDPR (United Kingdom).** More permissive for B2B than for
  consumers: messages to corporate subscribers are allowed if they identify the sender
  and offer a clear opt-out. Sole traders and some partnerships count as individuals and
  get consumer-level protection. As of 16/10/2026 the Data (Use and Access) Act 2025
  changes to PECR are in force: Schedule 13, which raises the PECR maximum fine from
  £500,000 to the UK GDPR higher maximum (£17.5m or 4% of worldwide annual turnover,
  whichever is higher), commenced on 05/02/2026 (S.I. 2026/82, per legislation.gov.uk).
  The B2B rule above did not change. Some older ICO pages still quote £500,000. Full
  detail and sources are in the uk-business plugin's uk-company-guide skill
  (`references/data-protection-and-marketing.md`). Verify at the Information
  Commissioner's Office (ico.org.uk) and legislation.gov.uk/ukpga/2025/18/schedule/13.
- **CASL (Canada).** An opt-in model and the strictest of the four. Needs express or
  implied consent **before** the first message (implied includes an existing business
  relationship within a defined window, and some cases of a conspicuously published
  address with no "no unsolicited messages" statement). Penalties up to C$10m per
  violation for organisations. Verify at the CRTC (crtc.gc.ca).

## Lists that span countries

Emailing into the EU from elsewhere still brings GDPR into play for how you handle the
data. Build for the strictest regime the list touches, or split the list by country and
run each segment under its own rules.

## Common-denominator practice

These satisfy most regimes at once and also help delivery:

- Accurate sender identity: no misleading From, Reply-To or domain.
- A genuine, easy opt-out, honoured fast, and kept on a suppression list so the person
  is never re-added.
- A record of where each contact's details came from and when.
- Role-relevant B2B targeting, using business contact details published for professional
  use, never scraped personal addresses.
- For EU and UK recipients, a short legitimate-interest assessment written before the
  first send.

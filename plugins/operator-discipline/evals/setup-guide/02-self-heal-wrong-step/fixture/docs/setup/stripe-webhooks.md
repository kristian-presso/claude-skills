# Stripe webhooks for local development

Last verified: 2 March 2026

## What you are doing, and why
You will forward Stripe test events to your laptop so you can build the webhook handler.

## Before you start
- A Stripe account with test mode on.
- The Stripe CLI installed.

## Step 1 - Log in (1 min)
```bash
stripe login
```
Verify: the terminal prints "Done! The Stripe CLI is configured".

## Step 2 - Start the app (1 min)
```bash
npm run dev
```
Verify: the app answers on http://localhost:4242.

## Step 3 - Forward events (1 min)
```bash
stripe listen --forward localhost:4242/webhook
```
Verify: the CLI prints a webhook signing secret starting with whsec_.

## You are done

## Troubleshooting
| Symptom | Fix |
| --- | --- |
| 404 from the app | Check the route is /webhook |

## Changelog
- 2 March 2026: first version.

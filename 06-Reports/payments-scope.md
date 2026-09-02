# Taking payment on riversidefairways.com — scope

Christy by text, 2026-09-01 19:31: *"we are going to take Venmo and PayPal or a
credit card for bookings."* Clint: *"do you want me to wire that up on the site?"*
→ *"Yes please."*

## What is already true

- The site said **nothing** about payment anywhere before 2026-09-01. No deposit
  amount, no methods, no terms.
- **No commerce plugin is installed.** No WooCommerce, no Stripe plugin, no
  PayPal plugin, no payment add-ons for WS Form PRO (only `ws-form-pro` is on
  disk).
- **Elementor Pro already registers `paypal-button` and `stripe-button`.** They
  are licensed and available today — no new plugin, no new subscription.
- WS Form PRO is active with 5 forms (Request Quote, Request Appointment,
  Newsletter Signup, Contact Us, Free Consultation). Bookings currently run
  through a form + phone, with no payment step.

## The Venmo constraint — read this first

**Venmo cannot be integrated on its own.** In the US it exists as a funding
source inside PayPal's checkout. So "Venmo, PayPal, or a credit card" is one
integration, not three:

- **PayPal Checkout** covers PayPal balance + **Venmo** + guest card payments.
- **Stripe** is optional on top, purely for better card economics.

Doing PayPal alone satisfies everything Christy asked for. That is the
recommendation.

## Done 2026-09-01 (content, no checkout)

- FAQ **6322** "What payment methods do you accept?" — Venmo / PayPal / cards,
  deposit on quote, balance due on or before event day. Live on /faq/ and in the
  FAQPage schema. Filed under Pricing & Packages.

## Sandbox build — 2026-09-01

**No gateway plugin was installed, and none is needed.** Elementor Pro's
`paypal-button` and `stripe-button` both ship their own sandbox/test modes:

| Widget | Test control |
| --- | --- |
| `paypal-button` | `sandbox_mode` switcher + `sandbox_email` |
| `stripe-button` | `sandbox_mode` ("Stripe test environment") + test keys |

Installing WooCommerce to test this would have added tables, pages, menu entries
and page weight to a site that launched 2026-08-29, to do something Elementor
already does.

**Page 6323 — "Pay Your Deposit (SANDBOX TEST)"**, slug `pay-deposit-test`.
Draft, noindex, `elementor_canvas`, not linked from anywhere.
Preview: `https://riversidefairways.com/?page_id=6323&preview=true`

Verified by server-side render: form action is `https://sandbox.paypal.com/cgi-bin/webscr`,
`cmd=_xclick`, `amount=100`, `currency_code=USD`. **The live PayPal endpoint does
not appear in the markup at all.**

Two deliberate placeholders, both called out in copy at the top of the page:
- `business` = `REPLACE-ME-sandbox@business.example.com`
- `amount` = **$100**, invented. Christy has not set the real deposit.

Going live is: real sandbox email → test → swap in the live PayPal **business**
account, set the real amount, toggle `sandbox_mode` off.

## Still to build

1. **Deposit button** — Elementor Pro `paypal-button` on Pricing and/or the
   booking confirmation, set to a fixed deposit amount.
2. **Deposit amount and terms** — still `[[PLACEHOLDER]]` in the draft Booking &
   Cancellation Policy (post 1628). **Blocking**: nobody has said what the
   deposit is, when the balance is due, or the refund window.
3. **Payment line on Pricing + Contact** — one sentence each, mirroring the FAQ.
4. **Swag checkout** — the Swag page buttons now read "Ask About Swag" because
   there is no cart. Five items at fixed prices is a real (small) storefront if
   they want one; that is a WooCommerce-sized decision, not a PayPal button.

## Blocked on the client

- **PayPal business account** — email / merchant ID. A personal Venmo handle is
  not enough; Venmo-through-PayPal needs the business account.
- **Deposit amount** and balance-due terms.
- Whether Stripe is wanted alongside PayPal, which needs Stripe account keys.
- Whether Swag should actually check out, or stay enquiry-only.

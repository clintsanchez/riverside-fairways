# Event Rental Agreement — template copy

Built as a GHL **Documents & Contracts** template (`documents_contracts` is a
snapshot asset). All operator specifics are merge fields; event specifics come
from contact custom fields captured by the Date Request form. Terms below were
decided by Clint 2026-09-04 (cancellation / reschedule) and sourced from the
seed client's public FAQ, pricing page and Event Safety & Liability Terms.

**Before deploying to a new client:** these cancellation and reschedule terms are
one operator's posture, not an industry standard. Confirm they match the new
operator's actual policy rather than shipping them as-is.

Merge fields used (GHL document syntax):
`{{custom_values.business_name}}` `{{custom_values.business_phone}}`
`{{custom_values.business_email}}` `{{custom_values.rental_asset_name}}`
`{{custom_values.deposit_percent}}` `{{custom_values.balance_due_days_before_event}}`
`{{custom_values.space_requirement_footprint}}` `{{custom_values.space_requirement_height}}`
`{{custom_values.power_requirement}}` `{{custom_values.travel_fee_policy}}`
`{{contact.first_name}}` `{{contact.last_name}}` `{{contact.email}}` `{{contact.phone}}`
`{{contact.event_date}}` `{{contact.event_start_time}}` `{{contact.event_type}}`
`{{contact.venue_address}}` `{{contact.guest_count}}` `{{contact.indoor_or_outdoor}}`
`{{contact.package_interest}}` `{{contact.quoted_amount}}`

---

## EVENT RENTAL AGREEMENT

**{{custom_values.business_name}}** ("we", "us") and **{{contact.first_name}} {{contact.last_name}}** ("you", the "Host")
agree to the following for the rental of our {{custom_values.rental_asset_name}} at your event.

### 1. Event details

| | |
|---|---|
| Event date | {{contact.event_date}} |
| Start time | {{contact.event_start_time}} |
| Event type | {{contact.event_type}} |
| Venue | {{contact.venue_address}} |
| Setting | {{contact.indoor_or_outdoor}} |
| Approximate guests | {{contact.guest_count}} |
| Package | {{contact.package_interest}} |
| Quoted total | {{contact.quoted_amount}} |

Setup and teardown happen outside the booked hours and are included. Additional
hours, add-ons and travel are as shown on your quote.

### 2. Reserving your date

Your date is **not held** until we have both this signed agreement and the
deposit. Until then it stays open to other customers. We will confirm in
writing once both are in.

### 3. Deposit and balance

- A deposit of **{{custom_values.deposit_percent}}** of the quoted total reserves the date. **The deposit is non-refundable.**
- The remaining balance is due **{{custom_values.balance_due_days_before_event}} days before the event**. We will send a reminder with a payment link; you can pay online or we can charge the card on file with your OK.
- If the balance is not received by the due date we may release the date.

### 4. Cancellation

Tell us in writing (email or text) as early as you can.

- **7 or more days before the event:** the deposit is kept; any balance already paid is refunded in full.
- **Fewer than 7 days before the event:** the full quoted total is due and no refund is made.
- **Event day / no access to the venue at the scheduled time:** treated as a cancellation with fewer than 7 days' notice.

### 5. Rescheduling

We would much rather move your event than lose it.

- **7 or more days' notice:** one reschedule at no charge, subject to availability. Your deposit is credited to the new date for **12 months**.
- **Fewer than 7 days' notice:** subject to availability and a **$175 rebooking fee**; deposit credited for 12 months.
- Peak dates may carry different pricing, which we will confirm before you commit.

### 6. Weather and outdoor events

Rain, high wind, extreme heat and lightning can damage the equipment and create
a safety risk. For outdoor events please plan cover (tent, pavilion, garage,
covered patio) and a safe, dry power source in advance rather than waiting on
the forecast. Our on-site team decides on safety grounds whether to delay, pause,
relocate or end setup. If we cannot safely set up because of weather and no
suitable covered alternative is available, we will reschedule at your convenience
or refund what you paid us for that event, at your choice.

### 7. What we need at the venue

- Floor space of **{{custom_values.space_requirement_footprint}}**
- Ceiling or overhead clearance of **{{custom_values.space_requirement_height}}**
- **{{custom_values.power_requirement}}** within reach of the setup area
- Vehicle access to unload within a reasonable distance of the setup area
- Any venue approvals, permits or certificates of insurance the venue requires, requested from us at least 7 days before the event

If the space, power or access on the day does not match what was agreed and we
cannot set up safely, the event is treated as cancelled with fewer than 7 days'
notice.

### 8. Travel

{{custom_values.travel_fee_policy}}

### 9. Safety and liability

Our **Event Safety and Liability Terms** (published on our website) are part of
this agreement. In short: one person swings at a time; everyone else stays
behind the marked line; only our clubs and balls, or clubs we approve, are used;
children must be supervised by a responsible adult at all times, and our team
operates the simulator but does not provide childcare; serving alcohol and
compliance with alcohol laws are the Host's and venue's responsibility, and our
team may decline to let an intoxicated guest swing. Our team may pause or stop
play when these rules are not followed; repeated or serious violations may end
the event without refund.

The Host is responsible for damage to our equipment caused by guests beyond
normal wear, at repair or replacement cost.

### 10. If we have to cancel

If equipment failure, vehicle breakdown, illness, severe weather or another
event outside our reasonable control means we cannot deliver, we will contact
you as quickly as possible and either reschedule at your convenience or refund
everything you paid us for the event, including the deposit. We are not
responsible for other costs of your event such as venue, catering or rentals.

### 11. Photos

We may take photos and short video at the event for our own marketing unless you
tell us in writing before the event that you would prefer we do not.

### 12. Contact

{{custom_values.business_name}} · {{custom_values.business_phone}} · {{custom_values.business_email}}

---

**Signatures**

Host: ______________________ Date: __________
{{contact.first_name}} {{contact.last_name}}

For {{custom_values.business_name}}: ______________________ Date: __________

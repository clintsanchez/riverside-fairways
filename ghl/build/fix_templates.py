#!/usr/bin/env python3
"""Rewrite all 15 inherited email templates for mobile event rental.

Find/replace on the live HTML so the layout survives. Kills: the phantom
discount, fake scarcity, the 'Lindsey' persona, the vendor's support@ email,
the misspelled twillio_ phone field, and every home-services line. Every
merge field is validated against live custom-value keys before anything is
written - an unresolved key aborts the run.

  python3 fix_templates.py           # dry run: shows edits + any MISS
  python3 fix_templates.py --apply
"""
import json, os, re, subprocess, sys, time

LOC = "SdgdulZOPTsu8bEZYnzN"
BASE = "https://services.leadconnectorhq.com"
DRY = "--apply" not in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TMP = os.environ.get("SCRATCH", "/tmp")

env = {}
for l in open(os.path.join(REPO, ".env")):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); env[k] = v
if env["GHL_LOCATION_ID_TEMPLATE_EVENT"] != LOC: sys.exit("ABORT wrong location")
HDR = {"Authorization": f"Bearer {env['GHL_PIT_TEMPLATE_EVENT']}", "Version": "2021-07-28",
       "Content-Type": "application/json", "Accept": "application/json"}


def call(m, p, b=None):
    c = ["curl", "-s", "--max-time", "60", "-X", m, BASE + p, "-w", "\n__S__%{http_code}"]
    for k, v in HDR.items(): c += ["-H", f"{k}: {v}"]
    if b is not None: c += ["-d", json.dumps(b)]
    r = subprocess.run(c, capture_output=True, text=True, timeout=90)
    pay, st = r.stdout.rsplit("__S__", 1)
    try: return int(st.strip()), json.loads(pay.strip() or "{}")
    except json.JSONDecodeError: return int(st.strip()), {"_raw": pay[:200]}


# ---- our merge fields ------------------------------------------------------
V = lambda k: "{{ custom_values." + k + " }}"
PHONE, CAL, OWNER, BIZ = V("business_phone"), V("booking_page_url"), V("owner_first_name"), V("business_name")
ASSET = V("rental_asset_name")
FOOT, HEIGHT, POWER = V("space_requirement_footprint"), V("space_requirement_height"), V("power_requirement")
ADDON, ADDON_DESC = V("addon_package_name"), V("addon_package_description")
PRICING, REVIEW = V("pricing_page_url"), V("google_review_link")

# ---- global substitutions applied to every template ------------------------
GLOBAL = [
    (r'\{\{\s*custom_values\.company_calendar\s*\}\}', CAL),
    (r'\{\{\s*custom_values\.company_phone\s*\}\}', PHONE),
    (r'\{\{\s*custom_values\.twillio_tracking_phone_number\s*\}\}', PHONE),   # misspelled -> blank
    (r'>\s*Lindsey\s*<', ">" + OWNER + "<"),                                   # vendor persona
    (r'support@homeservice\.co', "{{custom_values.business_email}}"),          # vendor email
    (r'Warm regards,|Best regards,|Best wishes,|Warm wishes,', "Thanks,"),
    (r'please give use a call', "please give us a call"),                      # base typo
    # location.* does NOT travel in a snapshot - the business profile is not a
    # snapshot asset, so these render blank/broken in every cloned sub-account.
    # Applies to the header logo, the sign-off and the footer of all 15 bases.
    (r'\{\{\s*location\.logo_url\s*\}\}', "{{custom_values.logo_url}}"),
    (r'\{\{\s*location\.name\s*\}\}',     "{{custom_values.business_name}}"),
    (r'\{\{\s*location\.email\s*\}\}',    "{{custom_values.business_email}}"),
]

# ---- per-template literal replacements -------------------------------------
PER = {
"1 Hour Before Appointment Reminder": [
 ("Appointment Confirmed", "Talk Soon"),
 ("Your Appointment Is In 1 Hour!", "Your Call Is In 1 Hour"),
 ("Your appointment with {{custom_values.business_name}} is in 1 hour.", "Your call with {{custom_values.business_name}} is in 1 hour. Have your event date, venue and rough guest count handy and we'll make quick work of it."),
 ("If for any reason you need to cancel or reschedule your appointment please give us a call at:", "Need to move it? Just call or text"),
],
"24 Hour Appointment Reminder": [
 ("Appointment Confirmed", "Talk Tomorrow"),
 ("Your Appointment Is In 24 Hours!", "Your Call Is Tomorrow"),
 ("Your appointment with {{custom_values.business_name}} is in 24 hours.", "Your call with {{custom_values.business_name}} is tomorrow. If you can, have a photo or two of the space where you'd want the " + ASSET + " set up - it makes the conversation a lot more useful."),
 ("If for any reason you need to cancel or reschedule your appointment please give us a call at:", "Need to move it? Just call or text"),
],
"Appointment Confirmation Email": [
 ("Appointment Confirmed", "You're Booked In"),
 ("Your Appointment Is Confirmed!", "Your Call Is Confirmed"),
 ("Your appointment with {{custom_values.business_name}} has been confirmed.", "Your call with {{custom_values.business_name}} is confirmed. We'll go over your date, the venue, guest count and which setup fits - and get you a quote from there."),
 ("If for any reason you need to cancel or reschedule your appointment please give use a call at", "Need to move it? Just call or text"),
],
"Appointment Follow-Up": [
 ("How did the appointment with {{contact.name}} ({{contact.email}}) go?", "How did the call with {{contact.name}} ({{contact.email}}) go?"),
 ("They showed and purchased", "Booked - agreement signed and deposit paid"),
 ("They showed, got estimate & needs follow-up", "Quote sent - needs follow-up"),
 ("They showed but are not interested", "Talked - not a fit / not interested"),
 ("They didn't show", "They didn't show"),
],
"Got Estimate / Follow-Up": [
 ("Thanks for meeting with us to discuss your home project! We're excited about the opportunity to help bring your vision to life.",
  "Thanks for talking through your event with us - your quote is on its way if it isn't in your inbox already."),
 ("To ensure we provide the best possible service and personalized attention to each client, we do have limited project spots. We'd love for you to be one of them!",
  "One thing worth knowing: the date isn't reserved until the agreement is signed and the deposit is in. Until then it stays open to other inquiries. No pressure - just so a date you're set on doesn't slip while you decide."),
 ("So, while you're reviewing the proposal, feel free to reach out with any questions or concerns you may have.",
  "If anything in the quote is unclear, or you want to talk through a different package or add-on, just ask."),
 ("You can give us a call at {{custom_values.company_phone}} or simply reply to this email. We're here to help and can't wait to work with you on your project.",
  "Call or text " + PHONE + ", or reply to this email."),
 ("Book Your Appointment Now!", "See Packages"),
],
"New Appointment Notification": [
 ("You Have A New Appointment!", "New Call Booked"),
 ("A new lead has booked a new appointment with you.", "A lead has booked a call with you."),
 ("About The Appointment", "About The Call"),
 ("Appointment Date &amp; Time", "Call Date &amp; Time"),
 ("Please contact this lead as soon as possible.", "Check the unit calendar for their event date before the call so you can speak to availability."),
 ("If you have any questions, please contact your account manager", ""),
],
"New Lead Confirmation": [
 ("Dear {{contact.first_name}},", "Hi {{contact.first_name}},"),
 ("We're excited to have you on board and thrilled that you've decided to claim our exclusive offer! Thank you for your interest in what we have to offer.",
  "Thanks for reaching out about bringing the " + ASSET + " to your event - we got your inquiry and a real person will be in touch shortly."),
 ("To move forward and redeem your special deal, please schedule an appointment using the link provided: {{custom_values.company_calendar}}.",
  "The fastest way to get a firm answer on your date is a quick call. Grab a time here: " + CAL),
 ("This will ensure that you get the most out of our services and receive the personalized attention you deserve.",
  "On the call we'll confirm the date against our calendar, talk through your venue and guest count, and get you a quote."),
 ("In the meantime, if you have any questions or concerns, please don't hesitate to reach out to us. We're here to help and make your experience as smooth as possible.",
  "If you'd rather just text, " + PHONE + " goes straight to us."),
 ("Book Your Appointment Now!", "Book a Quick Call"),
],
"New Lead Notification": [
 ("You Have A New Lead!", "New Event Inquiry"),
 ("A new lead has expressed interest in your offer.", "Someone just sent an event inquiry. Speed matters - most people are messaging several vendors right now."),
 ("Please contact this lead as soon as possible.", "Reply within 5 minutes if you can. Check the unit calendar for their date before you promise anything."),
 ("If you have any questions, please contact your account manager", ""),
],
"No Show Appointment": [
 ("Looks like we missed each other during our scheduled appointment on {{appointment.start_time}}. No worries, things happen!",
  "Looks like we missed each other for our call at {{appointment.start_time}}. No worries at all."),
 ("Are you still interested in our services? If so, just reply to this email, and we can find a better time that works for both of us. If not, that's cool too &ndash; just let us know.",
  "Still planning the event? Reply here or text " + PHONE + " and we'll find a time that works. If plans changed, that's fine too - just let us know."),
 ("Alternatively you can book a new appointment using this link:", "Or grab a new time here:"),
 ("Book Your Appointment Now!", "Rebook a Call"),
],
# ---- the six nurture emails: real information, zero offers -----------------
"Nurture Campaign: Email #1": [
 ("{{contact.first_name}}, Your Home Needs Some Love ❤️", "{{contact.first_name}}, three things to check before you book"),
 ("We hope you're doing great! Here at {{custom_values.business_name}}, we're dedicated to making sure your home is always in tip-top shape. That's why we want to remind you that our expert team is here to help with all your home maintenance needs.",
  "You asked about bringing the " + ASSET + " to an event, so here's the thing that saves the most headaches: three questions about the venue, answered early."),
 ("But wait! We've got some fantastic news for you. If you book a call with us before the end of the week, you'll get an exclusive discount on our services. Don't miss this limited-time offer!",
  "Space: we generally need " + FOOT + " of floor and " + HEIGHT + ". Height is the one people forget. Power: " + POWER + ". Access: how does gear get from the truck to the spot - doors, stairs, gates, parking? If any of those are uncertain, a couple of phone photos settle it in minutes."),
 ("🔗 Book a Call Now:", "Talk it through:"),
 ("Or simply give us a call at {{custom_values.twillio_tracking_phone_number}}, and one of our friendly team members will assist you in scheduling your appointment.",
  "Or text photos of the space to " + PHONE + " and we'll tell you what we see."),
 ("Looking forward to helping you take care of your home, {{contact.first_name}}.", ""),
 ("Claim Your Exclusive Discount Today!", "Book a Quick Call"),
],
"Nurture Campaign: Email #2": [
 ("Last Chance, {{contact.first_name}}! Don't Miss Out on Our Exclusive Offer", "{{contact.first_name}}, how a date actually gets held"),
 ("Time is running out, and we don't want you to miss the chance to take advantage of our exclusive discount offer for your home maintenance needs.",
  "Worth being straight about this, because it trips people up: asking about a date doesn't hold it, and neither does getting a quote."),
 ("Remember, you only have until the end of the week to book a call with us and claim your special discount.",
  "A date is reserved when two things have happened - the agreement is signed and the deposit is in. Until both land, the day stays open to anyone else who asks. We only have the one unit, so we can't pencil people in. If you're set on a specific Saturday, that's the reason to get the paperwork done rather than sit on the quote."),
 ("🔗 Schedule Your Call Now:", "Questions about your date?"),
 ("Alternatively, you can reach out to us at {{custom_values.twillio_tracking_phone_number}} to schedule your appointment.", "Or text " + PHONE + "."),
 ("Don't let this opportunity slip away, {{contact.first_name}}. Our team at {{custom_values.business_name}} is ready to provide you with the best service for your home.", ""),
 ("Book Now & Save - Limited Time Offer!", "Book a Quick Call"),
],
"Nurture Campaign: Email #3": [
 ("{{contact.first_name}}, We're Almost Fully Booked!", "{{contact.first_name}}, indoors or outdoors?"),
 ("Wow! Our calendar is filling up fast, and we don't want you to miss the chance to book your call with us before all the slots are taken.",
  "If your event is outside, one decision makes the whole day less stressful: know your backup spot before you need it."),
 ("Act now, and you can still claim your exclusive discount offer for your home maintenance needs. But hurry, as there are only a few slots remaining!",
  "The gear itself handles a fair amount, but heavy rain, high wind, extreme heat and lightning are safety calls the team makes on site - and conditions change faster than forecasts do. Having a covered or indoor option identified in advance means a change in weather is a five-minute move, not a cancelled party. Tell us where that spot would be and we'll check it fits the same way we check the main one."),
 ("🔗 Book Your Call Today:", "Talk through your venue:"),
 ("Or give us a call at {{custom_values.twillio_tracking_phone_number}} to secure your appointment.", "Or text " + PHONE + "."),
 ("We're looking forward to serving you and making your home the best it can be, {{contact.first_name}}.", ""),
 ("Secure Your Discounted Slot Now!", "Book a Quick Call"),
],
"Nurture Campaign: Email #4": [
 ("{{contact.first_name}}, Let's Get Your Home Ready for the Season!", "{{contact.first_name}}, what if half your guests aren't into it?"),
 ("As the seasons change, it's crucial to ensure your home is prepared to face new challenges. At {{custom_values.business_name}}, we're here to help you keep your home in perfect condition.",
  "The most common hesitation we hear isn't price. It's 'will people actually use it?' Fair question - so here's the honest answer."),
 ("Great news! We have a special offer just for you. Book a call with us before the end of the week to receive a limited-time discount on our services.",
  "For a crowd of enthusiasts, the standard setup is the right call. For a mixed group - kids, non-players, an evening where the main activity is really the conversation - that's what " + ADDON + " is for: " + ADDON_DESC + " Tell us who's coming and we'll steer you to the setup that fits, not the biggest one."),
 ("🔗 Reserve Your Spot:", "Tell us about your crowd:"),
 ("You can also reach us at {{custom_values.twillio_tracking_phone_number}} to schedule your appointment over the phone.", "Or text " + PHONE + "."),
 ("Act now and make sure your home stays in pristine condition, {{contact.first_name}}.", ""),
 ("Get Your Seasonal Discount - Book Now!", "Book a Quick Call"),
],
"Nurture Campaign: Email #5": [
 ("Friendly Reminder, {{contact.first_name}}: Exclusive Offer Ending Soon", "{{contact.first_name}}, booking for a company or organization?"),
 ("We wanted to send a quick reminder about our exclusive discount offer for your home maintenance needs. Time is ticking, and this amazing deal will end on Sunday.",
  "If this is for a company event, a fundraiser, a school or a venue with its own rules, a few things run differently and it helps to raise them early."),
 ("Don't miss the chance to enjoy our expert services at a discounted price.",
  "Certificates of insurance: many venues want one, sometimes with specific wording. Those come from our insurer and take a little lead time, so send the venue's exact ask as soon as you have it. Invoicing: if you need a W-9, a PO number or net terms, say so up front. Multiple dates: tell us the whole run and we'll look at it together rather than one date at a time."),
 ("🔗 Secure Your Discount:", "Set up a proper conversation:"),
 ("If you prefer to speak with someone, please give us a call at {{custom_values.twillio_tracking_phone_number}}, and we'll be happy to help you schedule your appointment.", "Or text " + PHONE + "."),
 ("Take advantage of this limited-time offer, {{contact.first_name}}, and keep your home in top shape.", ""),
 ("Grab Your Discount Before It's Gone!", "Book a Quick Call"),
],
"Nurture Campaign: Email #6": [
 ("Hurry, {{contact.first_name}}! Our Calendar is Filling Up Fast", "{{contact.first_name}}, last one from us"),
 ("Our appointment slots are being booked rapidly, and we wanted to make sure you don't miss out on our exclusive discount offer for your home maintenance needs.",
  "This is the last email in this series, so we'll stop filling your inbox after this."),
 ("Remember, this special deal is only available until the end of the week, so act fast to secure your spot.",
  "If the event's still on the table, we're around - reply here, text, or book a quick call and we'll check your date. If plans changed, no hard feelings. And if it's something you do every year, tell us and we'll reach out well before next time instead of leaving you to remember."),
 ("🔗 Claim Your Discounted Appointment:", "Still thinking about it?"),
 ("If you'd rather speak with us directly, please call {{custom_values.twillio_tracking_phone_number}} to schedule your appointment.", "Or text " + PHONE + "."),
 ("Don't wait, {{contact.first_name}}. Let our team at {{custom_values.business_name}} help you keep your home in perfect condition.", ""),
 ("Reserve Your Discounted Spot - Act Fast!", "Book a Quick Call"),
],
}


def main():
    # validate every merge field we intend to write
    st, d = call("GET", f"/locations/{LOC}/customValues")
    if st != 200: sys.exit(f"ABORT customValues {st}")
    live = {re.sub(r'[{}\s]', '', v["fieldKey"]).split(".")[-1] for v in d["customValues"]}
    want = set()
    for pairs in PER.values():
        for _, b in pairs: want |= set(re.findall(r'custom_values\.([a-z0-9_]+)', b))
    for _, b in GLOBAL: want |= set(re.findall(r'custom_values\.([a-z0-9_]+)', b))
    missing = sorted(want - live)
    if missing: sys.exit(f"ABORT unresolved merge fields (would render blank): {missing}")
    print(f"merge fields OK ({len(want)} used, all resolve)\n")

    st, t = call("GET", f"/emails/builder?locationId={LOC}&limit=100&templatesOnly=true")
    if st != 200: sys.exit(f"ABORT list {st}")
    print(f"{'DRY RUN' if DRY else 'APPLYING'}\n")
    seen = set(); tot_miss = 0
    for x in t.get("builders", []):
        nm = x.get("name")
        if nm not in PER: continue
        seen.add(nm)
        p = f"{TMP}/fix_{x['id']}.html"
        subprocess.run(["curl", "-s", "--max-time", "40", x["previewUrl"], "-o", p], timeout=60)
        s = open(p, encoding="utf-8", errors="replace").read()
        n = 0; miss = []
        # per-template literals FIRST - they match the base merge fields verbatim;
        # GLOBAL then rewrites whatever base fields remain.
        for a, b in PER[nm]:
            if a in s: s = s.replace(a, b); n += 1
            else: miss.append(a[:50])
        for pat, rep in GLOBAL:
            s, c = re.subn(pat, rep, s); n += c
        tot_miss += len(miss)
        print(f"  {nm:34} {n:2} edits" + (f"  MISS {len(miss)}" if miss else ""))
        for m in miss: print(f"      not found: {m}")
        if DRY: continue
        st, d = call("POST", "/emails/builder/data",
                     {"locationId": LOC, "templateId": x["id"], "updatedBy": "api",
                      "html": s, "editorType": "html", "dnd": {}, "isPlainText": False})
        print(f"      -> HTTP {st}" + ("" if st in (200, 201) else f" {json.dumps(d)[:160]}"))
        time.sleep(0.4)
    for nm in set(PER) - seen: print(f"  !! template not found in account: {nm}")
    if DRY:
        print(f"\nDRY RUN - {tot_miss} unmatched strings. Rerun with --apply" +
              (" after fixing the misses." if tot_miss else "."))


if __name__ == "__main__":
    main()

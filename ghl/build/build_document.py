#!/usr/bin/env python3
"""Write a GHL Documents & Contracts template as data.

Captured 2026-09-04 from the template builder (leadgen-apps-template-builder):
  POST https://services.leadconnectorhq.com/proposals/templates   {name, type:"proposal", locationId, isPublicDocument:false} -> {_id}
  GET  https://services.leadconnectorhq.com/proposals/templates/{id}?locationId=   full body
  PUT  https://services.leadconnectorhq.com/proposals/templates/{id}                full body (pages[] of elements)
Auth: Firebase `token-id` + channel: APP + source: WEB_USER + Version: 2021-07-28
(the location PIT is refused on the single-template routes: "token is not authorized for this scope").

Page = 816x1056 px, margins 48. Elements are absolutely positioned
(responsiveStyles.large.position.top/left, page-relative px). Text elements
carry HTML in component.options.text. Fillable fields (Signature, DateField,
TextField) are also listed in top-level `fillableFields`.

Spec JSON:
  {"name": "...", "pages": [ {"html": "<h1>..</h1>...", "elements": [ {"kind":"signature"|"date"|"textfield", "top":..,"left":..,"label":..} ]} ]}

  python build/build_document.py --target template-event --spec snapshots/event-rental/config/agreement.json [--live] [--template-id <id>]
"""
from __future__ import annotations

import argparse, json, os, sys, uuid
import requests
from ghl_target import add_target_args, resolve

SVC = "https://services.leadconnectorhq.com"
G, Y, R, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[1m", "\033[0m"
PAGE_W, PAGE_H, MARGIN = 816, 1056, 48


def hdrs():
    tok = os.getenv("GHL_TOKEN_ID", "").strip()
    if not tok: sys.exit(R + "GHL_TOKEN_ID not set (Firebase token from the browser)" + X)
    return {"token-id": tok, "channel": "APP", "source": "WEB_USER", "Version": "2021-07-28", "content-type": "application/json"}


def text_el(html, top, left=MARGIN, width=PAGE_W - 2 * MARGIN, bg="", pads=("0px", "0px", "0px", "0px")):
    return {"type": "Text", "version": 1, "id": str(uuid.uuid4()), "children": [],
            "component": {"name": "Text Element", "options": {"text": html}},
            "responsiveStyles": {"large": {"paddingTop": pads[0], "paddingBottom": pads[1], "paddingLeft": pads[2], "paddingRight": pads[3],
                                           "marginTop": None, "marginBottom": None, "marginLeft": None, "marginRight": None, "backgroundColor": bg,
                                           "dimensions": {"width": width}, "scale": {"scaleX": 1, "scaleY": 1},
                                           "position": {"top": top, "left": left}}}}


def image_el(src, height=64, width=240):
    return {"type": "Image", "version": 1, "id": str(uuid.uuid4()), "children": [],
            "component": {"name": "Image Element", "options": {"src": src, "altText": "logo", "href": ""}},
            "responsiveStyles": {"large": {"align": "img-left", "paddingTop": "6px", "paddingBottom": "26px", "paddingLeft": "0px", "paddingRight": "0px",
                                           "marginTop": None, "marginBottom": None, "marginLeft": None, "marginRight": None, "backgroundColor": "",
                                           "height": str(height), "width": str(width), "imageEffect": "img-full-color", "scale": {"scaleX": 1, "scaleY": 1}, "position": {"top": 0, "left": MARGIN}}}}


def brand_chrome(loc, H, title, subtitle):
    """Header (logo row + title band) and footer band from the location's custom values. Elements flow in order, positions are ignored."""
    cv = {v["name"]: (v.get("value") or "") for v in requests.get(f"{SVC}/locations/{loc}/customValues", headers=H, timeout=45).json()["customValues"]}
    c1 = cv.get("Color 1") or "#306553"; c2 = cv.get("Color 2") or "#111111"; logo = cv.get("Logo URL", "")
    head = []
    if logo.startswith("http"): head.append(image_el(logo))
    head.append(text_el(f'<h2 style="font-family: Open Sans; font-size: 20px; font-weight: 700; color: #ffffff; margin: 0;">{title}</h2>'
                        f'<h4 style="font-family: Open Sans; font-size: 11px; font-weight: 400; color: #ffffff; margin: 6px 0 0 0;">{subtitle}</h4>', 0, 0, PAGE_W, c2, ("22px", "22px", "48px", "48px")))
    head.append(text_el('<p style="margin:0;line-height:4px;">&nbsp;</p>', 0, 0, PAGE_W, c1, ("0px", "0px", "0px", "0px")))
    head.append(text_el('<p style="margin:0;line-height:10px;">&nbsp;</p>', 0, 0, PAGE_W, "", ("0px", "14px", "0px", "0px")))  # air under the band
    foot = text_el('<h4 style="font-family: Open Sans; font-size: 10px; font-weight: 400; color: ' + c1 + '; margin: 0; text-align: center;">{{custom_values.business_name}} &middot; {{custom_values.business_phone}} &middot; {{custom_values.business_email}} &middot; {{custom_values.business_website}}</h4>', 0, 0, PAGE_W, "#F5EFE5", ("12px", "12px", "0px", "0px"))
    return head, foot, c1, cv


def polish(html):
    """Typographic air: section headings get a top gap, list rows and paragraphs get real spacing."""
    return (html.replace('font-size: 14px; margin: 14px 0 6px 0;', 'font-size: 14px; margin: 26px 0 10px 0;')
                .replace('font-size: 12px; margin: 0 0 4px 12px;', 'font-size: 12px; margin: 0 0 9px 12px;')
                .replace('font-size: 12px; margin: 0 0 4px 0;', 'font-size: 12px; margin: 0 0 8px 0;')
                .replace('font-size: 12px; margin: 0 0 8px 0;', 'font-size: 12px; margin: 0 0 12px 0;')
                .replace('line-height: 1.45;', 'line-height: 1.6;'))


def owner_block(cv, c1):
    """Optional sign-off photo: Owner Photo URL custom value -> small round-ish image with name and title."""
    photo = cv.get("Owner Photo URL", "")
    if not photo.startswith("http"): return []
    img = image_el(photo, 150, 230); img["responsiveStyles"]["large"]["paddingBottom"] = "6px"; img["responsiveStyles"]["large"]["paddingTop"] = "18px"
    return [img, text_el('<h4 style="font-family: Open Sans; font-size: 12px; font-weight: 700; color: ' + c1 + '; margin: 0;">{{custom_values.owner_full_name}}</h4><p style="font-size: 11px; color: #475467; margin: 2px 0 14px 0;">{{custom_values.business_name}} &middot; {{custom_values.business_phone}}</p>', 0)]


def field_el(kind, field_id, top, left, label="", recipient="assignedContact", width=None):
    base_styles = {"align": "signature-left", "paddingTop": "0px", "paddingBottom": "0px", "paddingLeft": "0px", "paddingRight": "0px",
                   "marginTop": None, "marginBottom": None, "marginLeft": None, "marginRight": None, "scale": {"scaleX": 1, "scaleY": 1},
                   "position": {"top": top, "left": left}}
    if kind == "signature":
        return {"type": "Signature", "version": 2, "id": str(uuid.uuid4()), "children": [],
                "component": {"isDraggable": True, "name": "Signature Element", "options": {"isGhost": True, "showName": True, "text": label or "Signature", "required": True, "fieldId": field_id, "src": "", "recipient": recipient, "timestamp": None, "entityName": "contacts"}},
                "responsiveStyles": {"large": {**base_styles, "dimensions": {"width": width or 190, "height": 68}}}}, None
    if kind == "date":
        el = {"type": "DateField", "version": 1, "id": str(uuid.uuid4()), "children": [],
              "component": {"isDraggable": True, "name": "Text Field Element", "options": {"isGhost": True, "text": "", "required": True, "fieldId": field_id, "src": "", "recipient": recipient, "timestamp": None, "entityName": "contacts", "placeholder": label or "Select date", "availableDates": "any", "dateFormat": "yyyy-MM-dd"}},
              "responsiveStyles": {"large": {**base_styles, "dimensions": {"width": width or 190, "height": 40}}}}
        return el, {"value": "", "fieldId": field_id, "isRequired": True, "recipient": recipient, "hasCompleted": False, "entityType": "contacts", "id": str(uuid.uuid4()), "type": "DateField"}
    el = {"type": "TextField", "version": 1, "id": str(uuid.uuid4()), "children": [],
          "component": {"isDraggable": True, "name": "Text Field Element", "options": {"isGhost": True, "text": "", "required": True, "fieldId": field_id, "src": "", "recipient": recipient, "timestamp": None, "entityName": "contacts", "placeholder": label or "Enter value"}},
          "responsiveStyles": {"large": {**base_styles, "dimensions": {"width": width or 260, "height": 40}}}}
    return el, {"value": "", "fieldId": field_id, "isRequired": True, "recipient": recipient, "hasCompleted": False, "entityType": "contacts", "id": str(uuid.uuid4()), "type": "TextField"}


def page_el(children):
    return {"type": "Page", "version": 2, "children": children, "id": str(uuid.uuid4()),
            "component": {"name": "Page", "options": {"src": "", "pageDimensions": {"dimensions": {"width": PAGE_W, "height": PAGE_H}, "margins": {"top": MARGIN, "right": MARGIN, "bottom": MARGIN, "left": MARGIN}, "rotation": "portrait"}}},
            "responsiveStyles": {"large": {"backgroundColor": "#ffffff", "backgroundPosition": "top left", "backgroundSize": "cover", "backgroundRepeat": "repeat", "opacity": 100}}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap); ap.add_argument("--spec", required=True); ap.add_argument("--template-id")
    args = ap.parse_args(); t = resolve(args); loc = t.location_id; H = hdrs()
    spec = json.load(open(args.spec))
    pages, fillable = [], []
    n = 0
    head, foot, c1, cv = brand_chrome(loc, H, spec.get("title", spec["name"]).upper(), spec.get("subtitle", "Prepared by {{custom_values.business_name}} for {{contact.first_name}} {{contact.last_name}}")) if spec.get("brand", True) else ([], None, "#306553", {})
    for i, pg in enumerate(spec["pages"]):
        html = polish(pg["html"]).replace("font-family: Open Sans;", "font-family: Open Sans; color: " + c1 + ";")  # headings take the brand color
        children = (head if i == 0 else []) + [text_el(html, pg.get("top", MARGIN))]
        for e in pg.get("elements", []):
            n += 1
            el, ff = field_el(e["kind"], e.get("fieldId") or f"{e['kind']}_{n}", e["top"], e.get("left", MARGIN), e.get("label", ""), e.get("recipient", "assignedContact"), e.get("width"))
            children.append(el)
            if ff: fillable.append(ff)
        if foot and i == len(spec["pages"]) - 1:
            if spec.get("owner_signoff"): children.extend(owner_block(cv, c1))
            children.append(foot)
        pages.append(page_el(children))
    print(f"{B}{spec['name']}{X}: {len(pages)} pages, {sum(len(p['children']) for p in pages)} elements, {len(fillable)} fillable fields  ({'LIVE' if t.live else 'dry run'})")
    if not t.live: return 0

    tid = args.template_id
    if not tid:
        r = requests.post(f"{SVC}/proposals/templates", headers=H, data=json.dumps({"name": spec["name"], "type": "proposal", "locationId": loc, "isPublicDocument": False}), timeout=45)
        if not r.ok: sys.exit(R + f"create failed {r.status_code} {r.text[:200]}" + X)
        tid = r.json().get("_id") or r.json().get("id"); print(G + f"  created template {tid}" + X)
    d = requests.get(f"{SVC}/proposals/templates/{tid}", headers=H, params={"locationId": loc}, timeout=45).json()
    body = {k: v for k, v in d.items() if k not in ("_id", "__v", "createdAt", "updatedAt", "traceId", "versionHistory", "deleted", "updatedBy", "docFormPublicLink", "contentLibraryThumbnail", "assignedRoles", "tags", "type", "version", "isPublicDocument")}
    if not isinstance(d.get("timezone"), dict): body["timezone"] = {"zone": "America/Chicago", "abbreviation": "CDT"}
    body.update({"name": spec["name"], "locationId": loc, "pages": pages, "fillableFields": fillable, "fontsToLoad": ["Open Sans"],
                 "roles": d.get("roles") or [], "recipients": d.get("recipients") or [], "groups": d.get("groups") or [], "pricingTables": d.get("pricingTables") or []})
    p = requests.put(f"{SVC}/proposals/templates/{tid}", headers=H, data=json.dumps(body), timeout=60)
    print((G if p.ok else R) + f"  PUT {p.status_code} {'' if p.ok else p.text[:300]}" + X)
    print(f"  template id: {tid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

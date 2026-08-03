"""Convert icons from the golf pack into the Riverside Fairways badge format."""
import re, pathlib
from PIL import Image
import numpy as np

PACK = pathlib.Path("/Users/clintsanchez/Downloads/golf-icon-pack-2026-02-24-01-11-27-utc/outline/svg")
GREEN = "#306553"
BADGE = f'<rect x="10" y="14" width="341" height="341" rx="21" fill="{GREEN}"/>'
TARGET = (46, 14, 454, 490)   # art box used by the original six
FATTEN = 3                    # +3 lifts line weight 17 -> 20, matching the originals


def inner(path):
    s = pathlib.Path(path).read_text()
    m = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S)
    body = m.group(1)
    body = re.sub(r'\s(fill|stroke)="[^"]*"', "", body)   # drop baked colours
    return body


def wrap(body, transform="", fatten=FATTEN):
    """The pack draws thinner lines than the original six relative to content
    size. Adding a matching stroke to the filled outline shapes brings the line
    weight from ~17 up to the originals' 20 without scaling past the canvas."""
    tr = ' transform="%s"' % transform if transform else ""
    fat = ("" if not fatten else
           ' stroke="#FFFFFF" stroke-width="%s" stroke-linejoin="round"'
           ' stroke-linecap="round"' % fatten)
    g = '<g fill="#FFFFFF"%s%s>%s</g>' % (fat, tr, body)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" '
            'viewBox="0 0 500 500">%s%s</svg>' % (BADGE, g))


def art_box(png):
    a = np.array(Image.open(png).convert("RGBA"))
    w = (a[..., 0] > 235) & (a[..., 1] > 235) & (a[..., 2] > 235) & (a[..., 3] > 200)
    ys, xs = np.where(w)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def stroke_of(png):
    a = np.array(Image.open(png).convert("RGBA"))
    w = (a[...,0] > 235) & (a[...,1] > 235) & (a[...,2] > 235) & (a[...,3] > 200)
    runs = []
    for y in range(0, 500, 2):
        c = 0
        for v in w[y]:
            if v: c += 1
            else:
                if 4 < c < 70: runs.append(c)
                c = 0
    return float(np.median(runs)) if runs else 0.0


TARGET_STROKE = 20.0     # measured mean of the original six
CENTER = (250, 252)      # centre of the originals' art box


def build(page, name, out_dir, target=None):
    """Scale by STROKE WEIGHT, not bounding box: matching line weight is what
    makes an icon read as part of the same set."""
    body = inner(PACK / f"{name}.svg")
    tmp = out_dir / "_t.png"

    def render(svg, dst):
        page.set_content(f'<body style="margin:0;background:transparent">{svg}</body>')
        page.wait_for_timeout(110)
        page.screenshot(path=str(dst), omit_background=True)

    # pass 1: reference scale, measure stroke and bbox
    s0 = 0.85
    ref = "translate(%.2f,%.2f) scale(%.4f)" % (250 - 256*s0, 252 - 256*s0, s0)
    render(wrap(body, ref), tmp)
    st = stroke_of(tmp)
    x0, y0, x1, y1 = art_box(tmp)
    tmp.unlink()
    if st <= 0:
        return wrap(body, ref)

    s = s0 * (TARGET_STROKE / st)
    # keep the art inside the canvas with a small bleed, like the originals
    w = (x1 - x0) * (s / s0); h = (y1 - y0) * (s / s0)
    cap = min(492 / w, 492 / h, 1.0)
    if cap < 1.0:
        s *= cap
    cx, cy = ((x0 + x1) / 2) / s0, ((y0 + y1) / 2) / s0   # centre in user units
    tr = "translate(%.2f,%.2f) scale(%.4f)" % (CENTER[0] - cx*s, CENTER[1] - cy*s, s)
    return wrap(body, tr)

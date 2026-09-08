"""
Resolve which sub-account a build script is allowed to touch.

Every script under build/ goes through here. It exists because the internal API
and the browser driver can both write to a live client CRM, and the failure mode
is silent: the write succeeds, just in the wrong account.

Two rules, both deliberate:

  1. The target must be named explicitly. There is no default. Omitting --target
     is an error, not a fallback to primary.
  2. Writes are refused unless --live is passed. Dry-run is the default so a
     half-finished script cannot mutate anything by being run.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Slug -> the .env names holding that sub-account's credentials.
# Mirrors ghl_locations.py; kept separate so build scripts cannot accidentally
# inherit 'primary' as a default the way the older helper allows.
TARGETS: dict[str, dict[str, str]] = {
    # Two tokens exist for the same sub-account. GHL_PIT_AGENCY is older and
    # lacks customFields/payments/workflows scopes; GHL_PIT_GROW is the Private
    # Integration created for the Grow site and can read everything. Prefer
    # "grow" unless you specifically need the older token.
    # This machine's .env carries the primary sub-account under the plain
    # GHL_PIT / GHL_LOCATION_ID names rather than the *_AGENCY pair.
    "primary":         {"pit": "GHL_PIT",                 "loc": "GHL_LOCATION_ID",                    "label": "BlakSheep Creative (primary)"},
    "grow":            {"pit": "GHL_PIT_GROW",             "loc": "GHL_LOCATION_ID_AGENCY",             "label": "BlakSheep Creative — Grow"},
    "agency":          {"pit": "GHL_PIT_AGENCY",           "loc": "GHL_LOCATION_ID_AGENCY",             "label": "BlakSheep Creative (agency, limited scopes)"},
    "southern-dreams": {"pit": "GHL_PIT_SOUTHERN_DREAMS",  "loc": "GHL_LOCATION_ID_SOUTHERN_DREAMS",    "label": "Southern Dreams Mechanical"},
    "template-patio":  {"pit": "GHL_PIT_TEMPLATE_PATIO",   "loc": "GHL_LOCATION_ID_TEMPLATE_PATIO",     "label": "Template — Patio"},
    "template-event":  {"pit": "GHL_PIT_TEMPLATE_EVENT",   "loc": "GHL_LOCATION_ID_TEMPLATE_EVENT",     "label": "Template — Mobile Event Rental"},
    "riverside":       {"pit": "GHL_PIT_RIVERSIDE",         "loc": "GHL_LOCATION_ID_RIVERSIDE",          "label": "Riverside Fairways (client)"},
    "inspect-hvac":    {"pit": "GHL_PIT_INSPECT_HVAC",     "loc": "GHL_LOCATION_ID_INSPECT_HVAC",       "label": "Inspect — HVAC"},
    "inspect-roofing": {"pit": "GHL_PIT_INSPECT_ROOFING",  "loc": "GHL_LOCATION_ID_INSPECT_ROOFING",    "label": "Inspect — Roofing"},
    "inspect-land":    {"pit": "GHL_PIT_INSPECT_LAND",     "loc": "GHL_LOCATION_ID_INSPECT_LAND",       "label": "Inspect — Land"},
    "inspect-remodel": {"pit": "GHL_PIT_INSPECT_REMODEL",  "loc": "GHL_LOCATION_ID_INSPECT_REMODEL",    "label": "Inspect — Remodel"},
    "inspect-react":   {"pit": "GHL_PIT_INSPECT_REACT",    "loc": "GHL_LOCATION_ID_INSPECT_REACT",      "label": "Inspect — React"},
    "inspect-smma":    {"pit": "GHL_PIT_INSPECT_SMMA",     "loc": "GHL_LOCATION_ID_INSPECT_SMMA",       "label": "Inspect — SMMA"},
    "inspect-aibot":   {"pit": "GHL_PIT_INSPECT_AIBOT",    "loc": "GHL_LOCATION_ID_INSPECT_AIBOT",      "label": "Inspect — AI Bot"},
}


@dataclass
class Target:
    slug: str
    label: str
    token: str
    location_id: str
    live: bool

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Version": "2021-07-28",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def guard(self, what: str) -> None:
        """Refuse a write unless --live was passed. Call before every mutation."""
        if not self.live:
            raise SystemExit(
                f"\n  DRY RUN — would {what}\n"
                f"  Target: {self.label}\n"
                f"  Pass --live to actually do it.\n"
            )


def add_target_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--target",
        required=True,
        help="Sub-account slug. Required — there is no default. "
             f"Choices: {', '.join(sorted(TARGETS))}",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Actually perform writes. Without it, writes are refused.",
    )


def resolve(args: argparse.Namespace) -> Target:
    load_dotenv()
    slug = args.target
    if slug not in TARGETS:
        raise SystemExit(
            f"\n  Unknown target '{slug}'.\n"
            f"  Choices: {', '.join(sorted(TARGETS))}\n"
        )
    cfg = TARGETS[slug]
    token = os.getenv(cfg["pit"], "").strip()
    loc = os.getenv(cfg["loc"], "").strip()
    if not token or not loc:
        raise SystemExit(
            f"\n  Missing {cfg['pit']} or {cfg['loc']} in .env for target '{slug}'.\n"
        )
    t = Target(slug, cfg["label"], token, loc, bool(args.live))
    mode = "LIVE — writes enabled" if t.live else "dry run — writes refused"
    print(f"\n  Target: {t.label}  [{slug}]\n  Mode:   {mode}\n")
    return t

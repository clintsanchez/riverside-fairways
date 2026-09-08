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
    # Trimmed copy. The full registry (every BSC sub-account) lives in
    # ghl-toolkit/build/ghl_target.py; this repo only needs Riverside and the
    # template it was built from.
    "riverside":      {"pit": "GHL_PIT_RIVERSIDE",      "loc": "GHL_LOCATION_ID_RIVERSIDE",      "label": "Riverside Fairways (client)"},
    "template-event": {"pit": "GHL_PIT_TEMPLATE_EVENT", "loc": "GHL_LOCATION_ID_TEMPLATE_EVENT", "label": "Template — Mobile Event Rental"},
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

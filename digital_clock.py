#!/usr/bin/env python3
"""Digital clock for multiple time zones.

Example:
    python digital_clock.py --zones UTC America/New_York Europe/London Asia/Tokyo
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo


def format_time(zone_name: str) -> str:
    """Return a formatted time string for the provided timezone."""
    zone = ZoneInfo(zone_name)
    now = datetime.now(zone)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def display_clock(zones: list[str], refresh_seconds: float = 1.0) -> None:
    """Display a live digital clock for each timezone."""
    while True:
        lines = ["Digital Clock"]
        for zone in zones:
            try:
                lines.append(f"{zone}: {format_time(zone)}")
            except Exception:
                lines.append(f"{zone}: Invalid timezone")

        os.system("cls" if os.name == "nt" else "clear")
        print("\n".join(lines))
        time.sleep(refresh_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Display a digital clock for multiple time zones.")
    parser.add_argument(
        "--zones",
        nargs="+",
        default=["UTC", "America/New_York", "Europe/London", "Asia/Tokyo"],
        help="List of IANA timezone names to display (for example: UTC America/New_York Europe/London Asia/Tokyo).",
    )
    parser.add_argument(
        "--refresh",
        type=float,
        default=1.0,
        help="Refresh interval in seconds (default: 1.0).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        display_clock(args.zones, args.refresh)
    except KeyboardInterrupt:
        print("\nClock stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()

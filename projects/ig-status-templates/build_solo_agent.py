#!/usr/bin/env python3
"""Build the solo agent contact card for Jessica Wallace. Headshot is a
placeholder initial-badge until a real photo is supplied — add
"photo": Path(...) to AGENT below and rerun.

    python3 build_solo_agent.py
"""

from agent_card_common import build

AGENT = {"name": "Jessica Wallace", "phone": "0422 962 688"}


def main():
    build([AGENT], "jessica-wallace-agent-card")


if __name__ == "__main__":
    main()

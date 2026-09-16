#!/usr/bin/env python3
"""Build the 'Meet the Agents' contact card slide for Harcourts Property Hub
(Talei Kelly + Jessica Wallace). Headshots are placeholder initial-badges
until real photos are supplied — add "photo": Path(...) to an agent dict
below and rerun.

    python3 build_agent_card.py
"""

from agent_card_common import build

AGENTS = [
    {"name": "Talei Kelly", "phone": "0421 496 150"},
    {"name": "Jessica Wallace", "phone": "0422 962 688"},
]


def main():
    build(AGENTS, "meet-the-agents")


if __name__ == "__main__":
    main()

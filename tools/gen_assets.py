#!/usr/bin/env python3
"""Rebuild every hand-written pixel-art asset used by README.md.

    python tools/gen_assets.py

Nothing here talks to the network or needs a web font. Text is drawn as merged
<rect> runs from the 5x7 bitmap font in pixelfont.py, so the art is identical
on every renderer and stays crisp at any zoom. To re-skin the whole profile,
edit the nine hex values in tools/kit.py and run this again.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gen_desk
import gen_hero
import gen_parts
import kit


def main():
    os.makedirs(kit.OUT, exist_ok=True)
    print("writing assets to %s\n" % kit.OUT)
    kit.write("hero.svg", gen_hero.build())
    for name, body in gen_parts.all_parts():
        kit.write(name, body)
    for name, body in gen_parts.all_tags():
        kit.write(name, body)
    name, body = gen_desk.build()
    kit.write(name, body)
    print("\ndone.")


if __name__ == "__main__":
    main()

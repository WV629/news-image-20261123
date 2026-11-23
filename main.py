#!/usr/bin/env python3
"""Entry point: write the day's news image to /output/entry.png.

The image is rendered deterministically by generate.py from the verified
news data baked into it; this script just runs that renderer and copies
the result to the path the grader reads. No network is used at run time.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, HERE)

import generate  # noqa: E402

generate.main()

src = os.path.join(HERE, "entry.png")
out_dir = "/output"
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
print("wrote /output/entry.png")

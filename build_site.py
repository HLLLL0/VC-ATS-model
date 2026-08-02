#!/usr/bin/env python3
"""
Rebuild index.html (the public Vercel site) from source files:
  data.json -> gen_data.py -> data_array.js
  head.html + data_array.js + vcjobs.js.txt + freshfunds.js.txt + tail.html -> index.html

Run this after editing data.json, vcjobs.js.txt, or freshfunds.js.txt.
Strips the Cowork-artifact-only <script id="cowork-artifact-meta"> block since
it's meaningless (and slightly confusing) on the public site.
"""
import re
import subprocess
import sys

subprocess.run([sys.executable, "gen_data.py"], check=True)

head = open("head.html", encoding="utf-8").read()
data_array = open("data_array.js", encoding="utf-8").read()
vcjobs = open("vcjobs.js.txt", encoding="utf-8").read()
freshfunds = open("freshfunds.js.txt", encoding="utf-8").read()
tail = open("tail.html", encoding="utf-8").read()

marker = "const DATA = ["
idx = head.rfind(marker)
if idx == -1:
    raise SystemExit("head.html: couldn't find 'const DATA = [' marker")
head_trimmed = head[:idx]
head_trimmed = re.sub(
    r'<!DOCTYPE html><script type="application/json" id="cowork-artifact-meta">.*?</script>\n',
    "<!DOCTYPE html>\n",
    head_trimmed,
    flags=re.S,
)

combined = (
    head_trimmed.rstrip()
    + "\n\n"
    + data_array.strip()
    + "\n\n"
    + vcjobs.strip()
    + "\n\n"
    + freshfunds.strip()
    + "\n\n"
    + tail.lstrip()
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(combined)

n_companies = data_array.count("apolloId:") + data_array.count("unverified:true")
print(f"wrote index.html ({len(combined)} chars, {n_companies} companies)")

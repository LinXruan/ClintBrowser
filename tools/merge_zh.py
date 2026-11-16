
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
AMP = chr(38)
zh = Path("app/src/main/res/values-zh/strings.xml")
src = Path("app/src/main/res/values/strings.xml")

def esc(v):
    return v.replace(AMP, AMP + "amp;").replace("<", AMP + "lt;").replace(">", AMP + "gt;")

m = {}
for el in ET.parse(zh).getroot():
    if el.tag == "string":
        m[el.get("name")] = "".join(el.itertext())
    elif el.tag == "plurals":
        for it in el:
            if it.get("quantity") == "other":
                m[el.get("name")] = "".join(it.itertext())

added = 0
for f in sys.argv[1:]:
    for line in Path(f).read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            k, v = line.split("\t", 1)
            m[k.strip()] = v
            added += 1

out = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
n = 0
for el in ET.parse(src).getroot():
    if el.tag not in ("string", "plurals"): continue
    if el.get("translatable", "true") == "false": continue
    name = el.get("name")
    if name not in m: continue
    val = esc(m[name])
    if el.tag == "string":
        out.append(f'    <string name="{name}">{val}</string>')
    else:
        out.append(f'    <plurals name="{name}">')
        out.append(f'        <item quantity="other">{val}</item>')
        out.append("    </plurals>")
    n += 1
out.append("</resources>")
zh.write_text("\n".join(out) + "\n", encoding="utf-8")
ET.parse(zh)
print("新增", added, "总条目", n)

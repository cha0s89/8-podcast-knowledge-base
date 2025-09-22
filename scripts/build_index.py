import os, json, re
from pathlib import Path
import frontmatter

ROOT = Path(__file__).resolve().parents[1]
EP_DIR = ROOT / "episodes"
OUT_DIR = ROOT / "build"
OUT_DIR.mkdir(exist_ok=True, parents=True)

def section(text, header):
    m = re.search(rf"(?im)^###\s*{re.escape(header)}\s*(.*?)(?=^###\s|\Z)", text, re.S)
    return (m.group(1).strip() if m else "")

episodes = []
for md in sorted(EP_DIR.glob("*.md")):
    post = frontmatter.load(md)
    meta = {k: post.get(k) for k in ["podcast","episode","title","guest","tags","status"]}
    episodes.append({
        **meta,
        "slug": md.stem,
        "key_takeaways_md": section(post.content, "Key Takeaways"),
        "steps_md": section(post.content, "Step-by-Step"),
    })

with open(OUT_DIR / "index.json", "w", encoding="utf-8") as f:
    json.dump({"count": len(episodes), "episodes": episodes}, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(episodes)} episodes to build/index.json")


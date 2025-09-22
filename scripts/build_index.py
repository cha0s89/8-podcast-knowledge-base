# scripts/build_index.py
import json, re
from pathlib import Path
import yaml  # PyYAML

ROOT = Path(__file__).resolve().parents[1]
EP_DIR = ROOT / "episodes"
OUT_DIR = ROOT / "build"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_front_matter(text: str):
    """Parse minimal YAML front matter delimited by '---'."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except Exception:
                meta = {}
            body = parts[2].lstrip("\n")
            return meta, body
    return {}, text

def section(body: str, header: str):
    m = re.search(rf"(?im)^###\s*{re.escape(header)}\s*(.*?)(?=^###\s|\Z)", body, re.S)
    return m.group(1).strip() if m else ""

episodes = []
for md in sorted(EP_DIR.glob("*.md")):
    text = md.read_text(encoding="utf-8", errors="ignore")
    meta, body = parse_front_matter(text)
    episodes.append({
        "podcast": meta.get("podcast"),
        "episode": meta.get("episode"),
        "title": meta.get("title"),
        "guest": meta.get("guest"),
        "tags": meta.get("tags"),
        "status": meta.get("status"),
        "slug": md.stem,
        "key_takeaways_md": section(body, "Key Takeaways"),
        "steps_md": section(body, "Step-by-Step"),
    })

(OUT_DIR / "index.json").write_text(
    json.dumps({"count": len(episodes), "episodes": episodes}, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"Wrote {len(episodes)} episodes to build/index.json")


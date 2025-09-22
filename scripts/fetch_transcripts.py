import csv
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources.csv"
OUT = ROOT / "transcripts"
OUT.mkdir(exist_ok=True, parents=True)

def save_md(slug, title, text):
    (OUT / f"{slug}.md").write_text(f"# {title}\n\n{text}\n", encoding="utf-8")

def clean(chunks):
    return "\n".join(c["text"].strip() for c in chunks if c["text"].strip())

with open(SRC, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        yt = (row.get("youtube_id") or "").strip()
        title = (row.get("title") or "").strip() or "Untitled"
        if not yt:
            continue
        slug = yt
        out = OUT / f"{slug}.md"
        if out.exists():
            continue
        try:
            t = YouTubeTranscriptApi.get_transcript(yt, languages=["en"])
            save_md(slug, title, clean(t))
            print("Saved", out)
        except (TranscriptsDisabled, NoTranscriptFound):
            print("No captions:", yt)


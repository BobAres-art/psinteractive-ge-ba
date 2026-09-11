import os
import re

TOPICS_DIR = "topics"
OUTPUT_FILE = "index.html"

def extract_title(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read(2048)  # Read top part of the file
            match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    return None

def build_index():
    entries = []
    
    if os.path.exists(TOPICS_DIR):
        for folder in sorted(os.listdir(TOPICS_DIR)):
            folder_path = os.path.join(TOPICS_DIR, folder)
            index_path = os.path.join(folder_path, "index.html")
            
            # Look for folders inside topics/ that have an index.html
            if os.path.isdir(folder_path) and os.path.isfile(index_path):
                title = extract_title(index_path) or folder.replace("-", " ").title()
                entries.append((folder, title))

    # Build the HTML cards
    cards = []
    for slug, title in entries:
        card = (
            f'    <a class="card" href="{TOPICS_DIR}/{slug}/">\n'
            f'      <strong>{title}</strong>\n'
            f'      <span>Path: {TOPICS_DIR}/{slug}/</span>\n'
            f'    </a>'
        )
        cards.append(card)

    links_html = "\n".join(cards)

    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Master Index — Grammar Lab</title>
  <style>
    :root {{
      --bg: #090e17;
      --card: #121c2d;
      --border: #2a3d5a;
      --accent: #f59e0b;
      --text: #f1f5f9;
      --muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: system-ui, -apple-system, sans-serif;
      padding: 32px 16px;
      max-width: 680px;
      margin: 0 auto;
    }}
    h1 {{ color: var(--accent); margin-bottom: 6px; font-size: 1.8rem; }}
    p {{ color: var(--muted); margin-bottom: 24px; }}
    .list {{ display: grid; gap: 12px; }}
    .card {{
      display: block;
      background: var(--card);
      border: 1px solid var(--border);
      padding: 16px 20px;
      border-radius: 8px;
      color: var(--text);
      text-decoration: none;
      transition: border-color 0.2s, transform 0.2s;
    }}
    .card:hover {{
      border-color: var(--accent);
      transform: translateX(4px);
    }}
    .card strong {{ display: block; font-size: 1.05rem; }}
    .card span {{
      display: block;
      font-weight: normal;
      font-size: 0.8rem;
      color: var(--muted);
      margin-top: 4px;
    }}
  </style>
</head>
<body>
  <h1>Master Practice Index</h1>
  <p>All available interactive grammar modules.</p>
  <div class="list">
{links_html}
  </div>
</body>
</html>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(template)

if __name__ == "__main__":
    build_index()

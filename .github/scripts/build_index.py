import os
import re
import json

TOPICS_DIR = "topics"
STUDENTS_FILE = "students.json"
MASTER_FILE = "index.html"

def extract_title(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read(2048)
            match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
            if match:
                raw_title = match.group(1).strip()
                return re.sub(r"&amp;", "&", raw_title)
    except Exception as e:
        print(f"Warning reading {html_path}: {e}")
    return None

def scan_topics():
    topics = {}
    print(f"Checking for directory: {os.path.abspath(TOPICS_DIR)}")
    if os.path.exists(TOPICS_DIR):
        for folder in sorted(os.listdir(TOPICS_DIR)):
            folder_path = os.path.join(TOPICS_DIR, folder)
            index_path = os.path.join(folder_path, "index.html")
            if os.path.isdir(folder_path) and os.path.isfile(index_path):
                title = extract_title(index_path) or folder.replace("-", " ").title()
                topics[folder] = title
                print(f"  [Found Topic] {folder} -> '{title}'")
    else:
        print(f"Warning: '{TOPICS_DIR}' directory does not exist.")
    return topics

def render_page(badge_label, heading, description, cards_data):
    cards_html = ""
    for idx, (slug, title) in enumerate(cards_data, start=1):
        num_str = f"{idx:02d}"
        cards_html += f"""
      <a class="exercise-card" href="{TOPICS_DIR}/{slug}/">
        <div class="card-meta">
          <span class="card-num">{num_str}</span>
          <span class="card-tag">Practice Lab</span>
        </div>
        <div class="card-body">
          <h3 class="card-title">{title}</h3>
          <span class="card-slug">/{slug}/</span>
        </div>
        <div class="card-arrow" aria-hidden="true">&rarr;</div>
      </a>"""

    if not cards_data:
        cards_html = '<div class="empty-state">No practice sheets currently assigned to this track.</div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{heading} &bull; Language Labs</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #f8fafc;
      --surface: #ffffff;
      --surface-hover: #f1f5f9;
      --border: #e2e8f0;
      --border-focus: #cbd5e1;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-subtle: #94a3b8;
      --brand-indigo: #4338ca;
      --brand-indigo-light: #eef2ff;
      --brand-amber: #d97706;
      --brand-amber-light: #fef3c7;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.04);
      --shadow-md: 0 8px 24px -4px rgba(15, 23, 42, 0.06), 0 2px 6px -1px rgba(15, 23, 42, 0.04);
      --radius-lg: 16px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding: 48px 20px 24px;
      -webkit-font-smoothing: antialiased;
    }}
    .container {{ max-width: 740px; width: 100%; margin: 0 auto; flex: 1; }}
    header {{ margin-bottom: 36px; }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      background: var(--brand-indigo-light);
      color: var(--brand-indigo);
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      border-radius: 999px;
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 2.15rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text-main);
      line-height: 1.15;
      margin-bottom: 10px;
    }}
    header p {{ font-size: 1.02rem; color: var(--text-muted); line-height: 1.5; }}
    .card-grid {{ display: flex; flex-direction: column; gap: 12px; }}
    .exercise-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 20px 24px;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 20px;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .exercise-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--border-focus);
      background: #ffffff;
    }}
    .card-meta {{ display: flex; flex-direction: column; align-items: center; min-width: 48px; }}
    .card-num {{ font-size: 1.25rem; font-weight: 800; color: var(--brand-indigo); letter-spacing: -0.04em; line-height: 1; }}
    .card-tag {{ font-size: 0.65rem; font-weight: 600; text-transform: uppercase; color: var(--text-subtle); margin-top: 4px; }}
    .card-body {{ flex: 1; }}
    .card-title {{ font-size: 1.08rem; font-weight: 700; color: var(--text-main); letter-spacing: -0.01em; line-height: 1.35; margin-bottom: 4px; }}
    .exercise-card:hover .card-title {{ color: var(--brand-indigo); }}
    .card-slug {{
      font-family: ui-monospace, monospace;
      font-size: 0.78rem;
      color: var(--text-muted);
      background: var(--bg);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid var(--border);
    }}
    .card-arrow {{ color: var(--text-subtle); font-size: 1.25rem; font-weight: 600; transition: all 0.2s ease; padding-left: 6px; }}
    .exercise-card:hover .card-arrow {{ color: var(--brand-amber); transform: translateX(4px); }}
    .empty-state {{ padding: 40px; text-align: center; background: var(--surface); border: 1px dashed var(--border); border-radius: var(--radius-lg); color: var(--text-muted); font-size: 0.95rem; }}
    footer {{ margin-top: 56px; text-align: center; border-top: 1px solid var(--border); padding-top: 20px; }}
    .credit {{ font-size: 0.72rem; letter-spacing: 0.04em; color: #cbd5e1; text-transform: uppercase; font-weight: 500; user-select: none; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">{badge_label}</span>
      <h1>{heading}</h1>
      <p>{description}</p>
    </header>
    <main class="card-grid">
{cards_html}
    </main>
    <footer>
      <p class="credit">Designed by Babak Alaee</p>
    </footer>
  </div>
</body>
</html>
"""

def main():
    print(f"Current working directory: {os.getcwd()}")
    all_topics = scan_topics()

    # 1. Master Index
    master_cards = [(slug, all_topics[slug]) for slug in sorted(all_topics.keys())]
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        f.write(render_page("Curriculum Catalog", "Master Grammar Index", "Interactive analysis modules, applied diagnostics, and communicative drills.", master_cards))
    print(f"-> Generated {MASTER_FILE} with {len(master_cards)} topics.")

    # 2. Student Indices
    if not os.path.exists(STUDENTS_FILE):
        print(f"ERROR: Could not find '{STUDENTS_FILE}' at {os.path.abspath(STUDENTS_FILE)}")
        return

    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        students_data = json.load(f)

    print(f"-> Found {len(students_data)} entries in {STUDENTS_FILE}: {list(students_data.keys())}")

    for student_id, info in students_data.items():
        display_name = info.get("name", student_id.title())
        assigned_slugs = info.get("topics", [])
        student_cards = [
            (slug, all_topics.get(slug, slug.replace("-", " ").title()))
            for slug in assigned_slugs
        ]
        
        output_filename = f"{student_id}.html"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(render_page(
                f"Assigned Focus: {display_name}",
                f"{display_name}'s Portal",
                "Selected grammar structures and interactive case studies for your syllabus.",
                student_cards
            ))
        print(f"-> Successfully created {output_filename} ({len(student_cards)} items)")

if __name__ == "__main__":
    main()

"""Build a static, browser-only version of SAATHI AI for GitHub Pages.

The Streamlit app is packaged with stlite (Streamlit compiled to WebAssembly)
into docs/index.html. Run from the repository root:

    python3 scripts/build_pages.py

The Groq AI feature is replaced with a placeholder in this build so that no
API key is ever shipped to a public web page.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
STLITE_VERSION = "0.75.0"

AI_STUB = '''"""Browser-only build: the live AI service is not available on GitHub Pages."""


def generate_student_insight(student_data):
    return (
        "AI insights are available in the full SAATHI AI deployment. "
        "This static preview does not include the AI service key."
    )
'''

SKIP_PY = {"ai_engine.py"}


def collect_files():
    files = {}
    for path in sorted(ROOT.glob("*.py")):
        if path.name in SKIP_PY:
            continue
        files[path.name] = path.read_text(encoding="utf-8")
    for path in sorted(ROOT.glob("*.csv")):
        files[path.name] = path.read_text(encoding="utf-8")
    files["ai_engine.py"] = AI_STUB
    return files


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SAATHI AI | Student Success</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@__VERSION__/build/stlite.css" />
  <script type="module" src="https://cdn.jsdelivr.net/npm/@stlite/mountable@__VERSION__/build/stlite.js"></script>
  <style>
    html, body { margin: 0; padding: 0; height: 100%; }
    #root { height: 100vh; width: 100vw; }
    #loading { font-family: Arial, sans-serif; padding: 2rem; color: #333; }
  </style>
</head>
<body>
  <div id="root"><p id="loading">Loading SAATHI AI... the first load can take up to a minute.</p></div>
  <script>
    window.addEventListener("load", function () {
      var config = {
        requirements: ["pandas", "numpy", "plotly"],
        entrypoint: "app.py",
        files: __FILES__
      };
      var attempts = 0;
      (function tryMount() {
        if (window.stlite && window.stlite.mount) {
          window.stlite.mount(config, document.getElementById("root"));
        } else if (attempts++ < 200) {
          setTimeout(tryMount, 100);
        } else {
          document.getElementById("loading").textContent =
            "SAATHI AI could not load. Please refresh the page.";
        }
      })();
    });
  </script>
</body>
</html>
"""


def build():
    files = collect_files()
    # Escape "<" so that file contents can never terminate the inline script.
    files_json = json.dumps(files, ensure_ascii=False).replace("<", "\\u003c")
    html = HTML.replace("__VERSION__", STLITE_VERSION).replace("__FILES__", files_json)
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Wrote {DOCS / 'index.html'} with {len(files)} files")


if __name__ == "__main__":
    build()

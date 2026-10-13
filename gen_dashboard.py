"""Render results/ progress into a single HTML dashboard (stdout or --out)."""
import json
import sys
from datetime import datetime
from pathlib import Path

TOTAL_TASKS = 102
RESULTS = Path("results")


def read_models():
    return [l.strip() for l in open("models.txt") if l.strip() and not l.startswith("#")]


def log_path(model):
    return RESULTS / model.replace("/", "__") / "science_agent.jsonl"


def model_stats(model):
    path = log_path(model)
    if not path.exists():
        return {"model": model, "done": 0, "programs": 0, "empty": 0}
    rows = [json.loads(l) for l in open(path) if l.strip()]
    programs = len(list((path.parent / "pred_programs").glob("*.py")))
    empty = sum(1 for r in rows if not any(m["role"] == "assistant" for m in r["history"]))
    return {"model": model, "done": len(rows), "programs": programs, "empty": empty}


def status_of(s):
    if s["done"] >= TOTAL_TASKS:
        return "done", "Complete"
    if s["done"] == 0:
        return "idle", "Not started"
    return "run", "Running"


def render_row(s):
    pct = 100 * s["done"] / TOTAL_TASKS
    cls, label = status_of(s)
    return f"""<tr>
<td class="m">{s['model']}</td>
<td><span class="pill {cls}">{label}</span></td>
<td class="n">{s['done']} / {TOTAL_TASKS}</td>
<td class="n">{s['programs']}</td>
<td class="bar"><div class="track"><div class="fill {cls}" style="width:{pct:.1f}%"></div></div><span class="pct">{pct:.0f}%</span></td>
</tr>"""


def render(stats, now):
    done_tasks = sum(s["done"] for s in stats)
    finished = sum(1 for s in stats if s["done"] >= TOTAL_TASKS)
    rows = "\n".join(render_row(s) for s in sorted(stats, key=lambda s: -s["done"]))
    return TEMPLATE.format(now=now, rows=rows, done_tasks=done_tasks,
                           total=TOTAL_TASKS * len(stats), finished=finished, n=len(stats))


TEMPLATE = """<title>ScienceAgentBench on RiVault</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: one summary strip, one table; lab-notebook register, cool slate neutrals, teal accent */
:root {{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#1c2430; --muted:#5d6a7a; --line:#d9dee5;
  --accent:#0f766e; --run:#0f766e; --done:#2563eb; --idle:#9aa5b3;
  --sans:'IBM Plex Sans',system-ui,sans-serif; --mono:'IBM Plex Mono',ui-monospace,monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  color-scheme:dark; --bg:#141a21; --panel:#1b232c; --ink:#e6ebf0; --muted:#9aa7b5; --line:#2c3845;
  --accent:#2dd4bf; --run:#2dd4bf; --done:#60a5fa; --idle:#55626f; }} }}
:root[data-theme="dark"] {{
  color-scheme:dark; --bg:#141a21; --panel:#1b232c; --ink:#e6ebf0; --muted:#9aa7b5; --line:#2c3845;
  --accent:#2dd4bf; --run:#2dd4bf; --done:#60a5fa; --idle:#55626f; }}
body {{ background:var(--bg); color:var(--ink); font-family:var(--sans); padding:0 20px; padding-block:32px; }}
main {{ max-width:960px; margin:0 auto; display:grid; gap:24px; }}
h1 {{ font-size:1.6rem; font-weight:600; margin:0; text-wrap:balance; }}
.sub {{ color:var(--muted); font-size:.9rem; margin-top:6px; font-family:var(--mono); }}
.strip {{ display:flex; flex-wrap:wrap; gap:12px; }}
.stat {{ flex:1 1 160px; background:var(--panel); border:1px solid var(--line); padding:12px 16px; }}
.stat b {{ display:block; font-size:1.5rem; font-weight:600; font-variant-numeric:tabular-nums; }}
.stat span {{ font-size:.75rem; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); }}
.wrap {{ overflow-x:auto; background:var(--panel); border:1px solid var(--line); }}
table {{ border-collapse:collapse; width:100%; font-size:.9rem; }}
th {{ text-align:left; font-size:.72rem; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); padding:10px 12px; border-bottom:1px solid var(--line); }}
td {{ padding:9px 12px; border-bottom:1px solid var(--line); vertical-align:middle; }}
tr:last-child td {{ border-bottom:0; }}
.m {{ font-family:var(--mono); font-size:.85rem; }}
.n {{ font-variant-numeric:tabular-nums; text-align:right; white-space:nowrap; }}
.bar {{ min-width:180px; }}
.track {{ height:8px; background:var(--line); display:inline-block; width:calc(100% - 44px); vertical-align:middle; }}
.fill {{ height:100%; background:var(--run); }}
.fill.done {{ background:var(--done); }}
.pct {{ font-family:var(--mono); font-size:.8rem; margin-left:8px; color:var(--muted); }}
.pill {{ font-size:.72rem; padding:2px 8px; border:1px solid currentColor; border-radius:999px; white-space:nowrap; }}
.pill.run {{ color:var(--run); }} .pill.done {{ color:var(--done); }} .pill.idle {{ color:var(--idle); }}
.note {{ color:var(--muted); font-size:.85rem; max-width:65ch; }}
</style>
<main>
<header><h1>ScienceAgentBench on RiVault</h1>
<div class="sub">inference progress · updated {now}</div></header>
<div class="strip">
<div class="stat"><b>{done_tasks} / {total}</b><span>task runs finished</span></div>
<div class="stat"><b>{finished} / {n}</b><span>models complete</span></div>
<div class="stat"><b>{n}</b><span>models in models.txt</span></div>
</div>
<div class="wrap"><table>
<thead><tr><th>Model</th><th>Status</th><th>Tasks</th><th>Programs</th><th>Progress</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="note">Each model solves the 102 verified ScienceAgentBench tasks once, without self-debug or domain knowledge. "Programs" counts extracted pred_*.py files. Evaluation (success rate, CodeBERTScore, valid execution rate) is not started yet.</p>
</main>
"""

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = render([model_stats(m) for m in read_models()], now)
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    (open(out, "w").write(html) if out else print(html))

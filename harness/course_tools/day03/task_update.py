"""Update one ordered course step; preserve earlier evidence and other claims."""
import argparse
import re
from datetime import date
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("tracker", type=Path)
p.add_argument("task")
p.add_argument("step", type=int)
p.add_argument("state", choices=["in_progress", "done", "blocked", "not_applicable"])
p.add_argument("evidence")
a = p.parse_args()
s = a.tracker.read_text(encoding="utf-8-sig")
pattern = rf'(^#{{2,3}} {re.escape(a.task)} — [^\n]*\n.*?)(?=^#{{2,3}} |^<a id=|\Z)'
m = re.search(pattern, s, re.S | re.M)
if not m:
    raise SystemExit("Task missing")
b = m.group(1)
row = re.compile(rf'(?m)^\| {a.step} \| (.*?) \| (not_started|in_progress|done|blocked|not_applicable) \| (.*?) \|$')
old = row.search(b)
if not old:
    raise SystemExit("Step missing")
previous = re.findall(r'(?m)^\| (\d+) \| .*? \| (not_started|in_progress|done|blocked|not_applicable) \|', b)
if any(int(n) < a.step and st not in ("done", "not_applicable") for n, st in previous):
    raise SystemExit("Unfinished prerequisite step")
if a.state in ("done", "blocked") and old.group(2) != "in_progress":
    raise SystemExit("Claim step first")
ev = a.evidence.replace("|", " / ")
b = row.sub(lambda z: f'| {a.step} | {z.group(1)} | {a.state} | {ev} |', b, count=1)
states = re.findall(r'(?m)^\| (\d+) \| .*? \| (not_started|in_progress|done|blocked|not_applicable) \|', b)
unfinished = [(n, st) for n, st in states if st not in ("done", "not_applicable")]
status = "done" if not unfinished else "blocked" if a.state == "blocked" else "in_progress"
next_step = unfinished[0][0] if unfinished else "None"
owner = "unassigned" if status == "done" else "current automation chat"
b = re.sub(r'Status: `.*?` · Owner: `.*?` · Updated: .*? · Next step: .*?\n', f'Status: `{status}` · Owner: `{owner}` · Updated: {date.today().isoformat()} · Next step: {next_step}\n', b, count=1)
s = s[:m.start()] + b + s[m.end():]
s = re.sub(rf'(?m)^(\| \[{re.escape(a.task)} — .*?\| .*? \| )\w+( \| ).*?( \|)$', rf'\g<1>{status}\g<2>{next_step}\g<3>', s)
a.tracker.write_text(s, encoding="utf-8")
print(f"{a.task} step {a.step}: {a.state}; task {status}; next {next_step}")

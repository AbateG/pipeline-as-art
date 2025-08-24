# scripts/extract_timeline.py
# Parses conventional commits into event records with type, impact, and lesson
import subprocess, json, re, datetime

TYPES = {"feat":"Feature","fix":"Fix","docs":"Docs","refactor":"Refactor","perf":"Performance"}

def parse():
    log = subprocess.check_output(["git","log","--pretty=%H|%ad|%s","--date=iso"]).decode()
    events = []
    for line in log.splitlines():
        sha, date, msg = line.split("|", 2)
        m = re.match(r"(\w+)(\(.+\))?:\s(.+)", msg)
        t = TYPES.get(m.group(1), "Change") if m else "Change"
        events.append({
            "sha": sha[:7],
            "date": date,
            "type": t,
            "summary": m.group(3) if m else msg,
            "lesson": infer_lesson(msg)
        })
    print(json.dumps(events, indent=2))

def infer_lesson(msg):
    if "health" in msg: return "Healthchecks prevent silent failures."
    if "docker" in msg: return "Build context and layers matter."
    if "schema" in msg: return "Contracts are living documents."
    return "Iteration uncovers clarity."

if __name__ == "__main__":
    parse()

from datetime import date
from collections import defaultdict

DEFAULT_WEIGHTS = {
    'urgency': 0.4,
    'importance': 0.3,
    'effort': 0.2,
    'dependency': 0.1,
}

MODE_PRESETS = {
    'fastest': {'urgency':0.2,'importance':0.2,'effort':0.6,'dependency':0.0},
    'high_impact': {'urgency':0.2,'importance':0.7,'effort':0.1,'dependency':0.0},
    'deadline': {'urgency':0.7,'importance':0.2,'effort':0.1,'dependency':0.0},
    'smart': DEFAULT_WEIGHTS
}

def compute_days_remaining(due_date):
    if due_date is None:
        return None
    today = date.today()
    return (due_date - today).days

def urgency_score(days_remaining):
    if days_remaining is None:
        return 3
    if days_remaining < 0:
        return 10
    score = max(0.0, 10.0 * (1 - (days_remaining / 30.0)))
    return min(10.0, score)

def effort_score(hours):
    if hours <= 0:
        return 10
    return min(10.0, 10 / hours)

def dependency_score(task_id, tasks):
    count = sum(task_id in t.get("dependencies", []) for t in tasks)
    return min(10.0, count * 2)

def analyze_tasks(data, mode="smart"):
    weights = MODE_PRESETS.get(mode, DEFAULT_WEIGHTS)
    results = []

    for task in data:
        days = None
        if task.get("due_date"):
            from datetime import datetime
            days = compute_days_remaining(datetime.strptime(task["due_date"], "%Y-%m-%d").date())

        u = urgency_score(days)
        i = task.get("importance", 5)
        e = effort_score(task.get("estimated_hours", 1.0))
        d = dependency_score(task.get("id") or task["title"], data)

        score = (u * weights['urgency']) + (i * weights['importance']) + (e * weights['effort']) + (d * weights['dependency'])
        score = round(score * 10, 2)

        results.append({
            **task,
            "score": score,
            "reason": f"urgency={u}, importance={i}, effort={e}, dependency={d}"
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def suggest_top_3(data, mode="smart"):
    ranked = analyze_tasks(data, mode)
    return ranked[:3]

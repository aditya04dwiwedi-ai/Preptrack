"""
Endpoint + data-integrity checks for the Placement Preparation & Tracking System.
Run:  python test_api.py
Uses Flask's built-in test client, so the server does not need to be running.
"""
import collections
import sys

import app as backend
import datasets as ds

client = backend.app.test_client()
results = []


def check(name, condition, detail=""):
    results.append((name, bool(condition), detail))


def get(url):
    r = client.get(url)
    return r.status_code, (r.get_json(silent=True) or {})


def send(method, url, body=None):
    r = getattr(client, method)(url, json=body)
    return r.status_code, (r.get_json(silent=True) or {})


# ---------------------------------------------------------------- reset first
code, j = send("post", "/api/reset")
check("POST /api/reset", code == 200 and j.get("success"))

# ---------------------------------------------------------------- existing endpoints
r = client.get("/")
check("GET /  (dashboard page)", r.status_code == 200)

code, j = get("/api/data")
need = {"student", "subjects", "summary", "companies", "goals", "test_history", "sample_students",
        "suggestions", "suggestion_metrics", "progress_history", "activity_summary", "achievements"}
check("GET /api/data  (old + new keys)", code == 200 and need <= set(j), f"missing={need - set(j)}")
check("/api/data summary unchanged (score 52, Good)", j["summary"]["overall_score"] == 52 and j["summary"]["status"] == "Good")
check("/api/data weak areas = DSA, Aptitude", [w["subject"] for w in j["summary"]["weak_areas"]] == ["DSA", "Aptitude"])
check("pipeline has 8 rows, original 4 first", len(j["companies"]) == 8 and [c["company"] for c in j["companies"][:4]] == ["TCS", "Infosys", "Wipro", "Amazon"])
statuses = {c["status"] for c in j["companies"]}
check("pipeline covers all 6 statuses", statuses == {"Interested", "Applied", "Shortlisted", "Interview", "Selected", "Rejected"}, str(sorted(statuses)))
check("8 goals, first 4 text unchanged", len(j["goals"]) == 8 and j["goals"][0]["text"] == "Practice 10 Python coding problems"
      and j["goals"][1]["text"].startswith("Revise DBMS Normalization"))
check("every goal has category + priority", all("category" in g and "priority" in g for g in j["goals"]))
check("15 sample students", len(j["sample_students"]) == 15)
check("seeded test history has 6 attempts, newest 4/5 (80%)",
      len(j["test_history"]) == 6 and j["test_history"][0]["score"] == 4 and j["test_history"][0]["percentage"] == 80)

code, j = get("/api/suggestions")
sug = j.get("suggestions", [])
labels = collections.Counter(s["status_label"] for s in sug)
check("GET /api/suggestions  (13 companies)", code == 200 and len(sug) == 13, f"count={len(sug)}")
check("suggestions mix Eligible / Near / Target", labels["Eligible Match"] > 0 and labels["Near Match (Minor Gap)"] > 0 and labels["Target Aspirations"] > 0, dict(labels))
badge_ok = {"primary", "secondary", "success", "danger", "warning", "info", "light", "dark"}
check("company badge colours are valid Bootstrap colours", all(c["badge_color"] in badge_ok for c in backend.COMPANY_SUGGESTIONS_DATA))
tiers = {c["tier"] for c in backend.COMPANY_SUGGESTIONS_DATA}
check("company tiers cover product / IT / AI-ML / fintech / edtech / consulting",
      all(any(k in t for t in tiers) for k in ("Product", "IT", "AI/ML", "Fintech", "EdTech", "Consulting")), str(sorted(tiers)))

code, j = send("post", "/api/profile", {"name": "Test User", "cgpa": 8.5})
check("POST /api/profile", code == 200 and j["student"]["name"] == "Test User")
code, j = send("post", "/api/subjects", {"Python": 80})
check("POST /api/subjects", code == 200 and j["subjects"]["Python"] == 80)

code, j = send("post", "/api/companies", {"company": "TestCo", "role": "Dev", "status": "Applied"})
cid = j.get("company", {}).get("id")
check("POST /api/companies", code == 200 and cid)
code, j = send("put", f"/api/companies/{cid}", {"status": "Interview"})
check("PUT /api/companies/<id>", code == 200 and j["company"]["status"] == "Interview")
code, j = send("delete", f"/api/companies/{cid}")
check("DELETE /api/companies/<id>", code == 200)
code, j = send("post", "/api/companies", {"company": "", "role": ""})
check("POST /api/companies rejects empty input (400)", code == 400)

code, j = send("post", "/api/goals", {"text": "Test goal"})
gid = j.get("goal", {}).get("id")
check("POST /api/goals", code == 200 and gid)
code, j = send("put", f"/api/goals/{gid}", {"completed": True})
check("PUT /api/goals/<id>", code == 200 and j["goal"]["completed"] is True)
code, j = send("delete", f"/api/goals/{gid}")
check("DELETE /api/goals/<id>", code == 200)

code, j = get("/api/sample-students")
check("GET /api/sample-students", code == 200 and len(j["sample_students"]) == 15)
code, j = send("post", "/api/sample-students/load/6")
check("POST /api/sample-students/load/<id>", code == 200 and j["student"]["name"] == "Neha Kapoor")
code, j = send("post", "/api/sample-students/load/999")
check("load unknown student -> 404", code == 404)

# ---------------------------------------------------------------- mock test
code, j = get("/api/mock-test")
ids1 = [q["id"] for q in j["questions"]]
code2, j2 = get("/api/mock-test?category=Synopsis&count=5")
ids2 = [q["id"] for q in j2["questions"]]
check("Synopsis test: same 5 questions, same order, every time",
      ids1 == ids2 == ["syn_html", "syn_fifo", "syn_py_comment", "syn_sql", "syn_lifo"], str(ids1))
check("answer keys never exposed", all("answer" not in q and "explanation" not in q for q in j["questions"]))
check("questions carry difficulty", all(q.get("difficulty") in ("Easy", "Medium", "Hard") for q in j["questions"]))

for cat in ["Python", "C", "DSA", "DBMS", "Aptitude", "OOP", "Operating Systems", "Computer Networks", "Logical Reasoning", "All"]:
    code, j = get(f"/api/mock-test?category={cat.replace(' ', '%20')}&count=10")
    check(f"GET /api/mock-test category={cat} count=10", code == 200 and len(j["questions"]) == 10, f"got={len(j.get('questions', []))}")
code, j = get("/api/mock-test?category=Python&count=15")
check("count=15 returns 15 for Python", code == 200 and len(j["questions"]) == 15)
code, j = get("/api/mock-test?category=OOP&count=15")
check("count capped at bank size (OOP has 10)", code == 200 and len(j["questions"]) == 10)
runs = {tuple(q["id"] for q in get("/api/mock-test?category=DSA&count=5")[1]["questions"]) for _ in range(8)}
check("non-Synopsis categories are randomised", len(runs) > 1, f"{len(runs)} distinct orderings in 8 calls")
code, j = get("/api/mock-test?category=Python&count=10&difficulty=Hard")
check("difficulty filter works", code == 200 and all(q["difficulty"] == "Hard" for q in j["questions"]) and len(j["questions"]) == 3, f"n={len(j.get('questions', []))}")
check("bad count -> 400", get("/api/mock-test?count=7")[0] == 400 and get("/api/mock-test?count=abc")[0] == 400)
check("bad difficulty -> 400", get("/api/mock-test?difficulty=Insane")[0] == 400)
check("unknown category -> 400", get("/api/mock-test?category=Nope")[0] == 400)

# submit: every question in every bank must score correct with its own answer key
all_ids = {}
for bank in backend._all_question_banks():
    for q in bank:
        all_ids[q["id"]] = q
code, j = send("post", "/api/mock-test/submit", {"answers": {i: q["answer"] for i, q in all_ids.items()}, "category": "All"})
check("submit covers every bank: perfect answers -> 100%", code == 200 and j["percentage"] == 100 and j["total"] == len(all_ids), f"{j.get('score')}/{j.get('total')}")
served = ["syn_html", "syn_fifo", "syn_py_comment", "syn_sql", "syn_lifo"]
code, j = send("post", "/api/mock-test/submit", {"answers": {"syn_fifo": 1}, "question_ids": served, "category": "Synopsis"})
check("submit with question_ids counts skipped as wrong (1/5)", code == 200 and j["score"] == 1 and j["total"] == 5)
code, j = send("post", "/api/mock-test/submit", {"answers": {"syn_fifo": 1}})
check("submit (old frontend style, answers only)", code == 200 and j["total"] == 1)
check("submit bad answers type -> 400", send("post", "/api/mock-test/submit", {"answers": [1, 2]})[0] == 400)
check("submit unknown ids -> 400", send("post", "/api/mock-test/submit", {"answers": {"zzz": 1}})[0] == 400)

# ---------------------------------------------------------------- new endpoints
send("post", "/api/reset")
code, j = get("/api/leaderboard")
lb = j.get("leaderboard", [])
ranks = [r["rank"] for r in lb]
check("GET /api/leaderboard", code == 200 and len(lb) == 15 and ranks == sorted(ranks) and sum(r["is_active"] for r in lb) == 1,
      f"rows={len(lb)}")
check("leaderboard rows have required fields", all({"rank", "name", "branch", "overall_score", "status"} <= set(r) for r in lb))
check("active student not duplicated", sum(1 for r in lb if r["name"] == "Aditya Dwivedi") == 1)

code, j = get("/api/progress-history")
h = j.get("history", [])
check("GET /api/progress-history (8 snapshots)", code == 200 and len(h) == 8)
check("history ends exactly at DEFAULT_SUBJECTS", h[-1]["subjects"] == backend.DEFAULT_SUBJECTS, str(h[-1]["subjects"]))
check("history shows growth for every subject", all(h[0]["subjects"][s] < h[-1]["subjects"][s] for s in backend.DEFAULT_SUBJECTS))

code, j = get("/api/activity")
log = j.get("log", [])
check("GET /api/activity (84 days)", code == 200 and len(log) == 84)
check("activity has zero days and active days", any(e["problems_solved"] == 0 for e in log) and any(e["problems_solved"] > 0 for e in log))
check("activity has streak fields + totals", {"current_streak", "longest_streak", "total_problems_solved", "total_minutes_studied"} <= set(j))
check("current streak = 6 (demo design)", j["current_streak"] == 6, f"streak={j.get('current_streak')}, longest={j.get('longest_streak')}")
check("activity is deterministic", get("/api/activity")[1]["log"] == log)

code, j = get("/api/topics")
tp = j.get("topics", {})
check("GET /api/topics (5 subjects x 9 topics)", code == 200 and set(tp) == set(backend.DEFAULT_SUBJECTS) and all(len(v) == 9 for v in tp.values()))
check("GET /api/topics?subject=dsa (case-insensitive)", get("/api/topics?subject=dsa")[0] == 200)
check("GET /api/topics bad subject -> 400", get("/api/topics?subject=Java")[0] == 400)
code, j = send("put", "/api/topics/DSA/dsa-7", {"status": "Completed"})
check("PUT /api/topics/<subject>/<id>", code == 200 and j["topic"]["status"] == "Completed" and j["progress"]["completed"] == 5)
check("PUT topic invalid status -> 400", send("put", "/api/topics/DSA/dsa-7", {"status": "Done"})[0] == 400)
check("PUT topic missing body -> 400", send("put", "/api/topics/DSA/dsa-7", {})[0] == 400)
check("PUT topic unknown id -> 404", send("put", "/api/topics/DSA/nope", {"status": "Completed"})[0] == 404)
check("PUT topic unknown subject -> 404", send("put", "/api/topics/Java/x", {"status": "Completed"})[0] == 404)

code, j = get("/api/resources")
res = j.get("resources", {})
check("GET /api/resources (5-6 per subject)", code == 200 and all(5 <= len(v) <= 6 for v in res.values()) and set(res) == set(backend.DEFAULT_SUBJECTS))
check("resource types valid", all(r["type"] in ("Video", "Article", "Practice", "Course") for v in res.values() for r in v))
check("resource URLs are https and on approved sites", all(r["url"].startswith("https://") and any(d in r["url"] for d in (
    "docs.python.org", "geeksforgeeks.org", "leetcode.com", "w3schools.com", "freecodecamp.org", "nptel.ac.in", "indiabix.com")) for v in res.values() for r in v))
check("GET /api/resources?subject=C", get("/api/resources?subject=C")[0] == 200)
check("GET /api/resources bad subject -> 400", get("/api/resources?subject=Go")[0] == 400)

code, j = get("/api/achievements")
ach = j.get("achievements", [])
check("GET /api/achievements (10 badges)", code == 200 and len(ach) == 10)
check("badges have unlocked + hint", all(isinstance(b["unlocked"], bool) and b["hint"] for b in ach))
check("default state: some unlocked, some locked", 0 < j["unlocked"] < 10, f"unlocked={j.get('unlocked')}")
send("post", "/api/subjects", {"Python": 90, "C": 90, "DSA": 90, "DBMS": 90, "Aptitude": 90})
a2 = {b["id"]: b["unlocked"] for b in get("/api/achievements")[1]["achievements"]}
check("achievements react to live state (No Weak Areas + Placement Ready)", a2["no_weak_areas"] and a2["placement_ready"] and a2["all_rounder"])

code, j = get("/api/interview-questions")
check("GET /api/interview-questions (25)", code == 200 and j["total"] == 25)
counts = collections.Counter(q["category"] for q in j["questions"])
check("interview categories HR / Technical / Behavioural all present", set(counts) == {"HR", "Technical", "Behavioural"}, dict(counts))
check("interview filter works", get("/api/interview-questions?category=hr")[1]["total"] == counts["HR"])
check("interview bad category -> 400", get("/api/interview-questions?category=Fun")[0] == 400)

code, j = get("/api/placement-stats")
check("GET /api/placement-stats (4 years)", code == 200 and len(j["stats"]) == 4 and all({"year", "offers", "average_ctc", "highest_ctc", "top_recruiters"} <= set(s) for s in j["stats"]))

# ---------------------------------------------------------------- reset restores everything
send("put", "/api/topics/Python/py-9", {"status": "Completed"})
send("post", "/api/mock-test/submit", {"answers": {"syn_fifo": 0}})
send("post", "/api/reset")
d = get("/api/data")[1]
check("reset restores test history (6) and baseline", len(d["test_history"]) == 6 and d["test_history"][0]["percentage"] == 80)
check("reset restores subjects/companies/goals", d["subjects"] == backend.DEFAULT_SUBJECTS and len(d["companies"]) == 8 and len(d["goals"]) == 8)
check("reset restores topic checklist", get("/api/topics")[1]["topics"]["Python"][8]["status"] == "Not Started")

# ---------------------------------------------------------------- dataset integrity
banks = {"Synopsis": backend.SYNOPSIS_MOCK_QUESTIONS, **backend.EXTENDED_QUESTION_BANK, **backend.QUIZ_ONLY_BANK}
all_q = [q for b in banks.values() for q in b]
unique = {q["id"]: q for q in all_q}
check("all question ids are unique", len(unique) == len({q['id'] for q in unique.values()}) and len(unique) == len(set(q["id"] for q in unique.values())))
texts = collections.Counter(q["question"].strip().lower() for q in unique.values())
check("no duplicate question text", max(texts.values()) == 1, str([t for t, n in texts.items() if n > 1]))
for sub in backend.DEFAULT_SUBJECTS:
    check(f"{sub} bank has >= 15 questions", len(backend.EXTENDED_QUESTION_BANK[sub]) >= 15, f"{len(backend.EXTENDED_QUESTION_BANK[sub])}")
for cat, qs in backend.QUIZ_ONLY_BANK.items():
    check(f"{cat} quiz-only bank has 10 questions", len(qs) == 10)
check("total distinct questions >= 115", len(unique) >= 115, f"{len(unique)}")
bad = [q["id"] for q in unique.values() if len(q["options"]) != 4 or len(set(q["options"])) != 4 or not (0 <= q["answer"] < 4)
       or q.get("difficulty") not in ("Easy", "Medium", "Hard") or not q.get("explanation") or not q.get("concept")]
check("every question: 4 distinct options, valid answer index, difficulty, concept, explanation", not bad, str(bad))
new_q = [q for b in list(ds.EXTRA_SUBJECT_QUESTIONS.values()) + list(ds.QUIZ_ONLY_QUESTIONS.values()) for q in b]
dist = collections.Counter(q["answer"] for q in new_q)
check("answer positions evenly spread (new questions)", max(dist.values()) - min(dist.values()) <= 2, str(sorted(dist.items())))
check("synopsis questions untouched (answers 0,1,2,2,1)", [q["answer"] for q in backend.SYNOPSIS_MOCK_QUESTIONS] == [0, 1, 2, 2, 1])
check("tracked subjects still exactly 5", list(backend.DEFAULT_SUBJECTS) == ["Python", "C", "DSA", "DBMS", "Aptitude"])
check("sample student ids unique 1-15", sorted(s["id"] for s in backend.SAMPLE_STUDENTS) == list(range(1, 16)))
bands = collections.Counter(backend.calculate_summary(s["subjects"])["status"] for s in backend.SAMPLE_STUDENTS)
check("students span all 3 readiness bands", len(bands) == 3, dict(bands))
check("student CGPA within 6.5-9.5", all(6.5 <= s["cgpa"] <= 9.5 for s in backend.SAMPLE_STUDENTS))
check("every student has the 4 new optional fields", all({"skills", "target_company", "city", "weekly_study_hours"} <= set(s) for s in backend.SAMPLE_STUDENTS))
branches = {s["branch"] for s in backend.SAMPLE_STUDENTS}
check("varied branches", len(branches) >= 6, str(sorted(branches)))

# ---------------------------------------------------------------- report
passed = sum(1 for _, ok, _ in results if ok)
for name, ok, detail in results:
    print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail and not ok else (f"   ({detail})" if detail and ok else "")))
print("-" * 70)
print(f"{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)

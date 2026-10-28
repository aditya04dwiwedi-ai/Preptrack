"""
Tests for the PrepBot chat routes. The AI provider is MOCKED, so no API key or internet is needed.
Run:  python test_chat.py
"""
import os
import sys

for k in ("GEMINI_API_KEY", "OPENAI_API_KEY", "AI_PROVIDER", "GEMINI_MODEL", "OPENAI_MODEL"):
    os.environ.pop(k, None)

import app as backend
import chatbot

client = backend.app.test_client()
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))


def chat(message="hello", **extra):
    chatbot._RATE_BUCKETS.clear()
    r = client.post("/api/chat", json={"message": message, **extra})
    return r.status_code, (r.get_json(silent=True) or {})


calls = []


def fake_post(url, payload, headers):
    calls.append((url, payload, headers))
    if "generativelanguage" in url:
        return {"candidates": [{"content": {"parts": [{"text": "Gemini says "}, {"text": "hi"}]}}]}
    return {"choices": [{"message": {"content": "OpenAI says hi"}}]}


real_post = chatbot._post_json
client.post("/api/reset")

# ---------------- no key: local demo mode ----------------
code, j = client.get("/api/chat/status").status_code, client.get("/api/chat/status").get_json()
check("status: not configured -> local", code == 200 and j["configured"] is False and j["provider"] == "local")
code, j = chat("Analyze my progress")
check("no key: progress answer from live data", code == 200 and j["source"] == "local"
      and "52%" in j["reply"] and "DSA" in j["reply"] and "Aptitude" in j["reply"], j.get("reply", "")[:80])
code, j = chat("Can you recommend videos for DSA?")
check("no key: video request gives [[yt: ...]] search chips", "[[yt:" in j["reply"] and "DSA" in j["reply"])
code, j = chat("recommend a tutorial")
check("no key: video request w/o subject targets weakest subject", "Aptitude" in j["reply"] or "DSA" in j["reply"])
code, j = chat("What is a pointer in C and why does it segfault?")
check("no key: doubt question explains demo mode", "demo mode" in j["reply"].lower())

# ---------------- Gemini path (mocked) ----------------
os.environ["GEMINI_API_KEY"] = "test-key-123"
chatbot._post_json = fake_post
check("status: configured -> gemini", client.get("/api/chat/status").get_json()["provider"] == "gemini")
calls.clear()
code, j = chat("Explain recursion", history=[
    {"role": "assistant", "text": "stray leading bot message"},
    {"role": "user", "text": "hi"}, {"role": "assistant", "text": "hello!"},
    {"role": "user", "text": "one"}, "garbage", {"role": "user", "text": "two"}])
url, payload, headers = calls[0]
check("gemini: reply returned, source=gemini, parts joined", code == 200 and j["source"] == "gemini" and j["reply"] == "Gemini says hi")
check("gemini: key sent as header, not in URL or response", headers.get("x-goog-api-key") == "test-key-123"
      and "test-key-123" not in url and "test-key-123" not in str(j))
check("gemini: model in URL", "models/gemini-flash-latest:generateContent" in url)
sys_text = payload["system_instruction"]["parts"][0]["text"]
check("gemini: system prompt carries live student data", "DSA 42%" in sys_text and "52%" in sys_text and "Needs Improvement" not in sys_text.split("Overall")[0])
check("gemini: weak areas + topic checklist in context", "Weak areas (<50%): DSA (42%), Aptitude (35%)" in sys_text and "Topic checklist" in sys_text)
roles = [c["role"] for c in payload["contents"]]
check("gemini: turns start with user and alternate", roles[0] == "user" and all(a != b for a, b in zip(roles, roles[1:])) and roles[-1] == "user", str(roles))
check("gemini: current message is last turn", payload["contents"][-1]["parts"][0]["text"].endswith("Explain recursion"))

# context follows live state
client.post("/api/subjects", json={"Python": 95, "C": 90, "DSA": 88, "DBMS": 92, "Aptitude": 85})
calls.clear(); chat("how am i doing")
check("context reflects live updates (90% overall)", "Overall placement score: 90%" in calls[0][1]["system_instruction"]["parts"][0]["text"])
client.post("/api/reset")

# ---------------- OpenAI path (mocked) ----------------
os.environ["AI_PROVIDER"] = "openai"; os.environ["OPENAI_API_KEY"] = "sk-test"
calls.clear(); code, j = chat("hello")
url, payload, headers = calls[0]
check("openai: reply + source", j["reply"] == "OpenAI says hi" and j["source"] == "openai")
check("openai: bearer header, system + user messages", headers["Authorization"] == "Bearer sk-test"
      and payload["messages"][0]["role"] == "system" and payload["messages"][-1]["role"] == "user" and payload["model"] == "gpt-4o-mini")
os.environ.pop("AI_PROVIDER"); os.environ.pop("OPENAI_API_KEY")

# ---------------- provider failures fall back gracefully ----------------
os.environ["GEMINI_API_KEY"] = "test-key-123"
for status, text in ((429, "busy"), (403, "rejected")):
    def boom(url, payload, headers, s=status):
        raise chatbot.AIError({429: "The AI service is busy or the free quota is used up. Please try again in a minute.",
                               403: "The AI service rejected the request. Check that your API key and model name are correct."}[s], s)
    chatbot._post_json = boom
    code, j = chat("Analyze my progress")
    check(f"provider error {status} -> 200 + local answer + notice", code == 200 and j["source"] == "local" and j.get("notice") and "52%" in j["reply"])
def empty(url, payload, headers): return {"candidates": []}
chatbot._post_json = empty
code, j = chat("hi there")
check("empty AI answer -> local fallback with notice", code == 200 and j["source"] == "local" and j.get("notice"))

# real _post_json maps HTTP / network errors without leaking the key
import urllib.error, urllib.request, io
chatbot._post_json = real_post
orig = urllib.request.urlopen
def raise_http(req, timeout=None): raise urllib.error.HTTPError(req.full_url, 429, "x", {}, io.BytesIO(b"{}"))
urllib.request.urlopen = raise_http
code, j = chat("hi")
check("real HTTP 429 handled", j["source"] == "local" and "quota" in j["notice"] and "test-key" not in str(j))
def raise_net(req, timeout=None): raise urllib.error.URLError("no network")
urllib.request.urlopen = raise_net
code, j = chat("hi")
check("network failure handled", j["source"] == "local" and "internet" in j["notice"])
urllib.request.urlopen = orig
os.environ.pop("GEMINI_API_KEY")

# ---------------- model fallback + crash-proofing ----------------
os.environ["GEMINI_API_KEY"] = "test-key-123"; os.environ["GEMINI_MODEL"] = "retired-model"
chatbot._WORKING_MODEL.clear(); tried = []
def picky_post(url, payload, headers):
    tried.append(url.split("/models/")[1].split(":")[0])
    if "retired-model" in url:
        raise chatbot.AIError("model not found", 404)
    gc = payload["generationConfig"]
    return {"candidates": [{"content": {"parts": [{"text": "ok " + str("thinkingConfig" in gc)}]}}]}
chatbot._post_json = picky_post
code, j = chat("explain recursion")
check("404 on configured model -> falls back to another model", j.get("source") == "gemini" and tried[:2] == ["retired-model", "gemini-flash-latest"], str(tried))
tried.clear(); chat("again")
check("working fallback model is remembered (dead model not retried)", tried == ["gemini-flash-latest"], str(tried))
check("thinkingConfig only sent to 2.5-flash models", j["reply"] == "ok False")
os.environ.pop("GEMINI_MODEL")
def quota(url, payload, headers): raise chatbot.AIError("busy", 429)
chatbot._post_json = quota; tried.clear()
code, j = chat("hi")
check("429 does not loop through models", j["source"] == "local" and j.get("notice") == "busy")
import http.client
def weird(url, payload, headers): raise http.client.IncompleteRead(b"x")
chatbot._post_json = weird
code, j = chat("hi")
check("unexpected exception -> still JSON 200 with local answer + notice", code == 200 and j["source"] == "local" and j.get("notice"))
chatbot._post_json = real_post
urllib.request.urlopen = lambda req, timeout=None: (_ for _ in ()).throw(http.client.IncompleteRead(b"x"))
code, j = chat("hi")
check("real _post_json maps IncompleteRead to AIError", code == 200 and j["source"] == "local" and "internet" in j["notice"])
urllib.request.urlopen = orig
check("unknown /api route -> JSON 404, not HTML", client.get("/api/nope").get_json(silent=True) is not None)
os.environ.pop("GEMINI_API_KEY")

# ---------------- validation + rate limit ----------------
chatbot._RATE_BUCKETS.clear()
check("non-JSON body -> 400", client.post("/api/chat", data="x", content_type="text/plain").status_code == 400)
check("missing message -> 400", client.post("/api/chat", json={}).status_code == 400)
check("blank message -> 400", chat("   ")[0] == 400)
check("non-string message -> 400", client.post("/api/chat", json={"message": 123}).status_code == 400)
check("over-long message -> 400", chat("x" * 4001)[0] == 400)
check("exactly 4000 chars accepted", chat("x" * 4000)[0] == 200)
chatbot._RATE_BUCKETS.clear()
codes = [client.post("/api/chat", json={"message": "hi"}).status_code for _ in range(22)]
check("rate limit: first 20 ok, then 429", codes[:20] == [200] * 20 and codes[20:] == [429, 429], str(codes[18:]))
chatbot._RATE_BUCKETS.clear()

# ---------------- .env loader ----------------
import tempfile
tmp = tempfile.mkdtemp(); open(os.path.join(tmp, ".env"), "w", encoding="utf-8-sig").write('# c\nFOO_TEST_KEY="abc"\nBAR_TEST=1\nEMPTY_TEST=zzz\n')
os.environ["EMPTY_TEST"] = ""
old = chatbot.BASE_DIR; chatbot.BASE_DIR = tmp; os.environ["BAR_TEST"] = "keep"
chatbot._load_env_file(); chatbot.BASE_DIR = old
check(".env loader reads values (even with Windows BOM), real env wins, empty env var does not block",
      os.environ.get("FOO_TEST_KEY") == "abc" and os.environ["BAR_TEST"] == "keep" and os.environ["EMPTY_TEST"] == "zzz")

passed = sum(1 for _, ok, _ in results if ok)
for n, ok, d in results:
    print(("PASS  " if ok else "FAIL  ") + n + (f"   [{d}]" if d and not ok else ""))
print("-" * 70); print(f"{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)

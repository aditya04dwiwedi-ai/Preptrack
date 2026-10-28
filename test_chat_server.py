"""Checks for the room-based community chat server. Run: python test_chat_server.py"""

import json
import sys

import app as backend

client = backend.app.test_client()
results = []


def check(name, condition, detail=""):
    results.append((name, bool(condition), detail))


def post_message(room, name, message):
    return client.post("/api/chatroom/messages", json={
        "room": room, "name": name, "message": message
    })


page = client.get("/community-chat")
check("community chat page loads", page.status_code == 200 and b"Study together" in page.data)
check("dashboard links to community chat", b"/community-chat" in client.get("/").data)

response = post_message("test-room-a", "Student One", "Hello room")
data = response.get_json()
check("valid message accepted", response.status_code == 200 and data["success"])
check("message contains room, sender, content and id",
      data["message"]["room"] == "test-room-a" and data["message"]["name"] == "Student One"
      and data["message"]["message"] == "Hello room" and data["message"]["id"])

events = client.get("/api/chatroom/events?room=test-room-a", buffered=False)
first_event = next(events.response).decode("utf-8")
check("SSE starts with room history", "event: history" in first_event and "Hello room" in first_event)
response = post_message("test-room-a", "Student Two", "Live update")
live_event = next(events.response).decode("utf-8")
check("new messages are broadcast to connected clients",
      response.status_code == 200 and "event: message" in live_event and "Live update" in live_event)
events.close()

other_room = client.get("/api/chatroom/events?room=test-room-b", buffered=False)
other_history = next(other_room.response).decode("utf-8")
check("room history is isolated", "Hello room" not in other_history and "Live update" not in other_history)
other_room.close()

check("missing JSON rejected", client.post("/api/chatroom/messages", data="x", content_type="text/plain").status_code == 400)
check("blank message rejected", post_message("test-room-a", "Student", "  ").status_code == 400)
check("oversized message rejected",
      post_message("test-room-a", "Student", "x" * 1001).status_code == 400)
check("invalid name rejected", post_message("<script>", "x", "hello").status_code == 400)
check("invalid room rejected", post_message("../private", "Student", "hello").status_code == 400)
check("message history endpoint rejects invalid room",
      client.get("/api/chatroom/events?room=%2Fbad").status_code == 400)

passed = sum(1 for _, ok, _ in results if ok)
for name, ok, detail in results:
    print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail and not ok else ""))
print("-" * 70)
print(f"{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)

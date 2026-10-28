"""In-memory, room-based community chat with server-sent event delivery."""

import json
import re
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from queue import Empty, Full, Queue

from flask import Response, jsonify, render_template, request, stream_with_context

MAX_NAME_CHARS = 32
MAX_ROOM_CHARS = 32
MAX_MESSAGE_CHARS = 1000
HISTORY_LIMIT = 100
RATE_LIMIT = 12
RATE_WINDOW_SECONDS = 10
STREAM_HEARTBEAT_SECONDS = 20

_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9 _.-]*\Z")
_ROOM_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9 _-]*\Z")


class ChatRoomStore:
    """Thread-safe room history and subscriber queues for one server process."""

    def __init__(self):
        self._lock = threading.Lock()
        self._messages = defaultdict(lambda: deque(maxlen=HISTORY_LIMIT))
        self._subscribers = defaultdict(set)

    def subscribe(self, room):
        subscriber = Queue(maxsize=HISTORY_LIMIT)
        with self._lock:
            history = list(self._messages[room])
            self._subscribers[room].add(subscriber)
        return history, subscriber

    def unsubscribe(self, room, subscriber):
        with self._lock:
            self._subscribers[room].discard(subscriber)
            if not self._subscribers[room]:
                self._subscribers.pop(room, None)

    def publish(self, message):
        with self._lock:
            self._messages[message["room"]].append(message)
            subscribers = tuple(self._subscribers[message["room"]])
        for subscriber in subscribers:
            while True:
                try:
                    subscriber.put_nowait(message)
                    break
                except Full:
                    try:
                        subscriber.get_nowait()
                    except Empty:
                        continue


_store = ChatRoomStore()
_rate_lock = threading.Lock()
_rate_buckets = defaultdict(deque)


def _valid_label(value, pattern, max_length):
    return (isinstance(value, str) and 1 <= len(value.strip()) <= max_length
            and pattern.fullmatch(value.strip()) is not None)


def _rate_limited(client_id):
    now = time.monotonic()
    with _rate_lock:
        bucket = _rate_buckets[client_id]
        while bucket and now - bucket[0] >= RATE_WINDOW_SECONDS:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT:
            return True
        bucket.append(now)
        return False


def _sse(event, data):
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def register_chat_server(app):
    """Register the community chat page and its JSON/SSE endpoints."""

    @app.get("/community-chat")
    def community_chat_page():
        return render_template("chat.html")

    @app.get("/api/chatroom/events")
    def chatroom_events():
        room = request.args.get("room", "lobby").strip()
        if not _valid_label(room, _ROOM_RE, MAX_ROOM_CHARS):
            return jsonify({"success": False, "error": "Room names must be 1-32 letters, numbers, spaces, dots, underscores or hyphens."}), 400

        history, subscriber = _store.subscribe(room)

        @stream_with_context
        def stream():
            try:
                yield _sse("history", history)
                while True:
                    try:
                        message = subscriber.get(timeout=STREAM_HEARTBEAT_SECONDS)
                        yield _sse("message", message)
                    except Empty:
                        yield ": keepalive\n\n"
            finally:
                _store.unsubscribe(room, subscriber)

        return Response(stream(), mimetype="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        })

    @app.post("/api/chatroom/messages")
    def chatroom_send_message():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"success": False, "error": "Send a JSON object with name, room and message fields."}), 400

        name = data.get("name")
        room = data.get("room", "lobby")
        message = data.get("message")
        if not _valid_label(name, _NAME_RE, MAX_NAME_CHARS):
            return jsonify({"success": False, "error": "Display names must be 1-32 letters, numbers, spaces, dots, underscores or hyphens."}), 400
        if not _valid_label(room, _ROOM_RE, MAX_ROOM_CHARS):
            return jsonify({"success": False, "error": "Room names must be 1-32 letters, numbers, spaces, dots, underscores or hyphens."}), 400
        if not isinstance(message, str) or not message.strip():
            return jsonify({"success": False, "error": "Please type a message first."}), 400

        message = message.strip()
        if len(message) > MAX_MESSAGE_CHARS:
            return jsonify({"success": False, "error": f"Messages are limited to {MAX_MESSAGE_CHARS} characters."}), 400
        if _rate_limited(request.remote_addr or "unknown"):
            return jsonify({"success": False, "error": "You are sending messages too quickly. Please wait a moment."}), 429

        record = {
            "id": uuid.uuid4().hex,
            "room": room.strip(),
            "name": name.strip(),
            "message": message,
            "sent_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        _store.publish(record)
        return jsonify({"success": True, "message": record})

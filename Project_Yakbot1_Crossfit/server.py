import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock


WORKSPACE = Path(__file__).resolve().parent
MAX_REQUEST_SIZE = 64 * 1024
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://charlsdev281.github.io").rstrip("/")
workout_state = None
workout_lock = Lock()


def is_valid_workout(workout):
    if not isinstance(workout, dict):
        return False
    if not isinstance(workout.get("isActive"), bool):
        return False
    if not isinstance(workout.get("isFinished"), bool):
        return False
    if workout.get("timerMode") not in {"for-time", "amrap", "emom"}:
        return False
    if workout.get("controlMode") not in {"automatic", "manual"}:
        return False
    if not isinstance(workout.get("isStarted"), bool):
        return False

    exercises = workout.get("exercises")
    if not isinstance(exercises, list) or not exercises:
        return False
    for exercise in exercises:
        if not isinstance(exercise, dict):
            return False
        if not isinstance(exercise.get("name"), str) or not exercise["name"]:
            return False
        if not isinstance(exercise.get("focus"), str):
            return False
        duration = exercise.get("duration")
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration <= 0:
            return False

    current_index = workout.get("currentIndex")
    if isinstance(current_index, bool) or not isinstance(current_index, int):
        return False
    if not 0 <= current_index < len(exercises):
        return False

    remaining = workout.get("currentRemaining")
    if isinstance(remaining, bool) or not isinstance(remaining, (int, float)) or remaining < 0:
        return False

    timer_mode = workout["timerMode"]
    if timer_mode != "emom":
        time_cap = workout.get("timeCapSeconds")
        elapsed = workout.get("elapsedSeconds")
        if isinstance(time_cap, bool) or not isinstance(time_cap, int) or not 60 <= time_cap <= 7200:
            return False
        if isinstance(elapsed, bool) or not isinstance(elapsed, int) or not 0 <= elapsed <= time_cap:
            return False

        if timer_mode == "amrap":
            time_left = workout.get("remainingSeconds")
            if isinstance(time_left, bool) or not isinstance(time_left, int) or not 0 <= time_left <= time_cap:
                return False
    return True


class CrossFitRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE), **kwargs)

    def end_headers(self):
        origin = self.headers.get("Origin")
        if origin == ALLOWED_ORIGIN:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Vary", "Origin")
        super().end_headers()

    def do_GET(self):
        if self.path != "/api/workout":
            super().do_GET()
            return

        with workout_lock:
            current_workout = workout_state
        self._send_json({"workout": current_workout})

    def do_OPTIONS(self):
        if self.path != "/api/workout":
            self.send_error(404, "Not found")
            return

        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/workout":
            self.send_error(404, "Not found")
            return

        content_length = self.headers.get("Content-Length")
        if content_length is None:
            self.send_error(411, "Content-Length required")
            return
        try:
            request_size = int(content_length)
        except ValueError:
            self.send_error(400, "Invalid Content-Length")
            return
        if request_size < 0 or request_size > MAX_REQUEST_SIZE:
            self.send_error(413, "Request too large")
            return

        try:
            workout = json.loads(self.rfile.read(request_size))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_error(400, "Invalid JSON")
            return
        if not is_valid_workout(workout):
            self.send_error(400, "Invalid workout state")
            return

        global workout_state
        with workout_lock:
            workout_state = workout
        self._send_json({"ok": True})

    def do_DELETE(self):
        if self.path != "/api/workout":
            self.send_error(404, "Not found")
            return

        global workout_state
        with workout_lock:
            workout_state = None
        self._send_json({"ok": True})

    def _send_json(self, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), CrossFitRequestHandler)
    print(f"CrossFit Box available on port {port}. Press Ctrl+C to stop.")
    server.serve_forever()

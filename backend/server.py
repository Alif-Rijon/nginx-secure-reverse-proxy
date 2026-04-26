
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HOST = "0.0.0.0"
PORT = 3000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


tasks = load_tasks()


class TodoHandler(BaseHTTPRequestHandler):

    # Common response helper
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length).decode("utf-8")
        return json.loads(body)

    # Handle CORS preflight
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # GET /api/tasks
    def do_GET(self):
        path = urlparse(self.path).path
        print(f"GET {path}")

        if path == "/api/tasks":
            self.send_json(tasks)
        else:
            self.send_json({"error": "Not Found"}, 404)

    # POST /api/tasks
    def do_POST(self):
        global tasks
        path = urlparse(self.path).path
        print(f"POST {path}")

        if path == "/api/tasks":
            try:
                data = self.read_body()
                text = data.get("text", "").strip()

                if not text:
                    self.send_json({"error": "Task text is required"}, 400)
                    return

                new_task = {
                    "id": max([task["id"] for task in tasks], default=0) + 1,
                    "text": text,
                    "completed": False
                }

                tasks.append(new_task)
                save_tasks(tasks)
                self.send_json(new_task, 201)

            except json.JSONDecodeError:
                self.send_json({"error": "Invalid JSON"}, 400)
        else:
            self.send_json({"error": "Not Found"}, 404)

    # PUT /api/tasks/{id}
    def do_PUT(self):
        global tasks
        path = urlparse(self.path).path
        print(f"PUT {path}")

        parts = path.strip("/").split("/")

        if len(parts) == 3 and parts[0] == "api" and parts[1] == "tasks":
            try:
                task_id = int(parts[2])
                data = self.read_body()

                for task in tasks:
                    if task["id"] == task_id:
                        task["completed"] = data.get("completed", task["completed"])
                        save_tasks(tasks)
                        self.send_json(task)
                        return

                self.send_json({"error": "Task not found"}, 404)

            except ValueError:
                self.send_json({"error": "Invalid task ID"}, 400)
            except json.JSONDecodeError:
                self.send_json({"error": "Invalid JSON"}, 400)
        else:
            self.send_json({"error": "Not Found"}, 404)

    # DELETE /api/tasks/{id}
    def do_DELETE(self):
        global tasks
        path = urlparse(self.path).path
        print(f"DELETE {path}")

        parts = path.strip("/").split("/")

        if len(parts) == 3 and parts[0] == "api" and parts[1] == "tasks":
            try:
                task_id = int(parts[2])

                for task in tasks:
                    if task["id"] == task_id:
                        tasks = [t for t in tasks if t["id"] != task_id]
                        save_tasks(tasks)
                        self.send_json({"message": "Task deleted"})
                        return

                self.send_json({"error": "Task not found"}, 404)

            except ValueError:
                self.send_json({"error": "Invalid task ID"}, 400)
        else:
            self.send_json({"error": "Not Found"}, 404)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), TodoHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()

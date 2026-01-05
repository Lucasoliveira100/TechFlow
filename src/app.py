from flask import Flask, request, jsonify
from storage import Storage

app = Flask(__name__)
store = Storage("tasks.db")

@app.get("/")
def home():
    return """
    <h2>TechFlow Tasks</h2>
    <p>Endpoints:</p>
    <ul>
      <li>GET /tasks</li>
      <li>POST /tasks</li>
      <li>PUT /tasks/&lt;id&gt;</li>
      <li>DELETE /tasks/&lt;id&gt;</li>
    </ul>
    """

@app.get("/tasks")
def list_tasks():
    return jsonify(store.list_tasks())

@app.post("/tasks")
def create_task():
    data = request.get_json(force=True)
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    try:
        task_id = store.create_task(
            title=title,
            description=data.get("description"),
            priority=data.get("priority", "media"),
            status=data.get("status", "to_do"),
            assignee=data.get("assignee"),
            deadline=data.get("deadline"),
        )
        return jsonify({"id": task_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.put("/tasks/<int:task_id>")
def update_task(task_id: int):
    data = request.get_json(force=True)
    try:
        store.update_task(task_id, **data)
        return jsonify({"ok": True})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    store.delete_task(task_id)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)

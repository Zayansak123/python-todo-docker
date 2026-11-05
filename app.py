from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
tasks = []
next_id = 1

PAGE = """
<!doctype html>
<title>Todo App</title>
<body style="font-family:sans-serif;max-width:500px;margin:40px auto">
<h1>Python To-Do App</h1>
<form method="post" action="/add">
  <input name="title" placeholder="New task" required>
  <button>Add</button>
</form>
<ul>
{% for t in tasks %}
  <li>
    <span style="{{ 'text-decoration:line-through' if t.done }}">{{ t.title }}</span>
    <a href="/complete/{{ t.id }}">[done]</a>
    <a href="/delete/{{ t.id }}">[delete]</a>
  </li>
{% else %}
  <li>No tasks yet</li>
{% endfor %}
</ul>
</body>
"""

@app.route("/")
def index():
    return render_template_string(PAGE, tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    global next_id
    tasks.append({"id": next_id, "title": request.form["title"], "done": False})
    next_id += 1
    return redirect("/")

@app.route("/complete/<int:task_id>")
def complete(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

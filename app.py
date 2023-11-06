"""
Pequena aplicação em Flask para demonstrar uso de pipelines
"""
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()


class Todo(db.Model):
    """
    Class for representing a to-do item.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __init__(self, title, complete=False):
        """
        Initialize a to-do item.

        Args:
            title (str): The title of the to-do item.
            complete (bool, optional): Whether the to-do item is complete (default is False).
        """
        self.title = title
        self.complete = complete

    def mark_as_complete(self):
        """
        Mark this to-do item as complete.
        """
        self.complete = True

    def mark_as_incomplete(self):
        """
        Mark this to-do item as incomplete.
        """
        self.complete = False

@app.route("/edit")
def home1():
    """
    Api edit Todo
    """
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/")
def list1():
    """
    Api list Todo
    """
    todo_list = Todo.query.all()
    return render_template("list.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    """
    Api add Todo
    """
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home1"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    """
    Api update Todo
    """
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home1"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    """
    Api delete Todo
    """
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home1"))


if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", debug=True)

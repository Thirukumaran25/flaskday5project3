from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import db, Task
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ✅ Always initialize the DB (even in deployment)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.due_date).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    due_date_str = request.form['due_date']
    if title and due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        new_task = Task(title=title, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    Task.query.filter_by(is_done=True).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

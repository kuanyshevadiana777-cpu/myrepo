from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = "secretkey123"

conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=LAPTOP-B1IROIJR\SQLEXPRESS;"
    "Database=school_portal;"
    "Trusted_Connection=yes;"
)

def get_db_connection():
    try:
        return pyodbc.connect(conn_str)
    except Exception as e:
        print("Database connection error:", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == "POST":
        name = request.form['name']
        parent_email = request.form['parent_email']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Students (name, parent_email) VALUES (?, ?)", (name, parent_email))
            conn.commit()
            conn.close()
            flash("Студент успешно добавлен!", "success")
            return redirect(url_for('index'))
        else:
            flash("Ошибка соединения с базой данных", "danger")
    return render_template('add_student.html')

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database initialization function
def initialize_database():
    conn = sqlite3.connect("employee_management.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL,
            hire_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call the database initialization function
initialize_database()

# Database connection function
def get_db_connection():
    conn = sqlite3.connect("employee_management.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Add employee
@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        salary = request.form["salary"]
        hire_date = request.form["hire_date"]

        conn = get_db_connection()
        conn.execute("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
                     (name, department, salary, hire_date))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add_employee.html")

# View employees
@app.route("/view")
def view_employees():
    conn = get_db_connection()
    employees = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()
    return render_template("view_employees.html", employees=employees)

# Update employee
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_employee(id):
    conn = get_db_connection()
    employee = conn.execute("SELECT * FROM employees WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        salary = request.form["salary"]
        hire_date = request.form["hire_date"]

        conn.execute("UPDATE employees SET name = ?, department = ?, salary = ?, hire_date = ? WHERE id = ?",
                     (name, department, salary, hire_date, id))
        conn.commit()
        conn.close()
        return redirect("/view")
    return render_template("update_employee.html", employee=employee)

# Delete employee
@app.route("/delete/<int:id>")
def delete_employee(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM employees WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/view")

if __name__ == "__main__":
    app.run(debug=True)

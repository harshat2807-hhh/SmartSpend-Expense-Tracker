import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_NAME = "expenses.db"

def get_db_connection():
    """Establishes and returns a database connection with Row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database and creates the expenses table if it does not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on application load
init_db()

@app.route('/')
def index():
    """Renders the main dashboard page."""
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """READ ALL: Fetch all expenses from database ordered by date descending."""
    try:
        conn = get_db_connection()
        expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC, id DESC').fetchall()
        conn.close()
        
        result = [dict(expense) for expense in expenses]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve expenses: {str(e)}"}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """READ ONE: Fetch a single expense by ID."""
    try:
        conn = get_db_connection()
        expense = conn.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,)).fetchone()
        conn.close()
        
        if expense is None:
            return jsonify({"error": f"Expense with ID {expense_id} not found"}), 404
            
        return jsonify(dict(expense)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve expense: {str(e)}"}), 500

@app.route('/api/expenses', methods=['POST'])
def create_expense():
    """CREATE: Add a new expense record."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid payload, JSON required"}), 400
            
        title = data.get('title', '').strip() if isinstance(data.get('title'), str) else ''
        amount = data.get('amount')
        category = data.get('category', '').strip() if isinstance(data.get('category'), str) else ''
        date = data.get('date', '').strip() if isinstance(data.get('date'), str) else ''
        payment_method = data.get('payment_method', '').strip() if isinstance(data.get('payment_method'), str) else ''
        notes = data.get('notes', '').strip() if isinstance(data.get('notes'), str) else ''
        
        # Backend Validation
        if not title:
            return jsonify({"error": "Title is required"}), 400
            
        if amount is None or amount == '':
            return jsonify({"error": "Amount is required"}), 400
            
        try:
            amount_val = float(amount)
            if amount_val <= 0:
                return jsonify({"error": "Amount must be greater than 0"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Amount must be a valid numeric number"}), 400
            
        if not category:
            return jsonify({"error": "Category is required"}), 400
            
        if not date:
            return jsonify({"error": "Date is required"}), 400
            
        if not payment_method:
            return jsonify({"error": "Payment method is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (title, amount, category, date, payment_method, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, amount_val, category, date, payment_method, notes))
        conn.commit()
        new_id = cursor.lastrowid
        
        new_expense = conn.execute('SELECT * FROM expenses WHERE id = ?', (new_id,)).fetchone()
        conn.close()
        
        return jsonify(dict(new_expense)), 201

    except Exception as e:
        return jsonify({"error": f"Failed to create expense: {str(e)}"}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """UPDATE: Modify an existing expense record."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid payload, JSON required"}), 400

        conn = get_db_connection()
        existing = conn.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,)).fetchone()
        
        if existing is None:
            conn.close()
            return jsonify({"error": f"Expense with ID {expense_id} not found"}), 404

        title = data.get('title', '').strip() if isinstance(data.get('title'), str) else ''
        amount = data.get('amount')
        category = data.get('category', '').strip() if isinstance(data.get('category'), str) else ''
        date = data.get('date', '').strip() if isinstance(data.get('date'), str) else ''
        payment_method = data.get('payment_method', '').strip() if isinstance(data.get('payment_method'), str) else ''
        notes = data.get('notes', '').strip() if isinstance(data.get('notes'), str) else ''
        
        # Backend Validation
        if not title:
            conn.close()
            return jsonify({"error": "Title is required"}), 400
            
        if amount is None or amount == '':
            conn.close()
            return jsonify({"error": "Amount is required"}), 400
            
        try:
            amount_val = float(amount)
            if amount_val <= 0:
                conn.close()
                return jsonify({"error": "Amount must be greater than 0"}), 400
        except (ValueError, TypeError):
            conn.close()
            return jsonify({"error": "Amount must be a valid numeric number"}), 400
            
        if not category:
            conn.close()
            return jsonify({"error": "Category is required"}), 400
            
        if not date:
            conn.close()
            return jsonify({"error": "Date is required"}), 400
            
        if not payment_method:
            conn.close()
            return jsonify({"error": "Payment method is required"}), 400

        cursor = conn.cursor()
        cursor.execute('''
            UPDATE expenses
            SET title = ?, amount = ?, category = ?, date = ?, payment_method = ?, notes = ?
            WHERE id = ?
        ''', (title, amount_val, category, date, payment_method, notes, expense_id))
        conn.commit()
        
        updated_expense = conn.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,)).fetchone()
        conn.close()
        
        return jsonify(dict(updated_expense)), 200

    except Exception as e:
        return jsonify({"error": f"Failed to update expense: {str(e)}"}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """DELETE: Remove an expense by ID."""
    try:
        conn = get_db_connection()
        existing = conn.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,)).fetchone()
        
        if existing is None:
            conn.close()
            return jsonify({"error": f"Expense with ID {expense_id} not found"}), 404

        conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Expense deleted successfully", "id": expense_id}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete expense: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

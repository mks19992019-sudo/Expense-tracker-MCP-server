from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database.'''
    try:
        with sqlite3.connect(DB_PATH) as c:
            cur = c.execute(
                "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
                (date, amount, category, subcategory, note)
            )
            c.commit()
            return {"status": "success", "id": cur.lastrowid, "message": "Expense added successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    try:
        with sqlite3.connect(DB_PATH) as c:
            cur = c.execute(
                """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY id ASC
                """,
                (start_date, end_date)
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_expense(expense_id):
    '''Get a specific expense by ID.'''
    try:
        with sqlite3.connect(DB_PATH) as c:
            cur = c.execute(
                """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE id = ?
                """,
                (expense_id,)
            )
            cols = [d[0] for d in cur.description]
            row = cur.fetchone()
            if row:
                return dict(zip(cols, row))
            return {"error": "Expense not found"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def edit_expense(expense_id, date=None, amount=None, category=None, subcategory=None, note=None):
    '''Edit an existing expense entry. Only provide fields you want to update.'''
    try:
        with sqlite3.connect(DB_PATH) as c:
            # First check if expense exists
            cur = c.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
            if not cur.fetchone():
                return {"status": "error", "message": "Expense not found"}
            
            # Build dynamic update query
            updates = []
            params = []
            if date is not None:
                updates.append("date = ?")
                params.append(date)
            if amount is not None:
                updates.append("amount = ?")
                params.append(amount)
            if category is not None:
                updates.append("category = ?")
                params.append(category)
            if subcategory is not None:
                updates.append("subcategory = ?")
                params.append(subcategory)
            if note is not None:
                updates.append("note = ?")
                params.append(note)
            
            if not updates:
                return {"status": "error", "message": "No fields to update"}
            
            params.append(expense_id)
            query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
            c.execute(query, params)
            c.commit()
            return {"status": "success", "message": "Expense updated successfully", "id": expense_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def delete_expense(expense_id):
    '''Delete an expense entry by ID.'''
    try:
        with sqlite3.connect(DB_PATH) as c:
            cur = c.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
            if not cur.fetchone():
                return {"status": "error", "message": "Expense not found"}
            
            c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            c.commit()
            return {"status": "success", "message": "Expense deleted successfully", "id": expense_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    try:
        with sqlite3.connect(DB_PATH) as c:
            query = (
                """
                SELECT category, SUM(amount) AS total_amount
                FROM expenses
                WHERE date BETWEEN ? AND ?
                """
            )
            params = [start_date, end_date]

            if category:
                query += " AND category = ?"
                params.append(category)

            query += " GROUP BY category ORDER BY category ASC"

            cur = c.execute(query, params)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import sys
    print("Starting Expense Tracker MCP Server...")
    print(f"Database: {DB_PATH}")
    print(f"Categories: {CATEGORIES_PATH}")
    try:
        mcp.run(transport='http', host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)

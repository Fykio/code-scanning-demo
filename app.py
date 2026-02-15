from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# SQL Injection vulnerability
@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Vulnerable: Direct string concatenation
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)  # SonarLint will flag this
    result = cursor.fetchone()
    conn.close()
    return str(result)

# Command Injection vulnerability
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    # Vulnerable: Using shell=True with user input
    result = os.system(f'ping -c 1 {host}')  # SonarLint will flag this
    return f'Ping result: {result}'

# Hardcoded credentials (code smell)
DATABASE_PASSWORD = "admin123"  # SonarLint will flag this

# Unused variable (code smell)
def unused_function():
    x = 10  # SonarLint will flag this as unused
    return 5

# Complexity issue
def complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:  # Too many nested conditions
                        return True
    return False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)  # Security: debug mode in production
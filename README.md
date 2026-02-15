# Code Quality Scanning Demo

This is a demo project showing how to detect code quality issues, security vulnerabilities, bugs, and code smells in a Python/Flask application using SonarQube/SonarCloud and the SonarQube for IDE VSCode extension.

## What is Code Scanning?

Code scanning (also called Static Application Security Testing - SAST) analyzes your source code without executing it to find:
- **Security vulnerabilities** (SQL injection, command injection, XSS, etc.)
- **Bugs** (null pointer exceptions, resource leaks, logic errors)
- **Code smells** (unused variables, complexity issues, maintainability problems)
- **Best practice violations** (hardcoded credentials, debug mode in production)

## How it works

- The Flask app (`app.py`) contains intentional security vulnerabilities and code quality issues.
- **SonarQube for IDE VSCode extension** provides real-time feedback while you code, highlighting issues directly in the editor.
- **SonarCloud GitHub Action** runs automated scans on every push and pull request, preventing problematic code from being merged.
- Issues are classified by severity: Blocker, Critical, Major, Minor, and Info.

## Vulnerabilities Included

This demo includes the following intentional vulnerabilities and code issues:

1. **SQL Injection** - Direct string concatenation in SQL queries
2. **Command Injection** - Using `os.system()` with user input
3. **Hardcoded Credentials** - Database password stored in code
4. **Debug Mode in Production** - Flask debug mode enabled
5. **Unused Variables** - Dead code that should be removed
6. **High Cyclomatic Complexity** - Deeply nested conditions
7. **Resource Leaks** - Database connections not properly closed

## Files

- `app.py`: Flask application with intentional security vulnerabilities and code smells.
- `requirements.txt`: Python dependencies (Flask).
- `.github/workflows/code-scan.yml`: GitHub Actions workflow that runs SonarCloud scan on each push/PR to `main` branch.
- `sonar-project.properties`: SonarQube project configuration.

## Local Development with SonarQube for IDE

### Step 1: Install SonarQube for IDE Extension

1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
3. Search for "SonarQube for IDE"
4. Click Install
5. Restart VSCode

### Step 2: Open the Project

1. Open this project folder in VSCode
2. Open `app.py`
3. SonarQube for IDE will automatically analyze the file and show issues with colored underlines:
   - 🔴 **Red squiggles** = Bugs or Security Vulnerabilities
   - 🟡 **Yellow squiggles** = Code Smells
   - 💡 **Blue squiggles** = Suggestions

### Step 3: View Issues

- Hover over any squiggly line to see the issue description
- Click on the issue to see detailed explanation and how to fix it
- Check the "Problems" panel (View → Problems) to see all issues in the project

### Example Issues You'll See

```python
# SQL Injection - SonarQube for IDE will flag this
query = "SELECT * FROM users WHERE username = '" + username + "'"
# 🔴 Make sure that this SQL query is not vulnerable to injection attacks

# Command Injection - SonarQube for IDE will flag this
result = os.system(f'ping -c 1 {host}')
# 🔴 Make sure that command line arguments are sanitized

# Hardcoded credentials - SonarQube for IDE will flag this
DATABASE_PASSWORD = "admin123"
# 🟡 Remove this hardcoded password
```

## CI Integration with SonarCloud

### Prerequisites

1. A GitHub account
2. A SonarCloud account (free for public repos)

### Setup Steps

1. **Sign up for SonarCloud**
   - Go to [sonarcloud.io](https://sonarcloud.io)
   - Click "Log in with GitHub"
   - Authorize SonarCloud to access your repositories

2. **Import Your Repository**
   - Click the "+" icon in the top right
   - Select `Analyze new project`
   - Choose your repository from the list
   - Click `Set Up`

3. **Get Your Token**
   - Click on your profile picture in the top right corner
   - Select "My Account" fron the dropdown menu
   - Click on security from the left side menu
   - You'll see a "Generate Tokens" section
   - SonarCloud will generate a `SONAR_TOKEN`
   - Copy this token (you'll need it for GitHub)

4. **Add Token to GitHub Secrets**
   - Go to your GitHub repository
   - Click `Settings → Secrets and variables → Actions`
   - Click "New repository secret"
   - Name: `SONAR_TOKEN`
   - Value: [paste the token from SonarCloud]
   - Click "Add secret"

5. **Create Configuration File**
   - Create `sonar-project.properties` in your repository root:
   ```properties
   sonar.projectKey=your-github-username_your-repo-name
   sonar.organization=your-github-username

   sonar.sources=.
   sonar.exclusions=**/venv/**,**/__pycache__/**,**/node_modules/**

   sonar.python.version=3.8,3.9,3.10,3.11,3.12
   ```

6. **Push Your Code**
   - The GitHub Actions workflow will automatically run
   - View results in the Actions tab and on SonarCloud dashboard

## GitHub Actions Setup

The workflow (`.github/workflows/code-scan.yml`) automatically runs on:
- Every push to `main` branch
- Every pull request targeting `main` branch

The workflow will:
1. Check out your code
2. Set up Python environment
3. Install dependencies
4. Run SonarCloud analysis
5. Upload results to SonarCloud dashboard

## Expected Result

When SonarCloud scans the vulnerable code, you'll see output like:

```
INFO: Analysis report generated in 156ms
INFO: Analysis reports compressed in 23ms
INFO: Analysis report uploaded in 89ms
INFO: ANALYSIS SUCCESSFUL, you can browse https://sonarcloud.io/dashboard?id=your-project
INFO: Note that you will be able to access the updated dashboard once the server has processed the submitted analysis report

Quality Gate Status: FAILED
  - 7 Security Vulnerabilities found
  - 5 Code Smells found
  - 12 Bugs found
```

### Viewing Results

1. **In SonarCloud Dashboard:**
   - Click on your project in SonarCloud
   - See overview with bug count, vulnerability count, code smells
   - Click on any issue to see:
     - Where it occurs in the code
     - Why it's a problem
     - How to fix it
     - Severity level

2. **In GitHub Pull Requests:**
   - SonarCloud will add comments on your PR
   - Shows quality gate status (Pass/Fail)
   - Links to full analysis results

## How to Fix the Issues

Once you've seen the identified issues, here's how to fix them:

### 1. SQL Injection Fix

**Before (Vulnerable):**
```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)
```

**After (Secure):**
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))  # Use parameterized queries
```

### 2. Command Injection Fix

**Before (Vulnerable):**
```python
result = os.system(f'ping -c 1 {host}')
```

**After (Secure):**
```python
import subprocess
result = subprocess.run(['ping', '-c', '1', host], capture_output=True)
```

### 3. Hardcoded Credentials Fix

**Before (Vulnerable):**
```python
DATABASE_PASSWORD = "admin123"
```

**After (Secure):**
```python
import os
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
```

### 4. Debug Mode Fix

**Before (Vulnerable):**
```python
app.run(debug=True)
```

**After (Secure):**
```python
app.run(debug=os.environ.get('FLASK_ENV') == 'development')
```

## Running Locally

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app (with vulnerabilities - for demo only!)
python3 app.py

# Visit http://localhost:4444
```

## Alternative: Self-Hosted SonarQube

If you prefer to run SonarQube locally instead of using SonarCloud:

```bash
# Start SonarQube with Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Wait ~2 minutes for startup, then visit http://localhost:9000
# Login: use admin/admin (you'll be prompted to change the password)

# Install sonar-scanner
brew install sonar-scanner  # macOS
# or download from https://docs.sonarqube.org/latest/analyzing-source-code/scanners/sonarscanner/

# Create a token in SonarQube UI (Administration → Security → Users → Tokens)

# Run scan
sonar-scanner \
  -Dsonar.projectKey=code-scan-demo \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN
```

## Benefits of Code Scanning

✅ **Early Detection** - Catch vulnerabilities before code review  
✅ **Developer Education** - Learn secure coding practices through real-time feedback  
✅ **Consistent Standards** - Enforce code quality across the team  
✅ **Reduced Technical Debt** - Identify and fix code smells early  
✅ **Compliance** - Meet security standards (OWASP, CWE, SANS)  

## Learning Resources

- [SonarQube Documentation](https://docs.sonarqube.org/)
- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SonarQube for IDE VSCode Extension](https://marketplace.visualstudio.com/items?itemName=SonarSource.SonarQube for IDE-vscode)

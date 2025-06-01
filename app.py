from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask import jsonify
import sqlite3
import json, os

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

DATABASE = 'rakshsim_users.db'

# --- User Class ---
class User(UserMixin):
    def __init__(self, id_, email, name):
        self.id = id_
        self.email = email
        self.name = name

# --- DB Setup ---
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        # Users
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')
        conn.commit()

        # Check for 'completed_modules' column and add if missing
        cur = conn.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cur.fetchall()]  # fetchall on cursor, not connection
        if 'completed_modules' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN completed_modules INTEGER DEFAULT 0")
            conn.commit()

        # Alerts
        conn.execute('''CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()

        # Simulations
        conn.execute('''CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL,
            resolved BOOLEAN NOT NULL
        )''')
        conn.commit()

        # Training
        conn.execute('''CREATE TABLE IF NOT EXISTS training (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            progress INTEGER NOT NULL
        )''')
        conn.commit()

        # Incidents
        conn.execute('''CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            node TEXT,
            summary TEXT,
            actions TEXT,
            status TEXT,
            category TEXT,
            severity TEXT,
            timestamp TEXT
        )''')

        conn.commit()

init_db()

# --- Load user for Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, email, name FROM users WHERE id=?", (user_id,))
        user = cur.fetchone()
        if user:
            return User(id_=user[0], email=user[1], name=user[2])
    return None

# --- Routes ---
@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, email, name, password FROM users WHERE email=?", (email,))
            user = cur.fetchone()
            if user and bcrypt.check_password_hash(user[3], password):
                user_obj = User(id_=user[0], email=user[1], name=user[2])
                login_user(user_obj)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['fullname'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            with sqlite3.connect(DATABASE) as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                            (name, email, hashed_pw))
                conn.commit()
                flash('Account created successfully. Please log in.', 'success')
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered. Try logging in.', 'warning')
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        # Fetch simulation data
        cur.execute("SELECT COUNT(*) FROM simulations WHERE status='active'")
        active_simulations = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM simulations WHERE resolved=1")
        resolved_incidents = cur.fetchone()[0]
        # Fetch training progress
        cur.execute("SELECT AVG(completed_modules) FROM users")
        completed_avg = cur.fetchone()[0] or 0
        total_modules = 10
        training_progress = int((completed_avg / total_modules) * 100)
        # Fetch alerts
        cur.execute("SELECT message FROM alerts ORDER BY timestamp DESC LIMIT 5")
        alerts = cur.fetchall()

    return render_template('dashboard.html', name=current_user.name,
                           active_simulations=active_simulations,
                           resolved_incidents=resolved_incidents,
                           training_progress=training_progress,
                           alerts=alerts)

@app.route('/simulation')
@login_required
def simulation():
    return render_template('simulation.html', name=current_user.name)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- New route: View and submit incident reports ---
@app.route('/incident-report', methods=['GET', 'POST'])
@login_required
def incident_report():
    if request.method == 'POST':
        affected_node = request.form['node']
        summary = request.form['summary']
        actions = request.form['actions']
        status = request.form['status']
        category = request.form['category']
        severity = request.form['severity']
        timestamp = datetime.now().strftime('%d %b %Y, %I:%M %p')

        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                node TEXT,
                summary TEXT,
                actions TEXT,
                status TEXT,
                category TEXT,
                severity TEXT,
                timestamp TEXT
            )''')
            cur.execute('''INSERT INTO incidents 
                (user_id, node, summary, actions, status, category, severity, timestamp) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (current_user.id, affected_node, summary, actions, status, category, severity, timestamp))
            conn.commit()
            flash('Incident report submitted.', 'success')
            return redirect(url_for('incident_report'))

    # Fetch past reports
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT node, summary, actions, status, category, severity, timestamp FROM incidents WHERE user_id=?", (current_user.id,))
        reports = cur.fetchall()

    return render_template('incident_report.html', name=current_user.name, reports=reports)

@app.route('/api/reports')
@login_required
def api_reports():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT node, category, severity, summary, actions, status, timestamp 
            FROM incidents WHERE user_id=?
            ORDER BY timestamp DESC
            """, (current_user.id,))
        rows = cur.fetchall()

    # Convert query results into list of dicts
    reports = []
    for row in rows:
        reports.append({
            'node': row[0],
            'category': row[1],
            'severity': row[2],
            'summary': row[3],
            'actions': row[4],
            'status': row[5],
            'timestamp': row[6]
        })

    return jsonify(reports)


# --- Training Center Routes ---
@app.route('/training')
@login_required
def training():
    total_modules = 10
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT completed_modules FROM users WHERE id=?", (current_user.id,))
        row = cur.fetchone()
        completed_modules = row[0] if row and row[0] else 0
        progress = int((completed_modules / total_modules) * 100)
    return render_template('training.html', total_modules=total_modules,
                           completed_modules=completed_modules, progress=progress)


@app.route('/complete_module/<int:module_id>', methods=['POST'])
@login_required
def complete_module(module_id):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT completed_modules FROM users WHERE id=?", (current_user.id,))
        completed = cur.fetchone()[0] or 0
        if module_id > completed:
            cur.execute("UPDATE users SET completed_modules=? WHERE id=?", (module_id, current_user.id))
            conn.commit()
    flash(f"Module {module_id} marked as completed.", "success")
    return redirect(url_for('training'))

from backend.scenario_engine import SimulationEngine

# Store in-memory simulations (simplified, per session or ID in prod)
simulations = {}

@app.route('/api/start_simulation', methods=['POST'])
@login_required
def start_simulation():
    engine = SimulationEngine('backend/scenarios/police_hq_breach.json')
    simulations[current_user.id] = engine
    return jsonify(engine.get_current_step())

@app.route('/api/submit_choice', methods=['POST'])
@login_required
def submit_choice():
    data = request.get_json()
    choice_id = data.get('choice')
    engine = simulations.get(current_user.id)
    if not engine:
        return jsonify({'error': 'Simulation not found'}), 404
    result = engine.make_choice(choice_id)
    return jsonify(result)

@app.route('/api/simulation_status')
@login_required
def simulation_status():
    engine = simulations.get(current_user.id)
    if not engine:
        return jsonify({'error': 'Simulation not found'}), 404
    return jsonify({
        'step': engine.get_current_step(),
        'complete': engine.is_complete()
    })

@app.route('/interactive')
@login_required
def interactive_simulation():
    return render_template('interactive_simulation.html', name=current_user.name)

@app.route('/scenario_builder')
@login_required
def scenario_builder():
    return render_template('scenario_builder.html')

@app.route('/save_scenario', methods=['POST'])
@login_required
def save_scenario():
    data = request.get_json()
    try:
        title = data['title'].strip().replace(" ", "_").lower()
        filename = f"{current_user.id}_{title}.json"
        path = os.path.join('backend/user_scenarios', filename)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w') as f:
            json.dump({
                "description": data['description'],
                "nodes": json.loads(data['nodes'])
            }, f, indent=2)

        return "✅ Scenario saved successfully!"
    except Exception as e:
        return f"❌ Error saving scenario: {e}", 500

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
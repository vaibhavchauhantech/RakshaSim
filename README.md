# 🛡️ RakshaSim – Ransomware Incident Simulation & Training Platform

RakshaSim is an interactive, web-based simulation platform designed to train law enforcement officers on handling ransomware attack scenarios. It provides immersive decision-making simulations, tracks performance, and allows admins to create custom scenarios for tailored training.

---

## 📌 Organizer's Problem Statement & Deliverables

**Ransomware Incident Simulation & Training Platform**  
Develop an interactive simulator for law enforcement officers to understand ransomware attack scenarios and build strategic response mechanisms.  
**Deliverables**: Web-based simulation interface, ransomware propagation logic, and scenario-building toolkit.

---

## 🚨 Problem Statement

Law enforcement officers face increasing cybercrime threats, particularly from ransomware attacks. Traditional classroom training lacks the hands-on decision-making needed to respond effectively. RakshaSim bridges this gap with a simulation-based training environment.

---

## 🎯 Key Features

- 🎮 **Interactive Simulation Interface**: Choose-your-own-path scenarios that mimic real-world ransomware incidents.
- 🧠 **Ransomware Propagation Engine**: Simulates spread through network nodes, email vectors, USB devices, etc.
- 🛠️ **Admin Scenario Builder Toolkit**: Create, edit, and manage simulation scenarios through a user-friendly interface.
- 📊 **Trainee Dashboard & Reports**: Tracks trainee performance, decisions, and provides feedback.
- 🔐 **Role-based Access**: Supports admin and trainee logins.

---

## ⚙️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JS (no heavy frameworks for simplicity)
- **Backend**: Python 3.11, Flask
- **Database**: SQLite (`rakshsim_users.db`)
- **Scenario Format**: JSON files (extensible)
- **Deployment**: Localhost / Flask server (can be containerized for cloud)

---

## 🗂️ Folder Structure

```
RakshaSim/
├── app.py                     # Main Flask app
├── rakshsim_users.db          # SQLite database
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
├── frontend/
│   ├── static/                # CSS, JS, images
│   └── templates/             # HTML templates
│       ├── login.html
│       ├── signup.html
│       ├── dashboard.html
│       ├── simulation.html
│       ├── training.html
│       ├── incident_report.html
│       └── interactive_simulation.html
├── backend/
│   ├── scenarios/
│   │   └── police_hq_breach.json  # Sample scenario
│   ├── scenario_engine.py         # Simulation logic
│   └── simulation_engine.py       # Ransomware propagation logic
```

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/yourteam/rakshasim.git
cd rakshasim
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
python app.py
```

### 4. Access in Browser

```
http://localhost:5000/
```

---

## 📝 Creating New Scenarios

- Go to `/admin_builder` route (admin-only).
- Fill in scenario title, description, and nodes (JSON structure).
- Click **Save** — scenario is stored in `backend/scenarios/`.

### 🧩 Scenario JSON Example

```json
{
  "description": "HQ Ransomware Attack",
  "nodes": {
    "start": {
      "text": "A suspicious email attachment has been opened. What do you do?",
      "choices": {
        "isolate": "isolate_node",
        "ignore": "spread_1"
      }
    },
    "isolate_node": {
      "text": "You isolate the device. Attack is contained.",
      "choices": {}
    }
  }
}
```

---

## 📊 Scoring & Reports

- Users are scored based on their decision paths  
- Feedback and learning points are shown at the end of each simulation  
- Incident reports are generated dynamically

---

## 🔮 Future Roadmap

- 📈 Advanced analytics per officer  
- 🎓 Certification module for completed training  
- 🌐 Cloud deployment (SaaS model)  
- 🤖 AI-powered scenario generation  
- 👮 Integration with Chandigarh Police training programs  

---

## 🎥 Demo & Pitch Deck

- **Demo Video (MP4/YouTube)**: *Link to be added*  
- **Pitch Deck (PDF)**: *Link to be added*

---

## 👥 Project Name: RakshaSim - Ransomware Incident Simulation & Training Platform

- **Team Name**: Dam-Verse  
- **Developer**: Vaibhav Chauhan (Solo Developer)
- **University**: JK Lakshmipat University

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🤝 Built for Cyberthon.ai – 2025

**RakshaSim** was developed for **Cyberthon.ai – 2025**, a national-level hackathon organized by the **Chandigarh Police (Cyber Crime Unit)** in partnership with **Infosys TechCohere, Chandigarh**.
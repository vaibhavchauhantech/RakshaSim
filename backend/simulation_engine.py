# simulation_engine.py

import time

class RansomwareSimulation:
    def __init__(self):
        self.score = 0
        self.logs = []
        self.current_node = "start"
        self.start_time = time.time()
        self.path = []

        self.scenario = {
            "start": {
                "text": "Suspicious Email Received.",
                "choices": {
                    "Open attachment": {"next": "infected", "score": -20, "log": "Opened malicious file"},
                    "Report to IT": {"next": "containment", "score": +20, "log": "Proper escalation"}
                }
            },
            "infected": {
                "text": "System infected!",
                "choices": {
                    "Ignore and work": {"next": "spread", "score": -30, "log": "Negligent behavior"},
                    "Isolate system": {"next": "isolation", "score": +10, "log": "Attempted damage control"}
                }
            },
            "containment": {
                "text": "IT responding",
                "choices": {
                    "Wait": {"next": "spread", "score": -10, "log": "Wasted time"},
                    "Start restore": {"next": "restore", "score": +15, "log": "Proactive restore"}
                }
            },
            "spread": {
                "text": "Ransomware spreads!",
                "choices": {
                    "Pay ransom": {"next": "end_bad", "score": -50, "log": "Paid ransom"},
                    "Rebuild system": {"next": "end_good", "score": +10, "log": "Recovered securely"}
                }
            },
            "isolation": {
                "text": "System isolated",
                "choices": {
                    "Notify authority": {"next": "end_good", "score": +20, "log": "Legal protocol followed"},
                    "Decrypt yourself": {"next": "end_bad", "score": -15, "log": "Failed attempt"}
                }
            },
            "restore": {
                "text": "Restore in progress",
                "choices": {
                    "Post-incident review": {"next": "end_good", "score": +20, "log": "Security culture improved"},
                    "No further steps": {"next": "end_bad", "score": -10, "log": "Complacency risk"}
                }
            },
            "end_good": {
                "text": "Simulation complete. You handled it well!",
                "choices": {}
            },
            "end_bad": {
                "text": "Simulation complete. You need better practices.",
                "choices": {}
            }
        }

    def make_choice(self, choice_text):
        node = self.scenario[self.current_node]
        choice = node["choices"].get(choice_text)
        if not choice:
            return False

        self.logs.append(f"[{time.strftime('%H:%M:%S')}] {choice['log']}")
        self.score += choice["score"]
        self.path.append(self.current_node)
        self.current_node = choice["next"]

        return True

    def get_current_state(self):
        node = self.scenario[self.current_node]
        return {
            "text": node["text"],
            "choices": list(node["choices"].keys()),
            "score": self.score,
            "logs": self.logs,
            "is_end": not bool(node["choices"])
        }

    def get_final_report(self):
        return {
            "score": self.score,
            "logs": self.logs,
            "path": self.path,
            "ended_at": self.current_node
        }
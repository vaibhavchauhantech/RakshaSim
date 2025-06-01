import json
import time

class SimulationEngine:
    def __init__(self, scenario_file):
        with open(scenario_file, 'r') as f:
            self.scenario = json.load(f)
        self.state = {
            'current_step': self.scenario['start'],
            'history': [],
            'start_time': time.time()
        }

    def get_current_step(self):
        step_id = self.state['current_step']
        return self.scenario['steps'].get(step_id, {})

    def make_choice(self, choice_id):
        current = self.get_current_step()
        if 'choices' not in current or choice_id not in current['choices']:
            return {'error': 'Invalid choice'}
        
        next_step = current['choices'][choice_id]['next']
        self.state['history'].append({
            'step': self.state['current_step'],
            'choice': choice_id,
            'timestamp': time.time()
        })
        self.state['current_step'] = next_step
        return self.get_current_step()

    def is_complete(self):
        return self.get_current_step().get('type') == 'end'

    def get_history(self):
        return self.state['history']
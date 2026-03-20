import json
import time

class MetadataEngine:
    def __init__(self):
        self.logs = {
            "system_decisions": [],
            "performance_metrics": {},
            "extraction_stats": {}
        }

    def record_decision(self, module, decision, rationale):
        self.logs["system_decisions"].append({
            "timestamp": time.time(),
            "module": module,
            "decision": decision,
            "rationale": rationale
        })

    def export(self, path="output/metadata.json"):
        with open(path, 'w') as f:
            json.dump(self.logs, f, indent=4)
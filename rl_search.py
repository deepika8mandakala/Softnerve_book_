# utils/rl_search.py

import json
import os

REWARD_PATH = "C:\Users\manda\Softnerve_updated\rating.txt"

class RLSearchAgent:
    def __init__(self):
        self.rewards = {}

    def load_rewards(self):
        if os.path.exists(REWARD_PATH):
            with open(REWARD_PATH, 'r') as f:
                self.rewards = json.load(f)
        else:
            self.rewards = {}

    def save_rewards(self):
        with open(REWARD_PATH, 'w') as f:
            json.dump(self.rewards, f, indent=4)

    def give_feedback(self, version_id, score):
        self.rewards[version_id] = score
        print(f"[✓] Feedback recorded: {version_id} → {score}")

    def rank_versions(self, chroma_results):
        ranked = []
        for i in range(len(chroma_results['documents'][0])):
            version_id = chroma_results['ids'][0][i]
            doc = chroma_results['documents'][0][i]
            meta = chroma_results['metadatas'][0][i]
            reward = self.rewards.get(version_id, 0.0)
            ranked.append((version_id, doc, meta, reward))
        return sorted(ranked, key=lambda x: x[3], reverse=True)
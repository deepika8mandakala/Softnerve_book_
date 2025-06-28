# Continuing from `apply_human_feedback` in ai_processor.py
# + Next steps + Integration with MAB + Humanization + Gemini fallback

import random
import json
import os
from datetime import datetime
from config import Config
import anthropic

class AIProcessor:
    def __init__(self):
        self.config = Config()
        self.client = anthropic.Anthropic(api_key=self.config.ANTHROPIC_API_KEY)
        self.stats_file = os.path.join(self.config.OUTPUT_DIR, "mab_stats.json")
        self.arm_stats = self.load_mab_stats()

    def load_mab_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, "r") as f:
                return json.load(f)
        return {
            "claude": [self.config.MAB_ALPHA, self.config.MAB_BETA],
            "gemini": [self.config.MAB_ALPHA, self.config.MAB_BETA]
        }

    def save_mab_stats(self):
        with open(self.stats_file, "w") as f:
            json.dump(self.arm_stats, f, indent=2)

    def select_model_mab(self) -> str:
        # Thompson Sampling
        samples = {
            model: random.betavariate(alpha, beta)
            for model, (alpha, beta) in self.arm_stats.items()
        }
        return max(samples, key=samples.get)

    def update_mab(self, model_name: str, success: bool):
        if success:
            self.arm_stats[model_name][0] += 1  # Increment alpha
        else:
            self.arm_stats[model_name][1] += 1  # Increment beta
        self.save_mab_stats()

    def revise_with_feedback(self, content: str, feedback: str) -> str:
        prompt = f"""
        You are a professional editor. Improve the content below by applying the human feedback, while enhancing clarity, tone, and engagement.
        Avoid direct copying. Use a natural and human-like style.

        ### Content:
        {content}

        ### Feedback:
        {feedback}

        Provide only the improved content, no explanations.
        """
        try:
            model_choice = self.select_model_mab()
            print(f" Using model: {model_choice}")

            if model_choice == "claude":
                response = self.client.messages.create(
                    model=self.config.MODEL_NAME,
                    max_tokens=self.config.MAX_TOKENS,
                    temperature=0.6,
                    messages=[{"role": "user", "content": prompt}]
                )
                revised = response.content[0].text

            elif model_choice == "gemini":
                # Gemini stub (replace with real API integration if needed)
                revised = content + "\n(Note: Gemini editing fallback simulated.)"

            self.update_mab(model_choice, True)
            return revised

        except Exception as e:
            print(f" Model {model_choice} failed: {e}")
            self.update_mab(model_choice, False)
            return content

# Next Steps - common_pipeline.py (general orchestrator)
"""
1. `common_pipeline.py` will:
   - Trigger `scraper.py` to get new chapter.
   - Call `ai_processor.py` to rewrite content.
   - Run `review_content` and log feedback.
   - Allow CLI input for human feedback.
   - Re-run `revise_with_feedback` with MAB model selection.

2. Output organized in `output/spun_content_<timestamp>.json`
3. Track model performance in `output/mab_stats.json`
"""

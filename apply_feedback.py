# apply_feedback.py

import os
import json
from ai_processor import AIProcessor
from datetime import datetime

OUTPUT_DIR = "output"

def get_latest_session_folder():
    session_folders = [
        os.path.join(OUTPUT_DIR, d) for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d)) and d.startswith("session_")
    ]
    if not session_folders:
        raise FileNotFoundError(" No session folders found. Run common_pipeline.py first.")
    return max(session_folders, key=os.path.getmtime)

def load_edited_content(edited_file):
    if not os.path.exists(edited_file):
        raise FileNotFoundError(f" {edited_file} not found. Make sure spinning is done first.")
    with open(edited_file, "r", encoding="utf-8") as f:
        return f.read()

def get_feedback():
    print("\n Enter your review feedback (e.g., 'Make it more concise, fix grammar.'):\n")
    return input("> ")

def save_final_output(session_folder, text, feedback, edited_file):
    final_file = os.path.join(session_folder, "final_revised.txt")
    feedback_file = os.path.join(session_folder, "review_feedback.json")

    # Save final revised version
    with open(final_file, "w", encoding="utf-8") as f:
        f.write(text)

    # Save feedback metadata
    feedback_data = {
        "timestamp": datetime.now().isoformat(),
        "feedback": feedback,
        "source_file": edited_file,
        "output_file": final_file
    }
    with open(feedback_file, "w", encoding="utf-8") as f:
        json.dump(feedback_data, f, indent=2)

    print(f"\n Final version saved to: {final_file}")
    print(f"  Feedback metadata saved to: {feedback_file}")

def main():
    session_folder = get_latest_session_folder()
    edited_file = os.path.join(session_folder, "edited_spin.txt")

    content = load_edited_content(edited_file)
    feedback = get_feedback()
    processor = AIProcessor()
    final = processor.revise_with_feedback(content, feedback)

    save_final_output(session_folder, final, feedback, edited_file)

if __name__ == "__main__":
    main()

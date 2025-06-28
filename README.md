 # ✅ Softnerve Book Content Enhancement Platform

This project implements a robust, AI-driven content pipeline designed to scrape, rewrite, review, rank, and continuously improve book chapters. It leverages human feedback and a sophisticated multi-model selection strategy using **Reinforcement Learning (RL)** and **Multi-Armed Bandits (MAB)**, specifically **Thompson Sampling**, to optimize content quality.

---

## 🚀 Features

* **📚 Web Scraping**: Automatically scrapes target book chapters using `playwright` and `bs4`.
* **✍️ AI-Powered Rewriting & Revision**: Utilizes **Anthropic Claude** for content rewriting and incorporates human feedback for iterative improvements. The system is also **Gemini-ready** for future integration.
* **🧠 Dynamic Model Selection**: Employs **Thompson Sampling Multi-Armed Bandit (MAB)** for intelligent selection between AI models (e.g., Claude, Gemini) based on their performance metrics.
* **🔁 Human-in-the-Loop Feedback**: Integrates a clear human feedback loop to guide content refinement and ensure quality.
* **🏆 RL-Based Version Ranking**: Ranks different content versions based on real-time feedback scores, allowing for continuous improvement and selection of the best outputs.
* **💾 Vector Retrieval**: Uses **ChromaDB** for efficient storage and retrieval of content versions and embeddings.
* **✅ Modular and Reusable**: Designed as a modular Python pipeline for easy maintenance and expansion.

---

## 🛠️ Tech Stack

This platform is built with a powerful combination of modern AI and data management technologies:

| Layer            | Technologies Used                                  | AI Models                                   |
| :--------------- | :------------------------------------------------- | :------------------------------------------ |
| **Backend** | Python 3.12                                        |                                             |
| **AI Models** |                                                    | **Anthropic Claude**, **Gemini** (stub for future), **BGE-Base embedding** |
| **Web Scraping** | `playwright`, `bs4`                                |                                             |
| **LLM Access** | `anthropic`, `openai`                              |                                             |
| **Vector Store** | `chromadb`                                         |                                             |
| **RL/MAB** | Custom RL Search Agent & **Thompson Sampling** Logic |                                             |
| **Storage** | Local JSON files + Screenshot logs                 |                                             |
| **Version Control** | Git                                                |                                             |

---

## 📂 Folder Structure

```bash
Softnerve_book/
│
├── ai_processor.py         # Claude+Gemini editor + MAB logic for content generation
├── apply_feedback.py       # Applies human feedback to iteratively improve content
├── common_pipeline.py      # Orchestrates the full content generation and refinement process
├── config.py               # Centralized configuration for environment variables and constants
├── rl_search.py            # Reinforcement Learning agent to rank content versions based on rewards
├── scraper.py              # Handles web scraping of book chapter content
├── mab_stats.json          # Stores statistics for Multi-Armed Bandit (MAB) model performance (e.g., alpha, beta for Thompson Sampling)
├── rating.txt              # Manual score logs for content versions (for human review)
├── requirements.txt        # Lists all required Python libraries and dependencies
├── output/                 # Directory for generated output (e.g., spun, revised content)
├── screenshots/            # Stores visual screenshots of scraped chapters for review
└── .git/                   # Git repository metadata
```
## 🔁 Full Pipeline Overview
The content enhancement pipeline follows a systematic multi-stage process:

1. Scrape Content:

- A URL is pulled from config.py.

- HTML content is scraped and then converted to raw text.

> Output File: raw_scraped.txt

2. Spin Content (AI Rewriting):

- Anthropic Claude (or a selected model via MAB) rewrites the raw content based on predefined prompts.

> Output File: edited_spin.txt

3. Review Content (AI Feedback Generation):

- Claude or Gemini generates improvement suggestions for the rewritten content.

> Output File: review_feedback.json

4. Human Feedback Loop:

- apply_feedback.py processes human feedback to refine the content.

> Output File: final_revised.txt

5. Reinforcement Ranking:

- rl_search.py utilizes an RL agent to rank all generated content versions based on accumulated feedback scores.

> Output File: feedback_rewards.json (Reward scores for RL ranking)

6. Model Selection (Thompson Sampling MAB):

- The system uses Thompson Sampling within the MAB framework to dynamically select the best-performing AI model (e.g., Claude vs. Gemini) for the next iteration, adapting based on success rates over time.

Example **mab_stats.json** structure:
```
{
  "claude": [5, 2],  // alpha (successes), beta (failures) for Claude
  "gemini": [2, 5]   // alpha, beta for Gemini
}
```
## How to Run
Follow these steps to set up and run the content enhancement pipeline:
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set environment variables:
Make sure to replace your_key_here with your actual API keys
```
export ANTHROPIC_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here
```
3. Run the main pipeline:
This script orchestrates the scraping, AI rewriting, and initial feedback generation.
```
python common_pipeline.py
```
4. Apply feedback:
After reviewing the content and providing feedback, run this to apply the revisions.
```
python apply_feedback.py
```
5. Perform reinforcement-based retrieval:
This step handles the ranking and selection of the best content versions.
```

python rl_search.py
```
### Flowchart :
```

Start
    ↓
Scrape Chapter Text (WebScraper using Playwright) → raw_scraped.txt
    ↓
Store Raw Content (raw_scraped.txt)
    ↓
Select AI Model (Claude / Gemini) → via Thompson Sampling (MAB)
    ↓
Rewrite Content with AI → edited_spin.txt
    ↓
Generate Feedback Suggestions (Claude/Gemini) → review_feedback.json
    ↓
Apply Human Feedback (apply_feedback.py) → final_revised.txt
    ↓
Rank Versions Using RL (rl_search.py) → feedback_rewards.json
    ↓
Display Ranked Versions → Save Best Version
    ↓
End
```
## 📈 Model Selection: Thompson Sampling
The pipeline uses a Multi-Armed Bandit approach to select between models dynamically, adapting based on success rates over time.
```
"claude": [5, 2],  # alpha, beta
"gemini": [2, 5]
```



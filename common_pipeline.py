import os
import asyncio
import datetime
import json
from scraper import WebScraper
from ai_processor import AIProcessor
from config import Config
import chromadb
chroma_client = chromadb.PersistentClient(path="./chromadb_storage")

#  Create or get a collection to store versioned files
collection = chroma_client.get_or_create_collection(name="versioned_files")
def create_session_folder():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join("output", f"session_{timestamp}")
    os.makedirs(folder, exist_ok=True)
    return folder

def save_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as jf:
        json.dump(data, jf, indent=2, ensure_ascii=False)

def run_pipeline():
    config = Config()
    scraper = WebScraper()
    ai = AIProcessor()
    session_folder = create_session_folder()

    print(" Scraping content...")
    url = config.TARGET_URL
    raw_data = asyncio.run(scraper.scrape_content(url))  # returns dict

    # Save full dict as JSON
    json_path = os.path.join(session_folder, "raw_scraped.json")
    save_json(json_path, raw_data)

    # Save just the text content
    raw_path = os.path.join(session_folder, "raw_scraped.txt")
    raw_text = raw_data["content"]
    save_file(raw_path, raw_text)

    print(f" Raw content saved to {raw_path}")

    print(" Spinning content...")
    edited_content = ai.revise_with_feedback(raw_text, "Spin this professionally.")
    edited_path = os.path.join(session_folder, "edited_spin.txt")
    save_file(edited_path, edited_content)

    print(f" Edited content saved to {edited_path}")

if __name__ == "__main__":
    run_pipeline()

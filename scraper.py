import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
from config import Config

class WebScraper:
    def __init__(self):
        self.config = Config()
        self.config.create_directories()
        
    async def scrape_content(self, url: str) -> dict:
        """Scrape content and take screenshots from the given URL"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Set to True for production
            page = await browser.new_page()
            
            try:
                # Navigate to page
                await page.goto(url, wait_until="networkidle")
                await page.wait_for_timeout(2000)  # Wait for page to fully load
                
                # Take screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(
                    self.config.SCREENSHOTS_DIR, 
                    f"chapter_screenshot_{timestamp}.png"
                )
                await page.screenshot(path=screenshot_path, full_page=True)
                
                # Extract content
                content = await page.content()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extract main content (adjust selector TARGETd on WikiSource structure)
                main_content = soup.find('div', {'class': 'mw-parser-output'})
                if not main_content:
                    main_content = soup.find('div', {'id': 'mw-content-text'})
                
                text_content = main_content.get_text(strip=True) if main_content else ""
                
                # Extract title
                title_elem = soup.find('h1', {'class': 'firstHeading'}) or soup.find('title')
                title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
                
                result = {
                    'url': url,
                    'title': title,
                    'content': text_content,
                    'html': str(main_content) if main_content else "",
                    'screenshot_path': screenshot_path,
                    'scraped_at': timestamp,
                    'word_count': len(text_content.split())
                }
                
                # Save raw content
                content_file = os.path.join(
                    self.config.OUTPUT_DIR,
                    f"raw_content_{timestamp}.json"
                )
                with open(content_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f" Scraped content: {len(text_content)} characters")
                print(f" Screenshot saved: {screenshot_path}")
                print(f" Content saved: {content_file}")
                
                return result
                
            except Exception as e:
                print(f" Error scraping {url}: {str(e)}")
                raise
            finally:
                await browser.close()

# Test function
async def test_scraper():
    scraper = WebScraper()
    config = Config()
    result = await scraper.scrape_content(config.TARGET_URL)
    print(f"Scraped: {result['title']}")
    return result

if __name__ == "__main__":
    asyncio.run(test_scraper())
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator
from dotenv import load_dotenv
import os
import sys

load_dotenv()

jobsite = os.getenv("JOBSITE")
if not jobsite:
    raise ValueError("JOBSITE environment variable not set")

async def scrape(website: str, browser_config, run_config):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=website, config=run_config)
        return result.markdown


browser_config = BrowserConfig(
    enable_stealth=True,
    headless=False,
    viewport={
        "width": 800,
        "height": 600,
    },
)

# jobcard_ids = [f"#jobcard-{i}" for i in range(1, 51)]
# css_selector_string = ", ".join(jobcard_ids)

run_config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown_generator=DefaultMarkdownGenerator(
        options={
            "fit_html": True,
            "ignore_images": True
        }
    ),
    excluded_tags=["form", "header", "footer", "nav", "ul"],
)
        
def get_jobs(page: int = 1):
    website = jobsite
    if page > 1:
        # Add page to query
        website = f"{website}?page={page}"

    return asyncio.run(scrape(website, browser_config, run_config))

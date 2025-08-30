import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator
import os

jobsite = os.getenv("JOBSITE")
if not jobsite:
    raise ValueError("JOBSITE environment variable not set")



browser_config = BrowserConfig(
    enable_stealth=True,
    headless=True,
    viewport={
        "width": 800,
        "height": 600,
    },
)

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

async def scrape(website: str, browser_config, run_config):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=website, config=run_config)
        return result.markdown

       
def get_jobs(page: int = 1):
    website = jobsite
    if page > 1:
        # Add page to query
        website = f"{website}?page={page}"

    return asyncio.run(scrape(website, browser_config, run_config))
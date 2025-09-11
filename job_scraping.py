import asyncio
import logging
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator
import os

# Suppress crawl4ai logs to prevent TUI interference
logging.getLogger('crawl4ai').setLevel(logging.ERROR)
logging.getLogger('playwright').setLevel(logging.ERROR)
logging.getLogger('selenium').setLevel(logging.ERROR)

jobsite = os.getenv("JOBSITE")
if not jobsite:
    raise ValueError("JOBSITE environment variable not set")

browser_config = BrowserConfig(
    enable_stealth=True,
    headless=False,
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

async def _run_scrape_jobs(website: str):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=website, config=run_config)
        return result.markdown

async def scrape_jobs(page: int):
    website = jobsite
    if page > 1:
        if "?" in website:
            website = f"{website}&page={page}"
        else:
            website = f"{website}?page={page}"
    return await _run_scrape_jobs(website)

async def _run_scrape_job_description(link: str):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=link, config=run_config)
        return result.markdown

async def scrape_job_description(link: str):
    return await _run_scrape_job_description(link)
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator
from dotenv import load_dotenv
import os
import sys

load_dotenv()

jobsite = os.getenv("JOBSITE")
if not jobsite:
    raise ValueError("JOBSITE environment variable not set")

    
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
async def get_jobs(page: int = 1):
    browser_config = BrowserConfig(
        enable_stealth=True,
        headless=False,
        viewport={
            "width": 800,
            "height": 600,
        },
    )

    jobcard_ids = [f"#jobcard-{i}" for i in range(1, 51)]
    css_selector_string = ", ".join(jobcard_ids)

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

    website = jobsite
    if page > 1:
        # Add page to query
        website = f"{website}?page={page}"

    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=website, config=run_config)

        # Print the extracted content
        print(result.markdown)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(get_jobs(page=1))
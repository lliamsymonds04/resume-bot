import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from dotenv import load_dotenv
import os

load_dotenv()

jobsite = os.getenv("JOBSITE")
if not jobsite:
    raise ValueError("JOBSITE environment variable not set")


async def main():
    browser_config = BrowserConfig(
        enable_stealth=True,
        headless=False,
    )

    run_config = CrawlerRunConfig()
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=jobsite, run_config=run_config)

        # Print the extracted content
        print(result.markdown)

# Run the async main function
asyncio.run(main())
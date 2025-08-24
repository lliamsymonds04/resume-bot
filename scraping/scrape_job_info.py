import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator


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

async def scrape(link: str, browser_config, run_config):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=link, config=run_config)
        print(result.markdown)

def scrape_job_info(link: str):
    asyncio.run(scrape(link, browser_config, run_config))
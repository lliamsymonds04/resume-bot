import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator

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
    excluded_tags=["form", "header", "footer", "nav"],
)

async def scrape(link: str, browser_config, run_config):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=link, config=run_config)
        return result.markdown

# def scrape_job_info(link: str):
#     return asyncio.run(scrape(link, browser_config, run_config))

async def scrape_job_info(link: str):
    return await scrape(link, browser_config, run_config)
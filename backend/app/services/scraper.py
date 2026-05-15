import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright


async def scrape_search_results(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    results = []
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0"
        )
        page = await context.new_page()

        try:
            await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_selector("div#search", timeout=10000)

            elements = await page.query_selector_all("div.g")
            for i, el in enumerate(elements[:max_results]):
                try:
                    title_el = await el.query_selector("h3")
                    title = await title_el.inner_text() if title_el else "No title"

                    link_el = await el.query_selector("a")
                    href = await link_el.get_attribute("href") if link_el else ""

                    snippet_el = await el.query_selector("div.VwiC3b")
                    snippet = await snippet_el.inner_text() if snippet_el else ""

                    results.append({
                        "title": title,
                        "url": href,
                        "snippet": snippet,
                    })
                except Exception:
                    continue

        except Exception as e:
            results.append({"error": str(e), "title": "Scrape failed", "url": "", "snippet": ""})

        finally:
            await browser.close()

    return results

import asyncio
import json
import re
from urllib.parse import urljoin

from crawl4ai import AsyncWebCrawler

BASE_URL = "https://www.bankofamerica.com"
START_URL = "https://www.bankofamerica.com/credit-cards/"


def clean(text):
    """Remove markdown formatting."""
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = text.replace("**", "")
    return text.strip()


async def main():

    async with AsyncWebCrawler() as crawler:

        print("Fetching landing page...")

        result = await crawler.arun(url=START_URL)

        if not result.success:
            print("Failed")
            return

        markdown = result.markdown

        # -----------------------------
        # Find all card links
        # -----------------------------

        pattern = r"\[(.*?)\]\((https://www\.bankofamerica\.com/credit-cards/products/.*?)\)"

        matches = re.findall(pattern, markdown)

        card_links = {}

        for title, url in matches:
            card_links[url] = clean(title)

        print(f"Found {len(card_links)} cards")

        cards = []

        # -----------------------------
        # Visit every card page
        # -----------------------------

        for url, title in card_links.items():

            print("Scraping:", title)

            page = await crawler.arun(url=url)

            if not page.success:
                continue

            text = clean(page.markdown)

            category = ""

            if "travel" in url:
                category = "Travel Rewards"

            elif "cash" in url:
                category = "Cash Back"

            elif "student" in url:
                category = "Students"

            elif "airline" in url:
                category = "Airline Rewards"

            elif "points" in url:
                category = "Points Rewards"

            elif "interest" in url:
                category = "Lower Interest"

            benefits = ""
            rewards = ""
            rates = ""

            lines = text.split("\n")

            for line in lines:

                line = line.strip()

                if len(line) < 20:
                    continue

                if not benefits:
                    benefits = line

                if "reward" in line.lower():
                    rewards += line + " "

                if (
                    "apr" in line.lower()
                    or "annual fee" in line.lower()
                    or "interest" in line.lower()
                ):
                    rates += line + " "

            cards.append(
                {
                    "card_name": title,
                    "category": category,
                    "benefits": benefits,
                    "rewards": rewards.strip(),
                    "rates_fees": rates.strip(),
                    "source": url,
                }
            )

    with open("scraped_data/cards.json", "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=4, ensure_ascii=False)

    print(f"\nSaved {len(cards)} cards")


if __name__ == "__main__":
    asyncio.run(main())

# import os
# import json
# import asyncio
# from pydantic import BaseModel, Field

# from crawl4ai import AsyncWebCrawler, CacheMode
# from crawl4ai.async_configs import CrawlerRunConfig
# from crawl4ai.extraction_strategy import (
#     LLMExtractionStrategy,
#     create_llm_config,
# )


# # -----------------------------
# # Schema
# # -----------------------------
# class CreditCardSchema(BaseModel):
#     card_name: str = Field(
#         ..., description="Official name of the credit card"
#     )

#     category: str = Field(
#         ..., description="Cash Back, Travel Rewards, Student, etc."
#     )

#     features: str = Field(
#         ..., description="Main earning features"
#     )

#     benefits: str = Field(
#         ..., description="Bonuses and card benefits"
#     )

#     rates_fees: str = Field(
#         ..., description="APR, annual fee and other fees"
#     )

#     product_url: str = Field(
#         ..., description="Product page URL if available"
#     )


# # -----------------------------
# # Crawl + Extract
# # -----------------------------
# async def crawl_cards():

#     url = "https://www.bankofamerica.com/credit-cards/"

#     groq_key = os.getenv("GROQ_API_KEY")

#     if not groq_key:
#         raise ValueError("GROQ_API_KEY is not set.")

#     llm_config = create_llm_config(
#         provider="groq/llama-3.3-70b-versatile",
#         api_token=groq_key,
#     )

#     extraction_strategy = LLMExtractionStrategy(

#         llm_config=llm_config,

#         extraction_type="schema",

#         schema=CreditCardSchema.model_json_schema(),

#         input_format="fit_markdown",

#         instruction="""
# Extract every Bank of America credit card from this page.

# Return ONLY a JSON array.

# For every card include:

# - card_name
# - category
# - features
# - benefits
# - rates_fees
# - product_url

# Ignore:

# - navigation
# - footer
# - advertisements
# - legal notices
# - unrelated content
# """,

#         verbose=True,
#     )

#     async with AsyncWebCrawler(verbose=True) as crawler:

#         result = await crawler.arun(

#             url=url,

#             config=CrawlerRunConfig(

#                 extraction_strategy=extraction_strategy,

#                 excluded_tags=[
#                     "nav",
#                     "footer",
#                     "script",
#                     "style",
#                 ],

#                 cache_mode=CacheMode.BYPASS,
#             ),
#         )

#     if not result.success:
#         raise RuntimeError(result.error_message)

#     try:

#         cards = json.loads(result.extracted_content)

#     except Exception:

#         print(result.extracted_content)
#         raise

#     return cards


# # -----------------------------
# # Main
# # -----------------------------
# async def main():

#     print("Extracting cards...")

#     cards = await crawl_cards()

#     os.makedirs("data", exist_ok=True)

#     with open(
#         "data/cards.json",
#         "w",
#         encoding="utf-8",
#     ) as f:

#         json.dump(
#             cards,
#             f,
#             indent=4,
#             ensure_ascii=False,
#         )

#     print()

#     print(f"Successfully extracted {len(cards)} cards.")

#     print("Saved to data/raw_data.json")


# if __name__ == "__main__":
#     asyncio.run(main())
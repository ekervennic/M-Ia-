import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    # Créer une instance de AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Crawler une URL
        result = await crawler.arun(url="https://crawl4ai.com")
        
        # Afficher le contenu extrait en Markdown
        print(result.markdown)

# Exécuter la fonction async
asyncio.run(main())
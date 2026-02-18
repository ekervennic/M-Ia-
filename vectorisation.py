# scraping.py - TON CODE ACTUEL
import asyncio
import re
from crawl4ai import AsyncWebCrawler

async def scraper_from_file():
    print("🎵 Scraper de paroles depuis toutes_20_pages.md\n")
    
    with open("toutes_20_pages.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    liens = re.findall(r'https://lyricstranslate\.com/en/[^)]+lyrics\.html', content)
    liens = list(set(liens))
    
    print(f"✅ {len(liens)} liens trouvés\n")
    
    choix = input(f"Combien scraper ? (max {len(liens)}, défaut 10) : ").strip()
    nb = int(choix) if choix.isdigit() else 10
    nb = min(nb, len(liens))
    
    print(f"\n🎵 Scraping de {nb} chansons...")
    
    markdown = "# Paroles de chansons françaises\n\n"
    markdown += f"**Total :** {nb} chansons\n\n"
    markdown += "---\n\n"
    
    success = 0
    async with AsyncWebCrawler(headless=True, verbose=False) as crawler:
        for i, url in enumerate(liens[:nb], 1):
            titre = url.split('/')[-1].replace('-lyrics.html', '').replace('-', ' ').title()
            progress = i / nb * 100
            print(f"[{i:3d}/{nb}] ({progress:5.1f}%) {titre[:50]}")
            
            try:
                result = await crawler.arun(url=url, bypass_cache=True)
                
                if result.success:
                    markdown += f"## {i}. {titre}\n\n"
                    markdown += f"**URL :** {url}\n\n"
                    markdown += "### Paroles\n\n"
                    markdown += result.markdown
                    markdown += "\n\n---\n\n"
                    
                    chars = len(result.markdown)
                    print(f" ✅ OK - {chars:,} caractères")
                    success += 1
                else:
                    print(f" ❌ Échec")
                
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f" ⚠️ Erreur : {str(e)[:40]}")
    
    filename = f"paroles_francaises_{nb}_chansons.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    print(f"\n{'='*70}")
    print(f"🎉 TERMINÉ !")
    print(f"📊 Résultats : {success}/{nb} ({success/nb*100:.0f}%)")
    print(f"📁 Fichier : {filename}")
    print(f"{'='*70}")
    
    return filename  # Retourne le nom du fichier pour l'étape suivante

asyncio.run(scraper_from_file())
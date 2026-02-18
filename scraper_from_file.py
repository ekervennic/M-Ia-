import asyncio
import re
from crawl4ai import AsyncWebCrawler

async def scraper_from_file():
    print("🎵 Scraper de paroles depuis toutes_20_pages.md\n")
    
    # Lire ton fichier
    with open("toutes_20_pages.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extraire tous les liens de chansons
    # Cherche tous les liens qui contiennent "lyrics"
    liens = re.findall(r'https://lyricstranslate\.com/en/[^)]+lyrics\.html', content)
    
    # Supprimer les doublons
    liens = list(set(liens))
    
    print(f"✅ {len(liens)} liens trouvés\n")
    
    # Demander combien scraper
    choix = input(f"Combien scraper ? (max {len(liens)}, défaut 10) : ").strip()
    nb = int(choix) if choix.isdigit() else 10
    nb = min(nb, len(liens))
    
    print(f"\n🎵 Scraping de {nb} chansons...")
    print(f"⏱️  Temps estimé : {nb * 2.5 / 60:.1f} minutes\n")
    
    # Fichier Markdown de sortie
    markdown = "# Paroles de chansons françaises\n\n"
    markdown += f"**Total :** {nb} chansons\n\n"
    markdown += "---\n\n"
    
    # Scraper chaque chanson
    success = 0
    
    async with AsyncWebCrawler(headless=True, verbose=False) as crawler:
        
        for i, url in enumerate(liens[:nb], 1):
            # Extraire le titre de l'URL
            titre = url.split('/')[-1].replace('-lyrics.html', '').replace('-', ' ').title()
            
            progress = i / nb * 100
            print(f"[{i:3d}/{nb}] ({progress:5.1f}%) {titre[:50]}")
            
            try:
                result = await crawler.arun(
                    url=url,
                    bypass_cache=True
                )
                
                if result.success:
                    # Ajouter au fichier Markdown
                    markdown += f"## {i}. {titre}\n\n"
                    markdown += f"**URL :** {url}\n\n"
                    markdown += "### Paroles\n\n"
                    markdown += result.markdown
                    markdown += "\n\n---\n\n"
                    
                    chars = len(result.markdown)
                    print(f"            ✅ OK - {chars:,} caractères")
                    success += 1
                else:
                    print(f"            ❌ Échec")
                
                # Pause entre requêtes (IMPORTANT !)
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"            ⚠️ Erreur : {str(e)[:40]}")
    
    # Sauvegarder le fichier final
    filename = f"paroles_francaises_{nb}_chansons.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    print(f"\n{'='*70}")
    print(f"🎉 TERMINÉ !")
    print(f"{'='*70}")
    print(f"📊 Résultats :")
    print(f"   Chansons scrapées : {success}/{nb}")
    print(f"   Taux de réussite : {success/nb*100:.0f}%")
    print(f"\n📁 Fichier créé :")
    print(f"   {filename}")
    print(f"   Taille : {len(markdown):,} caractères")
    print(f"{'='*70}")

asyncio.run(scraper_from_file())
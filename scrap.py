import requests
from bs4 import BeautifulSoup
import time

def scrape_song_urls(num_pages=20):
    """Récupérer toutes les URLs des chansons"""
    all_urls = []
    
    for page in range(1, num_pages + 1):
        url = f"https://lyricstranslate.com/fr/language/french-lyrics-page-{page}"
        print(f"📥 Page {page}/{num_pages}...")
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trouver les divs avec class="stt"
        for div in soup.find_all('div', class_='stt'):
            link = div.find('a', href=lambda x: x and 'lyrics.html' in x)
            if link:
                song_url = 'https://lyricstranslate.com' + link['href']
                if song_url not in all_urls:
                    all_urls.append(song_url)
        
        time.sleep(1)
    
    return all_urls

def scrape_song_page(url):
    """Récupérer les infos d'une chanson"""
    print(f" → {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Titre
        title = ''
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text(strip=True)
        
        # Artiste
        artist = ''
        artist_div = soup.find('div', class_='artist-title')
        if artist_div:
            artist_link = artist_div.find('a')
            if artist_link:
                artist = artist_link.get_text(strip=True)
        
        # Paroles
        lyrics = ''
        lyrics_div = soup.find('div', id='song-body')
        if lyrics_div:
            lyrics = lyrics_div.get_text(strip=True)
        
        return {
            'url': url,
            'title': title,
            'artist': artist,
            'lyrics': lyrics
        }
    
    except Exception as e:
        print(f" ❌ Erreur: {e}")
        return {
            'url': url,
            'title': '',
            'artist': '',
            'lyrics': ''
        }

def save_to_markdown(songs, filename='french_songs.md'):
    """Sauvegarder les chansons en Markdown"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 🎵 Chansons Françaises\n\n")
        f.write(f"*{len(songs)} chansons récupérées*\n\n")
        f.write("---\n\n")
        
        for i, song in enumerate(songs, 1):
            f.write(f"## {i}. {song['title']}\n\n")
            f.write(f"**Artiste:** {song['artist']}\n\n")
            f.write(f"**Lien:** [{song['url']}]({song['url']})\n\n")
            f.write("### Paroles\n\n")
            f.write(f"{song['lyrics']}\n\n")
            f.write("---\n\n")
    
    print(f"✅ Fichier sauvegardé: {filename}")

# Programme principal
print("🔍 Récupération des URLs des chansons...\n")
song_urls = scrape_song_urls(num_pages=20)  # Changez 20 par le nombre voulu
print(f"\n✅ {len(song_urls)} chansons trouvées\n")

print("📖 Récupération des paroles...\n")
all_songs = []
for i, url in enumerate(song_urls, 1):
    print(f"[{i}/{len(song_urls)}]")
    song_data = scrape_song_page(url)
    all_songs.append(song_data)
    time.sleep(1)

print("\n📄 Création du fichier Markdown...")
save_to_markdown(all_songs)
print(f"\n✅ {len(all_songs)} chansons sauvegardées dans french_songs.md 🎉")
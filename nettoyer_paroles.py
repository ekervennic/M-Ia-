import re

def nettoyer_paroles():
    print("🧹 Nettoyage du fichier de paroles\n")
    
    # Lire ton fichier avec tout le bazar
    print("📂 Lecture du fichier...")
    with open("paroles_francaises_1772_chansons.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"✅ Fichier chargé : {len(content):,} caractères\n")
    
    # Séparer par chanson (chaque chanson commence par "## [numéro].")
    print("✂️ Découpage en chansons...")
    chansons = re.split(r'\n(## \d+\..*?)\n', content)
    
    # Fichier propre
    markdown_propre = "# Paroles de chansons françaises\n\n"
    markdown_propre += "**Nettoyé automatiquement**\n\n"
    markdown_propre += "---\n\n"
    
    nb_chansons = 0
    
    print("🧼 Nettoyage en cours...\n")
    
    for i in range(1, len(chansons), 2):
        if i + 1 >= len(chansons):
            break
        
        titre_ligne = chansons[i]  # ## 1. Titre
        contenu_brut = chansons[i + 1]  # Tout le contenu
        
        # Extraire l'URL
        url_match = re.search(r'\*\*URL :\*\* (https://[^\s\)]+)', contenu_brut)
        url = url_match.group(1) if url_match else ""
        
        # Extraire le numéro de la chanson
        num_match = re.search(r'## (\d+)\.', titre_ligne)
        num = num_match.group(1) if num_match else str(nb_chansons + 1)
        
        # Chercher le début des paroles (après "### Paroles")
        debut_paroles = contenu_brut.find('### Paroles')
        
        if debut_paroles != -1:
            # Prendre tout après "### Paroles"
            apres_titre = contenu_brut[debut_paroles:]
            
            # Trouver la fin (avant le prochain "---" ou fin de texte)
            fin_match = re.search(r'\n---\n', apres_titre)
            if fin_match:
                paroles_brutes = apres_titre[:fin_match.start()]
            else:
                paroles_brutes = apres_titre
            
            # Enlever "### Paroles" du début
            paroles_brutes = paroles_brutes.replace('### Paroles', '', 1).strip()
            
            # Nettoyer ligne par ligne
            lignes = paroles_brutes.split('\n')
            lignes_propres = []
            
            # Mots/patterns à exclure
            patterns_interdits = [
                r'^\s*\[.*?\]\s*$',  # [Liens entre crochets]
                r'^\s*\*.*?\*\s*$',  # *Étoiles*
                r'https?://',        # URLs
                r'Log in|Sign up',
                r'Home|LyricsTranslate',
                r'Copyright|©',
                r'Privacy|Theme|Interface',
                r'Artists:|All\s+[A-Z]',
                r'^\s*!\[',          # Images ![
                r'Powered by',
                r'Add new|Request',
                r'Community|Forum',
                r'^\s*\|\s*$',       # Lignes vides avec |
                r'^\s*#{1,6}\s+Home',
                r'Do not share',
            ]
            
            for ligne in lignes:
                ligne_clean = ligne.strip()
                
                # Ignorer les lignes vides
                if len(ligne_clean) == 0:
                    continue
                
                # Vérifier si la ligne contient des patterns interdits
                contient_interdit = False
                for pattern in patterns_interdits:
                    if re.search(pattern, ligne_clean, re.IGNORECASE):
                        contient_interdit = True
                        break
                
                if not contient_interdit and len(ligne_clean) > 1:
                    lignes_propres.append(ligne_clean)
            
            # Reconstruire les paroles
            paroles_propres = '\n'.join(lignes_propres)
            
            # Ajouter au fichier propre seulement si on a du contenu significatif
            if len(paroles_propres) > 100:  # Au moins 100 caractères
                markdown_propre += titre_ligne + "\n\n"
                markdown_propre += f"**URL :** {url}\n\n"
                markdown_propre += "### Paroles\n\n"
                markdown_propre += paroles_propres
                markdown_propre += "\n\n---\n\n"
                
                nb_chansons += 1
                
                # Afficher progression
                if nb_chansons <= 5 or nb_chansons % 100 == 0:
                    print(f"✅ Chanson {nb_chansons} nettoyée : {titre_ligne.strip()[:50]}")
    
    # Sauvegarder
    filename = f"paroles_PROPRES_{nb_chansons}_chansons.md"
    
    print(f"\n💾 Sauvegarde du fichier propre...")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_propre)
    
    print(f"\n{'='*70}")
    print(f"🎉 NETTOYAGE TERMINÉ !")
    print(f"{'='*70}")
    print(f"📊 Statistiques :")
    print(f"   Chansons nettoyées : {nb_chansons}")
    print(f"   Fichier original : {len(content):,} caractères")
    print(f"   Fichier propre : {len(markdown_propre):,} caractères")
    print(f"   Réduction : {(1 - len(markdown_propre)/len(content))*100:.1f}%")
    print(f"\n📁 Fichier créé :")
    print(f"   {filename}")
    print(f"{'='*70}")

# Lancer le nettoyage
nettoyer_paroles()
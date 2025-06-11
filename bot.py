import requests
from bs4 import BeautifulSoup
import openai
import os

# Clé API OpenAI
openai.api_key = "votre clé OPEN AI"

# Webhook Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1377676325703254186/C9rF23LunHXJ10TETAnvyE9UK7rMbA9NifNNeIlpRAg6_22pCdzsIkZ-bLUItX2R5ge9"

# Fichier pour suivre les articles déjà envoyés
ENVOYES_PATH = "articles_envoyes.txt"

def get_article_links():
    url = "https://connect.ed-diamond.com/misc/misc-139"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = set()
    for article_block in soup.select("a[href^='/misc/misc-139/']"):
        href = article_block.get("href")
        if href and href.count("/") == 3:
            full_url = "https://connect.ed-diamond.com" + href.strip()
            links.add(full_url)

    return list(links)

def extract_article_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Titre introuvable"

    content_div = soup.find("div", class_="truncated_body")
    content = content_div.get_text(separator="\n", strip=True) if content_div else "Contenu introuvable"

    return {
        "url": url,
        "title": title,
        "content": content
    }

def generate_summary(text):
    prompt = f"Voici le contenu d’un article technique. Résume-le de manière claire et concise en quelques lignes :\n\n{text[:3000]}\n\nRésumé :"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Erreur IA : {e}"

def send_to_discord(title, url, summary):
    payload = {
        "content": f" **Nouvel article analysé :** {title}\n🔗 {url}\n **Résumé IA :**\n{summary}"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f" Erreur Discord : {response.status_code} - {response.text}")
    except Exception as e:
        print(f" Exception Discord : {e}")

def charger_articles_envoyes():
    if not os.path.exists(ENVOYES_PATH):
        return set()
    with open(ENVOYES_PATH, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def enregistrer_article_envoye(url):
    with open(ENVOYES_PATH, "a", encoding="utf-8") as f:
        f.write(url + "\n")

if __name__ == "__main__":
    articles_existants = charger_articles_envoyes()
    tous_les_articles = get_article_links()
    nouveaux_articles = [link for link in tous_les_articles if link not in articles_existants]

    print(f"{len(nouveaux_articles)} nouvel(s) article(s) détecté(s).\n")

    for link in nouveaux_articles:
        print(f"---\nScraping : {link}")
        data = extract_article_data(link)
        print(f"Titre : {data['title']}")
        print(f"Contenu (début) :\n{data['content'][:300]}...\n")

        summary = generate_summary(data['content'])
        print(f"Résumé IA :\n{summary}\n")

        send_to_discord(data['title'], data['url'], summary)
        enregistrer_article_envoye(link)

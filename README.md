# Scraping & Notification Discord avec Résumé IA

## Objectif du projet

Automatiser une veille technologique à partir du site connect.ed-diamond.com
Il permet de :

- Scraper les nouveaux articles techniques publiés
- Générer un résumé automatique avec une clé OpenAI
- Envoyer une notification via Discord Webhook

## Technologies utilisées

`Python`

Langage principal

`OpenAI API`

Génération de résumé

`Discord Webhook`

Notification

## Fonctionnement général

### 1.  **Récupération des liens d’articles**

-   L’URL cible est :  `https://connect.ed-diamond.com/misc/misc-139`
    
-   On extrait les liens valides qui correspondent à des articles en utilisant un filtre CSS sur les balises  `<a>`.
    

soup.select("a[href^='/misc/misc-139/']")

----------

### 2.  **Extraction des données**

-   Pour chaque lien :
    
    -   On extrait le  **titre**  (`<h1>`)
        
    -   On extrait le  **contenu principal**  (div avec class  `truncated_body`)

### 3.  **Génération d’un résumé**

-   Le contenu est tronqué à 3000 caractères (limite API OpenAI).
    
-   Un prompt est envoyé au modèle  `gpt-3.5-turbo`  pour générer un résumé synthétique.
    

prompt = f"Voici le contenu d’un article technique. Résume-le..."`

### 4.  **Envoi sur Discord**

-   Format du message :
```python    
`**Nouvel  article  analysé :** [Titre]  [Lien]  **Résumé IA :** [Résumé généré]
```
    
-   Utilise l’URL Webhook pour la publication dans un canal Discord.
    

----------

### 5.  **Évitement des doublons**

-   Les articles déjà envoyés sont listés dans un fichier texte  `articles_envoyes.txt`.
    
-   Le script les compare aux nouveaux articles détectés pour éviter toute redondance.

-----

### 6. **Exemple**

On peux visiter l'URL cible pour analyser les différents article présent

[![Image](https://i.goopics.net/7eibzu.png)](https://goopics.net/i/7eibzu)

Nous avons un total de 8 articles en plus de celui présenté sur la page, cela nous donne un total de 9 articles.

On execute maintenant le code et on obtiens le résultat suivant :
[![Image](https://i.goopics.net/ngwc4e.png)](https://goopics.net/i/ngwc4e)

On trouve bien les 9 articles et comme pour l'exemple ainsi qu'un titre, contenu et résumé pour chaque articles.

Le fichier article_envoyes.txt à également été alimenté.
[![Image](https://i.goopics.net/jthru1.png)](https://goopics.net/i/jthru1)

De ce fait, si on réexécute le code :

[![Image](https://i.goopics.net/ef5dvd.png)](https://goopics.net/i/ef5dvd)

Aucun nouveau article n'est présent sur le site, comme ils sont tous déjà présent dans le fichier.txt, il ne sont pas récupérer de nouveau.

Un planificateur de tache à été mis en place 1 fois par mois afin de rester à jour sur les articles.

Le code étant lié à un webhook discord, celui est alimenté lorsque le code est exécuté est une notification est envoyé.

[![Image](https://i.goopics.net/4v81tr.png)](https://goopics.net/i/4v81tr)

---
### Conclusion

Ce projet démontre l’efficacité d’un système de veille technologique automatisé alliant scraping web, intelligence artificielle et notifications en temps réel. Grâce à Python, l’intégration de l’API OpenAI et l’usage des webhooks Discord, le processus de suivi et de diffusion des nouveaux articles techniques est entièrement automatisé, synthétisé et centralisé.




 

# Compte Rendu de Projet – Scraping & Notification Discord avec Résumé IA

##  Objectif du projet

Ce projet a pour but d’automatiser la veille technologique à partir du site **[connect.ed-diamond.com](https://connect.ed-diamond.com)**. Il permet de :

-   Scraper les nouveaux articles techniques publiés,
    
-   Générer un résumé automatique de leur contenu avec une clé **OpenAI**,
    
-   Envoyer une notification enrichie via **Discord Webhook**.
    

----------

##  Technologies utilisées


`Python`

Langage principal

`OpenAI API`

Génération de résumé

`Discord Webhook`

Notification

----------

##  Fonctionnement général

### 1. **Récupération des liens d’articles**

-   L’URL cible est : `https://connect.ed-diamond.com/misc/misc-139`
    
-   On extrait les liens valides qui correspondent à des articles en utilisant un filtre CSS sur les balises `<a>`.
    
```python
soup.select("a[href^='/misc/misc-139/']")
``` 


----------

### 2. **Extraction des données**

-   Pour chaque lien :
    
    -   On extrait le **titre** (`<h1>`)
        
    -   On extrait le **contenu principal** (div avec class `truncated_body`)
        

----------

### 3. **Génération d’un résumé**

-   Le contenu est tronqué à 3000 caractères (limite API OpenAI).
    
-   Un prompt est envoyé au modèle `gpt-3.5-turbo` pour générer un résumé synthétique.
    

```python
prompt = f"Voici le contenu d’un article technique. Résume-le..."` 
```

----------

### 4. **Envoi sur Discord**

-   Format du message :
    
    ```less
    `**Nouvel  article  analysé :** [Titre]  [Lien]  **Résumé IA :** [Résumé généré]`
    ```
    
-   Utilise l’URL Webhook pour la publication dans un canal Discord.
    

----------

### 5. **Évitement des doublons**

-   Les articles déjà envoyés sont listés dans un fichier texte `articles_envoyes.txt`.
    
-   Le script les compare aux nouveaux articles détectés pour éviter toute redondance.
    

----------

##  Résultat

-   **Articles automatiquement scrappés, résumés, et publiés sur Discord**
    
-   **Gain de temps** pour la veille technique
    
-   **Approche modulaire et évolutive**
    

----------

## Points forts

-   Intégration d’un modèle IA pour apporter de la valeur ajoutée.
    
-   Système de filtrage intelligent pour ne pas renvoyer les mêmes articles.
    
-   Utilisation d’un Webhook Discord pour une notification directe en équipe.
    

----------

## Organisation des fichiers

```text
`project/
│
├── main.py               # Script principal
├── articles_envoyes.txt  # Liste des articles déjà traités`
```

    

----------
Un planificateur de tache à été mis en place et le code est "automatiquement" mis a jour quand un nouvel article apparaît.

# TODO

## Podcast Page Enhancements
- [ ] Add a player on the search page
- [ ] Need to definitively fix the play/pause button that is constantly broken the play/pause action shall be in a more robust way.
- [x] Add a search button for local search on the podcase page in addition to the search in all episodes.
- [x] Ajouter un bouton avec une icône aléatoire sur la page podcast 
      pour sélectionner aléatoirement une saison et un épisode.
- [x] Lors de la saisie manuelle de la saison, empêcher le collapse automatique. 
      Ne le faire que lors de la sélection d'un épisode.
- [ ] Ajouter un bouton pour partager une page sur toutes les pages
- [ ] Ajouter une page de description pour chaque podcast avec des statistiques et 
      des informations sur le podcast. Ainsi que quelques search fights sympas en liens qui serons stocké dans le json des podcasts.
- [ ] Ajouter le moyen de proposer des modifications. 
    - [ ] PR automatique?
    - [ ] Formulaire qui génère un mail? 
    - [ ] Formulaire qui génère un ticket sur le repo?
    - [ ] Permet d'ajouter la personne qui parle
    - [ ] Permet de corriger le transcript ou sa traduction
    - Possible de faire des PR anonymes?
- [ ] On index.html can you :
      - add a list view in addition to the card view
      - add the number of transcript and translated podcast 150 [C 100 T 90] with hover hint C is converted to text, T is translated.  
## Python Scripts
- [ ] Modifier les scriptes pour qu'ils travaillent dans le dossier podcast directement.
- [ ] Créer un script Python pour vérifier si les épisodes sont présents localement :
  - Si absent, les ajouter au fichier JSON.
  - Télécharger l'épisode.
  - Transcrire l'épisode.
  - Traduire l'épisode.
- [ ] Écrire un script Python pour remplir le fichier JSON avec la durée des épisodes.
- [x] Update each episode with the duration in the JSON file reading the content of the info file.

## Voice Model
- [ ] Créer un modèle de voix à partir des sons.


# The WeasyPrint :books: Matrix Robots :robot: Project

### Pourquoi ce projet ?

L'objectif initial était juste de pouvoir générer un fichier PDF à partir d'une documentation MkDocs. J'ai essayé le plugin MkPDFs qui nécessite quelques ajustements pour fonctionner correctement car il n'est pas vraiment maintenu. 

Ces ajustements ont été l'occasion de découvrir WeasyPrint et d'appréhender peu à peu tout son potentiel pour la génération de documents à partir d'`HTML` et de `CSS`.

WeasyPrint prend en entrée un et un seul fichier HTML. L'HTML ne comprenant pas d'instruction d'import (include ou autre), il est nécessaire de produire un fichier monolithique comportant des centaines de lignes pour la génération du PDF d'un document comportant de nombreuses pages.

D'où l'idée de la création d'un système beaucoup plus modulaire et souple à l'aide d'une **Matrice WeasyPrint** servant à construire un fichier HTML et un fichier CSS servant d'entrée à WeasyPrint.

* MkDocs : https://www.mkdocs.org/
* MkPDFs https://comwes.github.io/mkpdfs-mkdocs-plugin/
* WeasyPrint : https://weasyprint.org/

### Objectifs

En découpant le projet en différentes parties indépendantes, il est possible de :
1. faciliter l'écriture et la maintenance du code
1. pouvoir travailler en équipe en utilisant Git
1. offrir des possiblités d'héritage et de réécriture de *templates* ou de contenu
1. offrir un cadre générique pour :
    * exporter des données depuis d'autres applications (mon export MkDocs de départ :wink:)
    * partager des *templates* utilisables et adaptables sans programmation

## La Matrice WeasyPrint

Elle est organisée en lignes et colonnes et chaque cellule peut contenir :
* du contenu : `content.hmtl`
* de la mise en forme (style) : `print.scss`
* des métadonnées : `meta.html`
* des fichiers associés (essentiellement polices et images)

Elle est parcourue dans le sens des lignes puis des colonnes (**héritage**), si plusieurs fichiers `content.hmtl` ou `print.scss` existent sur la même ligne c'est le dernier qui est sélectionné (**réécriture**). Pour les métadonnées `meta.html`, c'est dernier fichier trouvé qui est retenu.

C'est très facile à visualiser grâce au fichier <a href="https://htmlpreview.github.io/?https://github.com/FrancoisCapon/TheWeasyPrintMatrixRobotsProject/blob/master/matrices/courtbouillon-report/weasyprint/matrix.html" target="_blank">matrix.html</a> produit lors de l'impression (au sens génération du PDF).

### Création

A partir de la racine d'une matrice, les dossiers et fichiers sont à organisés de la manière suivante :

#### colonnes
C'est le premier niveau de dossier, les noms des dossiers doivent commener par un nombre sur deux chiffres suivi d'un tiret (exemple `05-` ou `75-`), la suite est libre.

Il est impératif de respecter l'unicité des numéros de colonnes (deux `10-..` n'est pas possible)

#### cellules
C'est le second niveau de dossiers, les noms des dossiers doivent commencer par un nombre sur quatre chiffres suivi d'un tiret (exemple `0005-` ou `7500-`), la suite est libre. Ces quatres chiffres correspondent au numéro de la ligne de la cellule.

Il est impératif de respecter l'unicité des numéros de lignes au sein d'une même colonne (deux `4040-..` n'est pas possible).

Il est par contre tout à fait possible d'avoir deux numéros de ligne identiques dans deux colonnes différentes, c'est ce qui permet la **réécriture**.

### Exemples

```
.
├── 05-template-base
│   ├── 1010-root-variables
│   │   └── print.scss
│   ├── 1020-fonts
│   │   ├── firasans-bold.otf
│   │   ├── firasans-italic.otf
│   │   ├── firasans-lightitalic.otf
│   │   ├── firasans-light.otf
│   │   ├── firasans-regular.otf
│   │   └── print.scss
│   ├── 1030-pages
│   │   └── print.scss
│   └── 1040-content
│       └── print.scss
├── 10-template-report
│   ├── 1010-variables
│   │   └── print.scss
│   ├── 1030-pages
│   │   └── print.scss
│   ├── 1100-page--cover
│   │   ├── content.html
│   │   ├── print.scss
│   │   └── report-cover.jpg
│   ├── 1200-page--toc
│   │   └── print.scss
│   └── 1800-pdf-bookmarks
│       └── print.scss
...
├── 30-content-report
│   ├── 3010-toc-meta
│   │   ├── content.html
│   │   └── meta.html
│   ├── 3100-columns
│   │   ├── content.html
│   │   └── print.scss
│   ├── 3110-skills
│   │   ├── content.html
│   │   ├── heading.svg
│   │   ├── internal-links.svg
│   │   ├── multi-columns.svg
│   │   ├── print.scss
│   │   ├── style.svg
│   │   └── table-content.svg
│   ├── 3120-offers
│   │   ├── content.html
│   │   └── print.scss
...
```

Deux exemples de matrices sont présents dans le dossier `matrices` du projet, ils intégrent les différentes possibilités offertes.

### Impression

L'impression est réalisé par les robots, le robot manager ne "fait rien" mais il a la "lourde tâche" de coordonner le travail des autres robots :
1. le `retriever` parcourt les dossiers pour identifier les colonnes, les lignes et la présence des fichiers (contenu, style et meta) dans les cellules 
1. le `preparer` demande à la matrice quels sont les fichiers retenus et prépare en mémoire :
    * le futur fichier `weasyprint.html`
    * la liste des fichiers `printnnnn.scss`
    * par convention les nom des fichiers contenu dans `src='fichier'` ou `url('fichier')` sont considérés comme relatifs, le `preparer` va le transformer en chemin absolu
        * la solution est simpliste mais suffisante pour une version de "démarrage" de projet
1. le `writer` écrit dans le dossier `weasyprint` de la matrice les fichiers nécessaires à l'impression :
    * le fichier `weasyprint.html` (nom des fichiers d'origine des parties indiqués en commentaire)
    * les fichiers `print.scss` et `printnnnn.scss`, il les compile en `weasyprint.css` (idem)
    * fichiers de la matrice 
        * `matrix.html` pour visualisation utilisateur
        * `matrix.db3` pour débuggage
1. le `printer` imprime le document dans le fichier PDF `weasyprint.pdf` à l'aide de WeasyPrint (`weasyprint.html` et `weasyprint.css` en entrée), les éventuels problèmes d'impression sont journalisés dans `weasyprint.log`.

## FAQ

#### Comment désactiver une colonne ou une cellule ?
En préfixant son nom par `Z` (par exemple) et elle ne sera pas prise en compte.

#### Faut-il connaitre SASS ?
Pas du tout, SASS est un sur-ensemble de CSS donc il est possible de travailler en CSS uniquement.

#### Est-ce que je peux stocker des fichiers en dehors des cellules ?
Tout à fait, dans l'exemple `madcats-book`, les images communes aux chapitres sont stockées dans un dossier spécifique `40-book-chapters/images/` puis référencées de manière relative dans les cellules `<img src='../images/cat-john.png' />`

#### Et l'héritage extra matrice ?
Il suffit d'utiliser des liens symboliques vers des "dossiers externes" pour mettre en commun des colonnes : **réutilisabilité**

#### Est-ce que le projet fonctionne en dehors d'un container ?
Je n'ai pas essayé, mais le code s'appuie sur la bibliothèque `os.path` et j'utilise systématiquement `os.sep`. Donc, si `weasyprint` est installé ainsi que `sass`, les robots doivent être en mesure d'effectuer leur travail.
* https://doc.courtbouillon.org/weasyprint/stable/first_steps.html
* https://sass-lang.com/install

## Utilisation avec le container Docker

### Création de l'image

Lancement de la construction à partir de la racine du projet

```
$ git clone https://github.com/FrancoisCapon/TheWeasyPrintMatrixRobotsProject
$ cd ./TheWeasyPrintMatrixRobotsProject
$ docker build -t fcapon/weasyprintmatrixrobots .
```

### Démarrage du container

Le container est démarré à la racine du projet et la présence de `weasyprint` et `sass` sont confirmées.

```
$ docker run -it -v $(pwd):/project fcapon/weasyprintmatrixrobots
root@0b004447b473:/project# weasyprint --version
WeasyPrint version 54.2
root@0b004447b473:/project# sass --version
1.49.9
```
### Installation du module `weasyprintmatrixrobots` ("mode développement")

```
root@0b004447b473:/project# pip install -e weasyprintmatrixrobots/
Obtaining file:///project/weasyprintmatrixrobots
Installing collected packages: weasyprintmatrixrobots
  Running setup.py develop for weasyprintmatrixrobots
Successfully installed weasyprintmatrixrobots
root@0b004447b473:/project# pip freeze | grep weasy
weasyprint==54.2
weasyprintmatrixrobots @ file:///project/weasyprintmatrixrobots
```

### Impression des exemples

```
root@0b004447b473:/project# cd matrices/courtbouillon-report/
root@0b004447b473:/project/matrices/courtbouillon-report# ./print.py
root@0b004447b473:/project/matrices/courtbouillon-report# cd ../madcats-book/
root@0b004447b473:/project/matrices/madcats-book# ./print.py 
```

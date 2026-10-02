Source: https://no-sleep-pika.online/guide/fr/keep-mac-awake/
Language: fr

MAC GUIDE · 2026-10-02

# Empêcher un Mac de se mettre en veille : écran fermé, caffeinate et pika

Comparez le mode capot fermé avec alimentation, les commandes Terminal et pika. Découvrez les conditions, les limites et la manière de terminer chaque session.

## Choisir selon le besoin

Écran éteint, verrouillage et veille du système sont différents. Un Mac verrouillé peut continuer à travailler. Utilisez le mode capot fermé pour un écran externe, caffeinate pour une tâche temporaire capot ouvert, ou pika avec son service auxiliaire pour travailler fermé sans écran externe.

## 1. Alimentation et mode capot fermé

Capot ouvert, branchez l’alimentation, un écran compatible, le clavier et la souris, puis vérifiez leur fonctionnement avant de fermer. Un écran fournissant du courant peut remplacer le chargeur selon ses caractéristiques. Le chargeur seul ne suffit pas. Le nombre d’écrans et leur résolution dépendent du modèle. Autorisez les accessoires avant de fermer.

[Apple · External displays](https://support.apple.com/en-us/102501)

## Réglages avec le capot ouvert

Sur un portable branché, cherchez dans Réglages Système → Batterie → Options le réglage empêchant la veille automatique lorsque l’écran est éteint. Son emplacement varie selon macOS et le modèle. Conservez le mot de passe au verrouillage. Cela ne garantit pas d’empêcher la veille déclenchée par la fermeture du capot. Notez les anciens réglages.

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. Utiliser caffeinate temporairement

Ouvrez Terminal et lancez la commande ci-dessous. caffeinate est intégré à macOS et ne demande pas sudo. Il empêche la veille d’inactivité, mais l’écran peut s’éteindre. Gardez le processus actif et utilisez Contrôle+C dans ce Terminal pour l’arrêter. L’absence de message est normale. La demande disparaît quand le processus se termine.

```
caffeinate -i
```

## Durée, écran et commande

Le premier exemple dure 3 600 secondes, soit une heure. Le deuxième maintient aussi l’écran pendant 1 800 secondes, soit trente minutes ; retirez -d si inutile. Le troisième exécute réellement make et accompagne sa durée : utilisez-le seulement pour compiler le projet voulu. Un lanceur quittant immédiatement peut finir avant la tâche réelle. L’option -t n’est pas utilisée lorsqu’une commande est lancée.

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## Et lorsque le capot est fermé ?

-i concerne la veille d’inactivité du système et -d celle de l’écran. Fermer le capot est une autre condition : ces options ne garantissent pas le fonctionnement fermé sans écran externe. -s ne vaut que sur secteur ; -u signale une activité et peut rallumer l’écran. Choisissez les options selon leur fonction.

## 3. Installer pika

pika prend en charge macOS 13 et versions ultérieures, Apple Silicon et Intel. Son PKG officiel complet installe l’app et le service auxiliaire administrateur. Effectuez vous-même l’authentification et les autorisations nécessaires. Ouvrez /Applications/pika.app, vérifiez le service, activez Session, choisissez Monitor OFF si nécessaire, puis fermez le capot. La prévention est préparée avant ; la politique d’affichage est appliquée après fermeture. Capot ouvert, Monitor enregistre seulement le choix. Session OFF restaure le réglage géré sans éteindre immédiatement l’écran. Fermer la fenêtre ne quitte pas l’app.

[Télécharger pika · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[Aide à l’installation](https://no-sleep-pika.online/install/)

## Vérifier puis arrêter

Testez une courte tâche en notant l’heure et vérifiez ses journaux après l’attente. Cette procédure ne signifie pas que tous les modèles ont été testés. pmset -g assertions lit les demandes existantes sans les modifier ; il ne prouve pas la continuité réseau ni le fonctionnement capot fermé. man caffeinate ouvre le manuel local.

```
pmset -g assertions
```

```
man caffeinate
```

## Verrouillage, réseau et chaleur

Un verrouillage n’est pas forcément une veille. Wi-Fi, VPN, limites d’API, autorisations en attente et erreurs peuvent interrompre le travail. pika ne poursuit pas les conversations IA et ne rétablit pas le réseau. Utilisez une surface ferme et ventilée, jamais un sac. Batterie, protection thermique ou panne du service peuvent arrêter la session ; aucune garantie contre toute surchauffe ou décharge n’est donnée.

## Sources et portée

Comparaison rédigée par le créateur de no-sleep-pika, incluant sa propre app. Sources : Apple, manuel macOS caffeinate(8), documentation et code de pika 1.0.13. Il ne s’agit pas d’une recommandation d’Apple ou d’un fournisseur d’IA. Limitez la session à la durée nécessaire.

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

Rédigé par le créateur de no-sleep-pika ; présente notre app.

[Télécharger pika](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[Guide du MacBook fermé →](https://no-sleep-pika.online/guide/fr/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/fr/keep-mac-awake/index.md)

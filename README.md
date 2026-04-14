# 🔍 SQLi Scanner Pro

> Détecteur de vulnérabilités **SQL Injection** basique en ligne de commande.

---

## ⚠️ Avertissement légal

> **Cet outil est destiné exclusivement à des fins éducatives et à des tests de sécurité sur des systèmes dont vous avez l'autorisation explicite d'auditer.**
> Toute utilisation non autorisée sur des systèmes tiers est illégale et contraire à l'éthique. L'auteur décline toute responsabilité pour un usage abusif.

---

## 📋 Description

SQLi Scanner Pro est un outil léger en Python qui tente de détecter des vulnérabilités **SQL Injection** dans les paramètres GET d'une URL cible, en injectant des payloads courants et en analysant les messages d'erreur renvoyés par le serveur.

Bases de données détectées :
- MySQL
- PostgreSQL
- Microsoft SQL Server
- Oracle

---

## 🚀 Installation

**Prérequis :** Python 3.x

```bash
# Cloner le dépôt
git clone https://github.com/Maxime288/sqli-scanner.git
cd sqli-scanner

# Installer les dépendances
pip install requests
```

---

## 🛠️ Utilisation

```bash
python sqli_scanner.py -u "http://exemple.com/page.php?id=1"
```

### Options

| Option | Description |
|--------|-------------|
| `-u`, `--url` | URL cible avec paramètre(s) GET *(obligatoire)* |
| `-h`, `--help` | Affiche l'aide |

### Exemple de sortie

```
[*] Analyse de l'URL : http://exemple.com/page.php?id=1
[*] Test du paramètre : id

[VULNÉRABLE] Injection possible !
  Paramètre : id
  Payload   : '
  Type DB   : MySQL

Terminé en 1.23s
```

---

## ⚙️ Fonctionnement

1. L'outil extrait les paramètres GET de l'URL fournie.
2. Pour chaque paramètre, il injecte une série de payloads (`'`, `"`, `';`, etc.).
3. La réponse HTTP est analysée à la recherche de messages d'erreur SQL caractéristiques.
4. Si une erreur est détectée, le paramètre vulnérable, le payload et le type de base de données sont affichés.

---

## 📦 Structure du projet

```
sqli-scanner/
├── sqli_scanner.py   # Script principal
└── README.md
```

---

## 🔒 Limites

- Détection basée uniquement sur les **erreurs SQL visibles** (error-based).
- Ne couvre pas les injections **blind**, **time-based** ou **out-of-band**.
- Ne teste que les paramètres **GET** (pas POST, cookies, headers).
- Conçu à des fins pédagogiques, non pour un usage en production.

---

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

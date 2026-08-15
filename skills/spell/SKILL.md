---
name: spell
description: Prüft und korrigiert deutsche Texte, Lebensläufe (src/*.md), Anschreiben und Templates auf Rechtschreibung (Rechtschreibung), Grammatik (Grammatik), Zeichensetzung (Kommasetzung), IT-Komposita und Schweizer Rechtschreibregeln (konsequent ss statt ß, Bindestriche).
---

# Skill: Rechtschreib- & Stilprüfung (Spell & Style Checker)

Dieser Skill führt eine systematische und pedantische Sprach- und Rechtschreibprüfung für Bewerbungsunterlagen, Markdown-Dateien und LaTeX-Vorlagen durch.

## Prüfungsdimensionen & Regeln

### 1. Schweizer Orthografie & Typografie (Standard)
- **Kein `ß`:** Konsequente Verwendung von `ss` (z. B. *gross*, *schliessen*, *massgeschneidert*, *einschliesslich*, *ausserdem*, *Prozess*).
- **Bindestriche statt Gedankenstriche:** Ausschliesslich Standard-Bindestriche (`-` bzw. `--` in LaTeX) für Zeiträume (z. B. `2022--heute`, `1997--2001`) und Trennungen verwenden, niemals echte Geviert- oder Halbgeviertstriche (`–` / `—`).
- **Anführungszeichen:** Entweder französische Guillemets (`«...»`) oder neutrale Anführungszeichen (`"..."`).

### 2. IT-Begriffe, Anglizismen & Komposita-Kopplung
- **Kopplung mehrteiliger englischer/deutscher IT-Begriffe:**
  - *Richtig:* `End-to-End-Prozess`, `Second-Level-Support`, `Data-Warehouse-Architektur`, `Python-Skripte`, `Kunden-Workshops`, `SQL-Abfragen`, `Java-basiert`
  - *Falsch:* `End to End Prozess`, `Second Level Support`, `Python Skripte`, `SQL Abfragen`
- **Deutsche Zusammenschreibung:**
  - *Richtig:* `systemübergreifend`, `geschäftskritisch`, `dokumentenbasiert`, `evidenzbasiert`, `regulatorisch`

### 3. Grammatik & Interpunktion
- **Kommasetzung:**
  - Vor erweiterten Infinitiven mit *zu* (*„...mit dem Ziel, Prozesse zu automatisieren“*).
  - Vor Nebensätzen (*dass*, *weil*, *um zu*, *obwohl*).
  - Aufzählungen und gleichrangige Teilsätze.
- **Gross-/Kleinschreibung:**
  - Substantivierte Verben (*beim Einführen*, *das Testen*, *zur Optimierung*).
  - Eigennamen und Fachabkürzungen (*PL/SQL*, *REST APIs*, *YAML*, *JSON*).

### 4. CV-Stil & Satzbau
- **Aktionsorientierte Formulierungen:** Bullet-Points mit starken Nomen/Verben einleiten (*Konzeption*, *Einführung*, *Leitung*, *Entwicklung*, *Optimierung*).
- **Konsistente Satzstrukturen:** Einheitliche Endungen (kein Mix aus ganzen Sätzen und Stichworten innerhalb einer Liste).

---

## Workflow

1. **Datei einlesen:** Datei aus `$ARGUMENTS` (oder standardmässig alle Dateien in `src/*.md`) laden.
2. **Prüfen:** Zeile für Zeile gegen die 4 Prüfungsdimensionen abgleichen.
3. **Ergebnisbericht erstellen:**
   - **Tabelle der Fundstellen:**
     - *Zeile / Kontext*
     - *Aktueller Text*
     - *Korrekturvorschlag*
     - *Regel / Begründung*
   - **Gesamtfazit:** Sprachliche Qualitätseinschätzung (fehlerfrei / Korrekturbedarf).
4. **Korrektur:** Auf Wunsch Korrekturen direkt in die betroffene Datei übernehmen und das PDF neu kompilieren.

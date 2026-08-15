---
name: test
description: Orchestriert eine ganzheitliche Qualitätsprüfung eines Lebenslaufs, indem nacheinander die Skills fit, audit, spell und links ausgeführt werden und deren Ergebnisse als kompakte Zusammenfassung mit Status-Ampel dargestellt werden.
---

# Skill: Lebenslauf QA & Test-Workflow (test)

Dieser Skill dient als reiner **Workflow-Orchestrator** ohne eigene Geschäftslogik. Er führt nacheinander die 4 etablierten Prüf-Skills aus und aggregiert die Ergebnisse in einer kompakten, übersichtlichen Management-Zusammenfassung (Dashboard).

---

## Ablauf des Workflows

Bei Aufruf von `/test` bzw. `/test <target>` (z. B. `/test example`) werden folgende Prüfungen sequenziell durchlaufen:

1. **🎯 Fit (`fit`):**
   - Abgleich des Lebenslaufs (`src/cv-<target>.md`) mit der Stellenausschreibung (`jobs/<target>.md`).
   - Match-Score (Must-Have, Nice-to-Have, Rollen-Fit, ATS-Keywords).

2. **🛡️ Audit (`audit`):**
   - Prüfung der Angaben gegen die Belege in `docs/` (Zeugnisse, Zertifikate, Ausbildungen).
   - Trust-Score & Gap-Analyse.

3. **✍️ Rechtschreibung & Stil (`spell`):**
   - Überprüfung auf Schweizer Rechtschreibung (`ss` statt `ß`), Bindestriche (`--`), IT-Komposita und Kommasetzung.

4. **🔗 Links & Kontakte (`links`):**
   - Technische Erreichbarkeit und syntaktische Korrektheit aller URLs und E-Mail-Adressen im PDF (`dist/*.pdf`).

---

## Ausgabeformat (Kompaktes QA-Dashboard)

Der Skill gibt ausschliesslich die aggregierte Zusammenfassung der 4 Module aus:

```markdown
# 📋 Gesamtergebnis Qualitätsprüfung: [Target-Name]

## 🚦 Executive Dashboard

| Prüf-Dimension | Modul | Score / Status | Ampel | Kernbefund / Fazit |
| :--- | :---: | :---: | :---: | :--- |
| **1. Stellen-Fit** | `fit` | XX % | 🟢/🟡/🔴 | [Kurzfazit zu Must-Haves & ATS] |
| **2. Dossier-Belege** | `audit` | XX % | 🟢/🟡/🔴 | [Kurzfazit zu Zeugnissen & Gaps] |
| **3. Rechtschreibung & Stil** | `spell` | XX Befunde | 🟢/🟡/🔴 | [Kurzfazit zu Orthografie & Stil] |
| **4. Links & Kontakte** | `links` | X/X OK | 🟢/🟡/🔴 | [Kurzfazit zu URLs & Mailto] |

---

## 📌 Modul-Zusammenfassungen

### 1. 🎯 Fit & Matching (Score: XX %)
- **Stärken:** [1-2 Sätze zu den stärksten Übereinstimmungen]
- **Optimierungspotenzial:** [1-2 konkrete Anpassungsempfehlungen]

### 2. 🛡️ Trust & Belegbarkeit (Score: XX %)
- **Belegte Stationen & Abschlüsse:** [Kurzer Status]
- **Hinweise / Gaps:** [Eventuelle Unstimmigkeiten oder unbelegte Punkte]

### 3. ✍️ Rechtschreibung, Kommas & Schweizer Orthografie
- **Status:** [Fehlerfrei oder Liste der konkreten Korrekturen]

### 4. 🔗 Hyperlinks & E-Mail-Adressen
- **Status:** [Erreichbarkeit aller Links im PDF]

---
💡 **Gesamtempfehlung:** [1 abschliessender Satz zur Freigabe / Bewerbungsreife]
```

---

## Aufruf

- `/test` (prüft Standard-Lebenslauf `example`)
- `/test example`
- `/test <target>`

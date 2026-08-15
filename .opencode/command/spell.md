---
description: Führt eine pedantische Rechtschreib-, Grammatik- und Schweizer Orthografieprüfung (ss statt ß) für Markdown- und TeX-Dateien durch.
---

Führe eine gründliche Rechtschreib- und Grammatikprüfung gemäss dem Skill `spell` durch.

Prüfe die angegebene Datei "$ARGUMENTS" (falls leer, prüfe alle Dateien in `src/*.md` und `templates/*.tex`).

Achte besonders auf:
1. Schweizer Orthografie: Konsequent `ss` statt `ß`, keine Gedankenstriche (`–`), nur normale Bindestriche (`-` bzw. `--` in LaTeX).
2. IT-Komposita & Anglizismen: Korrekte Durchkopplung mit Bindestrich (z.B. `Python-Skripte`, `End-to-End-Prozess`, `Data-Warehouse-Abfragen`).
3. Kommasetzung und Grammatik.
4. Stilistische Konsistenz der Aufzählungspunkte.

Gib das Ergebnis in einer strukturierten Tabelle aus:
- Fundstelle (Datei / Zeile)
- Aktueller Text
- Korrekturvorschlag
- Regel / Begründung

Biete abschliessend an, gefundene Korrekturen direkt anzuwenden und die PDFs neu zu kompilieren.

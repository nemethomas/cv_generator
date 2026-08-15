---
description: Führt den ganzheitlichen QA-Workflow (fit, audit, spell, links) durch und liefert ein kompaktes Dashboard.
---

Führe den ganzheitlichen QA- und Test-Workflow gemäss dem Skill `test` für "$ARGUMENTS" durch.

**Ziel-Lebenslauf:**
- Falls ein Argument angegeben ist (z. B. `example` oder ein spezifischer Name), prüfe diesen Lebenslauf.
- Falls kein Argument angegeben ist, prüfe standardmässig `example`.

**Ablauf (sequenziell):**
1. **🎯 Fit (`fit`):** Match gegen `jobs/<target>.md` (Must-Have, Nice-to-Have, Rollen-Fit, ATS-Keywords).
2. **🛡️ Audit (`audit`):** Trust-Check gegen Nachweise in `docs/` (Zeugnisse, Zertifikate, CAS).
3. **✍️ Rechtschreibung & Stil (`spell`):** Schweizer Orthografie (`ss`), Komposita, Bindestriche (`--`).
4. **🔗 Links & Kontakte (`links`):** Prüfung aller Hyperlinks im PDF (`dist/<target>.pdf`).

Gib das Ergebnis als kompaktes **Executive Dashboard** mit Status-Ampeln und Kernbefunden aus.

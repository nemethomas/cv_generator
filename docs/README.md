# Nachweise & Dokumente (docs/)

In diesem Ordner werden persönliche Nachweise, Diplome, Arbeitszeugnisse und Zertifikate abgelegt.

Das integrierte OCR- und Sync-Werkzeug fasst alle Nachweise automatisch in einer einzigen, durchsuchbaren Markdown-Datei **`docs/dossier.md`** zusammen. Diese dient den Skills **`audit`**, **`fit`** und **`scout`** als blitzschnelle Evidenz-Basis.

## Empfohlene Ordnerstruktur

- `docs/zeugnisse/` – Arbeitszeugnisse (Zwischen- und Schlusszeugnisse, z. B. `2024_Firma_Arbeitszeugnis.pdf`)
- `docs/zertifikate/` – Fachzertifikate (z. B. IREB, IPMA, ITIL, Scrum, Cloud)
- `docs/ausbildung/` – Diplome, Notenausweise & Nachweise (CAS, Bachelor, Master, EFZ, Maturität)
- `docs/sprachen/` – Sprachdiplome (z. B. Cambridge First, DELF)

## Dokumente importieren & synchronisieren

Sobald neue PDF-Dokumente abgelegt wurden:
```bash
# Via Make:
make dossier
# oder
make sync

# Via Python direkt:
python3 skills/audit/sync_dossier.py

# Via Opencode-Befehl:
/audit sync
```
Das Skript erkennt automatisch, ob Text im PDF vorliegt oder führt via nativer macOS Apple Vision Engine eine lokale OCR-Textextraktion durch.

> **Sicherheitshinweis:** Der Ordner `docs/` sowie die generierte `docs/dossier.md` enthalten vertrauliche Personendaten und sind in der `.gitignore` vollständig geschützt.

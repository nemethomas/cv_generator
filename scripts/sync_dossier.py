#!/usr/bin/env python3
"""
Dossier Sync & OCR Extractor for CV Documents.
Scans docs/ (zeugnisse, ausbildung, zertifikate, sprachen), performs high-precision
text extraction (pypdf + native macOS Apple Vision OCR for image scans), aggregates
everything into docs/dossier.md, and automatically extracts docs/profile.json.
"""

import sys
import os
import re
import json
import subprocess
from pathlib import Path

try:
    import pypdf
except ImportError:
    pypdf = None

BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "docs"
DOSSIER_FILE = DOCS_DIR / "dossier.md"

# Import profile extractor from same scripts folder
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from extract_profile import build_profile, PROFILE_FILE

SWIFT_OCR_SCRIPT = r"""
import Foundation
import Vision
import PDFKit
import AppKit

guard CommandLine.arguments.count > 1 else { exit(1) }
let pdfPath = CommandLine.arguments[1]
let url = URL(fileURLWithPath: pdfPath)
guard let doc = PDFDocument(url: url) else { exit(1) }

for pageIdx in 0..<doc.pageCount {
    guard let page = doc.page(at: pageIdx) else { continue }
    let pageRect = page.bounds(for: .mediaBox)
    let targetSize = NSSize(width: max(1200, pageRect.width * 2.5), height: max(1600, pageRect.height * 2.5))
    let image = page.thumbnail(of: targetSize, for: .mediaBox)
    guard let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    
    let request = VNRecognizeTextRequest()
    request.recognitionLanguages = ["de-CH", "de-DE", "en-US", "fr-FR"]
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    
    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try? handler.perform([request])
    
    if let observations = request.results {
        let text = observations.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
        print("--- PAGE \(pageIdx + 1) ---")
        print(text)
    }
}
"""


def extract_text_pypdf(pdf_path):
    """Extract text stream from PDF if available."""
    if not pypdf:
        return ""
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        text_parts = []
        for idx, page in enumerate(reader.pages):
            txt = page.extract_text()
            if txt and len(txt.strip()) > 30:
                text_parts.append(f"--- PAGE {idx + 1} ---\n" + txt.strip())
        return "\n\n".join(text_parts)
    except Exception:
        return ""


def extract_text_ocr(pdf_path):
    """Perform native macOS Vision OCR via Swift."""
    try:
        res = subprocess.run(
            ["swift", "-e", SWIFT_OCR_SCRIPT, str(pdf_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if res.returncode == 0 and len(res.stdout.strip()) > 20:
            return res.stdout.strip()
    except Exception as e:
        print(f"Warnung bei OCR für {pdf_path.name}: {e}", file=sys.stderr)
    return ""


def extract_document_text(pdf_path):
    """Extract text from PDF using pypdf first, falling back to Apple Vision OCR."""
    text = extract_text_pypdf(pdf_path)
    # If text is too short or likely a scanned image, use Vision OCR
    if len(text.strip()) < 80:
        ocr_text = extract_text_ocr(pdf_path)
        if len(ocr_text.strip()) > len(text.strip()):
            text = ocr_text
    return text.strip()


def format_doc_entry(category, pdf_file, raw_text):
    """Format single document into clean Markdown section."""
    rel_path = pdf_file.relative_to(DOCS_DIR)
    clean_title = pdf_file.stem.replace("_", " ")

    clean_text = raw_text.strip()
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)

    entry = f"### 📄 {clean_title}\n\n"
    entry += f"- **Kategorie:** `{category}`\n"
    entry += f"- **Quelldatei:** `{rel_path}`\n\n"
    entry += "#### Extrahierter Originaltext / Nachweis\n\n"
    entry += "```text\n"
    entry += clean_text if clean_text else "[Kein Text extrahierbar]"
    entry += "\n```\n\n---\n\n"
    return entry


def sync_dossier(output_file=DOSSIER_FILE):
    """Scan docs/ and regenerate docs/dossier.md, then build docs/profile.json."""
    if not DOCS_DIR.exists():
        print(f"Fehler: Ordner {DOCS_DIR} existiert nicht.", file=sys.stderr)
        return False

    categories = [
        ("zeugnisse", "1. Arbeitszeugnisse"),
        ("ausbildung", "2. Aus- und Weiterbildung (Diplome & Noten)"),
        ("zertifikate", "3. Fachzertifikate & Nachweise"),
        ("sprachen", "4. Sprachzertifikate")
    ]

    content = "# 🗂️ Zentrales Nachweis- & Evidenz-Dossier (docs/dossier.md)\n\n"
    content += "Dieses Dokument aggregiert alle im Ordner `docs/` hinterlegten Zeugnisse, Diplome und Zertifikate.\n"
    content += "Es dient als ultraschnelle, strukturierte Single Source of Truth für die Skills **`audit`**, **`fit`** und **`scout`**.\n\n"
    content += "> **Sicherheitshinweis:** Diese Datei enthält vertrauliche Personendaten und wird via `.gitignore` geschützt.\n\n"
    content += "---\n\n"

    total_docs = 0

    for cat_dir_name, cat_title in categories:
        cat_path = DOCS_DIR / cat_dir_name
        pdf_files = sorted(list(cat_path.glob("*.pdf"))) if cat_path.exists() else []

        content += f"## {cat_title}\n\n"

        if not pdf_files:
            content += "_Keine Dokumente in dieser Kategorie vorhanden._\n\n---\n\n"
            continue

        for pdf_file in pdf_files:
            total_docs += 1
            print(f"[{total_docs}] Extrahiere: {pdf_file.name} ...")
            raw_text = extract_document_text(pdf_file)
            entry = format_doc_entry(cat_dir_name, pdf_file, raw_text)
            content += entry

    output_path = Path(output_file)
    output_path.write_text(content, encoding="utf-8")
    print(f"\n✓ Erfolgreich synchronisiert: {total_docs} Dokumente in {output_path.relative_to(BASE_DIR)} aggregiert.")

    # Automatically extract profile & keyword weights
    print("\n🔄 Generiere dynamisches Bewerberprofil & Keyword-Wortwolke...")
    profile = build_profile()
    roles = ", ".join(profile.get("target_roles", [])[:5])
    print(f"✓ Profil aktualisiert in {PROFILE_FILE.relative_to(BASE_DIR)} (Rollen: {roles})")
    return True


def main():
    print("# 🔄 Dossier Sync & OCR Extractor\n")
    sync_dossier()


if __name__ == "__main__":
    main()

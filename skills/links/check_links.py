#!/usr/bin/env python3
"""
PDF & Markdown Link Checker for CV files.
Extracts and checks all links, URLs, and email addresses in dist/*.pdf and src/*.md.
"""

import sys
import os
import re
import ssl
import urllib.request
import urllib.error
from pathlib import Path

try:
    import pypdf
except ImportError:
    pypdf = None


def extract_pdf_links(pdf_path):
    """Extract all URI annotations from a PDF file."""
    links = []
    if not pypdf:
        return links
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        for page_idx, page in enumerate(reader.pages):
            if '/Annots' in page:
                for annot in page['/Annots']:
                    try:
                        obj = annot.get_object()
                        if obj.get('/Subtype') == '/Link':
                            if '/A' in obj and '/URI' in obj['/A']:
                                uri = obj['/A']['/URI']
                                links.append({
                                    'page': page_idx + 1,
                                    'url': str(uri),
                                    'source': str(pdf_path)
                                })
                    except Exception:
                        continue
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}", file=sys.stderr)
    return links


def extract_md_links(md_path):
    """Extract links and contact URIs from a markdown file."""
    links = []
    try:
        content = Path(md_path).read_text(encoding='utf-8')
        # Markdown links [text](url)
        md_pattern = r'\[([^\]]+)\]\((https?://[^\s\)]+|mailto:[^\s\)]+)\)'
        for match in re.finditer(md_pattern, content):
            text, url = match.groups()
            links.append({'text': text, 'url': url, 'source': str(md_path), 'type': 'inline_link'})

        # Frontmatter email, linkedin, github
        email_match = re.search(r'^email:\s*["\']?([^"\'\s\n]+)', content, re.MULTILINE)
        if email_match:
            links.append({'text': email_match.group(1), 'url': f"mailto:{email_match.group(1)}", 'source': str(md_path), 'type': 'frontmatter_email'})

        li_match = re.search(r'^linkedin:\s*["\']?([^"\'\s\n]+)', content, re.MULTILINE)
        if li_match:
            links.append({'text': f"linkedin.com/in/{li_match.group(1)}", 'url': f"https://linkedin.com/in/{li_match.group(1)}", 'source': str(md_path), 'type': 'frontmatter_linkedin'})

        gh_match = re.search(r'^github:\s*["\']?([^"\'\s\n]+)', content, re.MULTILINE)
        if gh_match:
            links.append({'text': f"github.com/{gh_match.group(1)}", 'url': f"https://github.com/{gh_match.group(1)}", 'source': str(md_path), 'type': 'frontmatter_github'})

    except Exception as e:
        print(f"Error reading Markdown {md_path}: {e}", file=sys.stderr)
    return links


def validate_url(url, timeout=10):
    """Check a single URL for reachability."""
    if url.startswith('mailto:'):
        email = url[7:]
        # Simple email regex validation
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return {
                'status': 'OK',
                'badge': '🟢',
                'http_code': 200,
                'detail': f'Gültige E-Mail-Adresse ({email})'
            }
        else:
            return {
                'status': 'INVALID',
                'badge': '🔴',
                'http_code': 0,
                'detail': f'Ungültiges E-Mail-Format ({email})'
            }

    ctx = ssl.create_default_context()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'de-CH,de;q=0.9,en;q=0.8'
    }

    try:
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            final_url = resp.url
            redirect_info = f' -> {final_url}' if final_url != url else ''
            return {
                'status': 'OK',
                'badge': '🟢',
                'http_code': resp.status,
                'detail': f'HTTP {resp.status} OK{redirect_info}'
            }
    except urllib.error.HTTPError as e:
        # Some servers reject HEAD (405 Method Not Allowed) or block bots with 403 (e.g., Medium, Cloudflare)
        if e.code in (403, 405, 999):
            try:
                # Retry with GET
                req_get = urllib.request.Request(url, headers=headers, method='GET')
                with urllib.request.urlopen(req_get, context=ctx, timeout=timeout) as resp_get:
                    return {
                        'status': 'OK',
                        'badge': '🟢',
                        'http_code': resp_get.status,
                        'detail': f'HTTP {resp_get.status} OK'
                    }
            except urllib.error.HTTPError as e_get:
                if e_get.code in (403, 999):
                    return {
                        'status': 'PROTECTED',
                        'badge': '🟡',
                        'http_code': e_get.code,
                        'detail': f'HTTP {e_get.code} (Bot-/Cloudflare-Schutz, Domain existiert)'
                    }
                elif e_get.code == 404:
                    return {
                        'status': 'NOT_FOUND',
                        'badge': '🔴',
                        'http_code': 404,
                        'detail': 'HTTP 404 Nicht gefunden (Toter Link)'
                    }
                else:
                    return {
                        'status': 'WARN',
                        'badge': '🟡',
                        'http_code': e_get.code,
                        'detail': f'HTTP {e_get.code} ({e_get.reason})'
                    }
            except Exception as e_get_other:
                return {
                    'status': 'PROTECTED',
                    'badge': '🟡',
                    'http_code': e.code,
                    'detail': f'HTTP {e.code} ({e.reason})'
                }
        elif e.code == 404:
            return {
                'status': 'NOT_FOUND',
                'badge': '🔴',
                'http_code': 404,
                'detail': 'HTTP 404 Nicht gefunden (Toter Link)'
            }
        else:
            return {
                'status': 'WARN',
                'badge': '🟡',
                'http_code': e.code,
                'detail': f'HTTP {e.code} ({e.reason})'
            }
    except urllib.error.URLError as e:
        return {
            'status': 'ERROR',
            'badge': '🔴',
            'http_code': 0,
            'detail': f'Verbindungsfehler / DNS-Problem: {e.reason}'
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'badge': '🔴',
            'http_code': 0,
            'detail': f'Fehler: {str(e)}'
        }


def check_pdf_file(pdf_path):
    """Check links for a single PDF file and return results."""
    links = extract_pdf_links(pdf_path)
    if not links:
        return []

    results = []
    # Deduplicate while preserving page info
    seen = {}
    for item in links:
        url = item['url']
        page = item['page']
        if url not in seen:
            res = validate_url(url)
            seen[url] = res
        else:
            res = seen[url]

        results.append({
            'file': os.path.basename(pdf_path),
            'page': page,
            'url': url,
            'badge': res['badge'],
            'status': res['status'],
            'detail': res['detail']
        })
    return results


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    base_dir = Path(__file__).resolve().parents[2]
    dist_dir = base_dir / 'dist'

    pdf_files = []
    if target == 'all':
        pdf_files = sorted(list(dist_dir.glob('*.pdf')))
    elif os.path.isabs(target) and os.path.exists(target):
        pdf_files = [Path(target)]
    elif (dist_dir / target).exists():
        pdf_files = [dist_dir / target]
    elif (dist_dir / f"{target}.pdf").exists():
        pdf_files = [dist_dir / f"{target}.pdf"]
    elif (dist_dir / f"CV_Thomas_Nemeth_{target}.pdf").exists():
        pdf_files = [dist_dir / f"CV_Thomas_Nemeth_{target}.pdf"]
    else:
        # Try matching any pdf matching target
        matched = list(dist_dir.glob(f"*{target}*.pdf"))
        if matched:
            pdf_files = matched
        else:
            print(f"Keine passende PDF-Datei für '{target}' in {dist_dir} gefunden.", file=sys.stderr)
            sys.exit(1)

    print(f"# Link-Prüfbericht für Lebenslauf-PDFs\n")
    all_ok = True

    for pdf in pdf_files:
        print(f"### PDF: `{pdf.name}`\n")
        results = check_pdf_file(pdf)
        if not results:
            print("_Keine Hyperlinks im PDF gefunden._\n")
            continue

        print("| Seite | URL / Link-Ziel | Status | Detail / HTTP-Status |")
        print("| :---: | :--- | :---: | :--- |")
        for r in results:
            if r['badge'] == '🔴':
                all_ok = False
            print(f"| S. {r['page']} | `{r['url']}` | {r['badge']} {r['status']} | {r['detail']} |")
        print()

    if all_ok:
        print("🟢 **Ergebnis:** Alle geprüften Hyperlinks und E-Mail-Adressen sind intakt und erreichbar.")
    else:
        print("🔴 **Ergebnis:** Es wurden fehlerhafte oder nicht erreichbare Links gefunden. Siehe Details oben.")


if __name__ == '__main__':
    main()

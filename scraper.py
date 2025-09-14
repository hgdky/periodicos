import argparse
import json
import time
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
# ---- Configuración de sitios ----
SITES = {
    "rpp": {
        "base": "https://rpp.pe",
        "categories": {
            "politica": "/politica",
            "actualidad": "/actualidad",
            "deportes": "/deportes"
        }
    },
    "exitosa": {
        "base": "https://www.exitosanoticias.pe",
        "categories": {
            "actualidad": "/actualidad",
            "politica": "/politica",
            "mundo": "/mundo"
        }
    },
    "peru21": {
        "base": "https://peru21.pe",
        "categories": {
            "politica": "/politica",
            "economia": "/economia",
            "deportes": "/deportes"
        }
    }
}


"""scraper.py"""

def scrape_site(base, category_path, max_articles=50):
    links = []

    # recolectar enlaces (ejemplo, deberás adaptar fetch y urljoin)
    html = fetch(base + category_path)
    for href in extract_links(html):
        links.append(urljoin(base, href))

    # normalizar y deduplicar
    seen = set()
    out_links = []
    for l in links:
        p = urlparse(l)
        clean = p.scheme + '://' + p.netloc + p.path
        if clean not in seen:
            seen.add(clean)
            out_links.append(clean)
        if len(out_links) >= max_articles:
            break

    articles = []
    for link in out_links:
        try:
            art_html = fetch(link)
            meta = get_article_meta(art_html, base)
            meta.update({'url': link, 'site': base})
            articles.append(meta)
            time.sleep(0.5)
        except Exception:
            # saltar errores individuales
            continue

    return articles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='data.json')
    args = parser.parse_args()

    result = []
    for site_key, cfg in SITES.items():
        base = cfg['base']
        for cat_name, cat_path in cfg['categories'].items():
            try:
                arts = scrape_site(base, cat_path)
                for a in arts:
                    a['category'] = cat_name
                    a['source'] = site_key
                    result.append(a)
            except Exception:
                continue

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()

"""generator.py
Genera el sitio estático en una carpeta de salida (p. ej. _site) usando Jinja2.
Entrada: JSON generado por scraper.py
"""
import argparse
import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from shutil import copyfile


def makedir(p):
    os.makedirs(p, exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data.json')
    parser.add_argument('--out', default='_site')
    args = parser.parse_args()

    with open(args.data, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    makedir(args.out)
    makedir(os.path.join(args.out, 'static'))

    # copiar static/style.css
    copyfile('static/style.css', os.path.join(args.out, 'static', 'style.css'))

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )

    # index: agrupar por fuente
    grouped = {}
    for a in articles:
        grouped.setdefault(a['source'], []).append(a)

    index_tpl = env.get_template('index.html')
    with open(os.path.join(args.out, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_tpl.render(sources=grouped))

    # article pages
    article_tpl = env.get_template('article.html')
    for i, a in enumerate(articles):
        slug = f"article-{i}.html"
        with open(os.path.join(args.out, slug), 'w', encoding='utf-8') as f:
            f.write(article_tpl.render(article=a))


if __name__ == '__main__':
    main()

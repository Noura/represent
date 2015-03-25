#!/usr/bin/env python
import os, os.path, shutil, codecs, sys, jinja2
import json

datafile = 'data.json'

pages = [
    {
        'name': 'represent',
        'path': '',
        'template': 'index.html',
    },
    {
        'name': 'about',
        'path': 'about',
        'template': 'about.html',
    },
    {
        'name': 'people',
        'path': 'people',
        'template': 'people.html',
    },
    {
        'name': 'projects',
        'path': 'projects',
        'template': 'projects.html',
    },
    {
        'name': 'publications',
        'path': 'publications',
        'template': 'publications.html',
    },
]

def main():
    here = os.path.dirname(__file__)
    loader = jinja2.FileSystemLoader(os.path.join(here, 'templates'))
    templates = jinja2.Environment(loader=loader)

    ctx = {}
    with open(datafile, 'r') as fin:
        ctx = json.loads(fin.read()) 
    ctx['pages'] = pages

    for page in pages:
        tem = templates.get_template(page['template'])
        ctx['active_page'] = page['name']
        out_dir = os.path.join(here, page['path'])
        if page['path'] and not os.path.exists(page['path']):
            os.makedirs(out_dir)
        with codecs.open(os.path.join(out_dir, 'index.html'), 'w', 'utf-8') as out:
            out.write(tem.render(**ctx))

if __name__ == '__main__':
    main()

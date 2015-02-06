#!/usr/bin/env python
import os, os.path, shutil, codecs, sys, jinja2

import data

pages = [
    {
        'name': 'represent',
        'path': '',
        'template': 'index.html',
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

ctx = {
    'pages': pages,
    'people': data.people,
    'projects': data.projects,
    'publications': data.publications,
}

def main():
    here = os.path.dirname(__file__)
    loader = jinja2.FileSystemLoader(os.path.join(here, 'templates'))
    templates = jinja2.Environment(loader=loader)

    for page in pages:
        tem = templates.get_template(page['template'])
        ctx['active_page'] = page['name']
        out_dir = os.path.join(here, page['path'])
        if page['path'] and not os.path.exists(page['path']):
            os.makedirs(out_dir)
        with codecs.open(os.path.join(out_dir, 'index.html'), 'w') as out:
            out.write(tem.render(**ctx))

if __name__ == '__main__':
    main()

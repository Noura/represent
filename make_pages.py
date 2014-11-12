#!/usr/bin/env python
import os, os.path, shutil, codecs, sys, jinja2

import data as DATA
ctx = {
    'people': DATA.people,
}

def main():
    here = os.path.dirname(__file__)
    loader = jinja2.FileSystemLoader(os.path.join(here, 'templates'))
    templates = jinja2.Environment(loader=loader)

    tem = templates.get_template('index.html')
    with codecs.open(os.path.join(here, 'index.html'), 'w') as out:
        out.write(tem.render(**ctx))

if __name__ == '__main__':
    main()

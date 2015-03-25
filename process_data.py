#!/usr/bin/env python
import os, os.path, shutil, sys
import csv
import json

# filename & folder settings
source = 'data'
people_csv = 'People - Sheet1.csv'
projects_csv = 'Projects - Sheet1.csv'
publications_csv = 'Publications - Sheet1.csv'

people_dir_in = os.path.join(source, 'people images')
projects_dir_in = os.path.join(source, 'project images')
people_dir_out = 'static/img/people'
projects_dir_out = 'static/img/projects'

output = 'data.json'

# parsing settings
people_top_lines = 3 # ignore the first 3 rows
people_old = 'Alumni:' # row with this in first cell marks start of alumni
projects_top_lines = 4 # ignore first 4 rows
projects_old = 'PAST' # row with this in first cell marks start of old projects
publications_top_lines = 2

def main():
    """
    for (dirpath, dirnames, filenames) in os.walk(source):
        print dirpath
        print dirnames
        print filenames
    """
    here = os.path.abspath(os.path.dirname(__file__))

    current_ppl = []
    alumni = []
    current_projects = []
    old_projects = []
    publications = []

    shutil.rmtree(people_dir_out)
    shutil.rmtree(projects_dir_out)
    shutil.copytree(people_dir_in, people_dir_out)
    shutil.copytree(projects_dir_in, projects_dir_out)

    with open(os.path.join(here, source, people_csv)) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        current = True
        for row in reader:
            if count < people_top_lines:
                count += 1
                continue
            if row[0] == '':
                continue
            if row[0] == people_old:
                current = False
                continue
            person = {}
            person['name'] = row[0]
            person['url'] = row[1]
            if row[5] != '':
                person['img_src'] = os.path.join('/', people_dir_out, row[5])
            else:
                person['img_src'] = '/static/img/wave.gif'
            if current:
                current_ppl.append(person)
            else:
                alumni.append(person)

    with open(os.path.join(here, source, projects_csv)) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        current = True
        for row in reader:
            if count < projects_top_lines:
                count += 1
                continue
            if row[0] == '':
                continue
            if row[0] == projects_old:
                current = False
                continue
            project = {}
            project['name'] = row[0]
            project['url'] = row[1]
            project['desc'] = row[7]
            if row[5] != '':
                project['img_src'] = os.path.join('/', projects_dir_out, row[5])
            else:
                project['img_src'] = '/static/img/wave.gif'
            if current:
                current_projects.append(project)
            else:
                old_projects.append(project)

    with open(os.path.join(here, source, publications_csv)) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            if count < publications_top_lines:
                count += 1
                continue
            if row[0] == '':
                continue
            pub = row[0]
            publications.append(pub)

    data = {
            'members': current_ppl,
            'alumni': alumni,
            'current_projects': current_projects,
            'old_projects': old_projects,
            'publications': publications
            }

    out = os.path.join(here, output)
    with open(out, 'w+') as f:
        f.write(json.dumps(data, indent=4, separators=(',', ':'), sort_keys=True).encode('utf-8'))

if __name__ == '__main__':
    main()

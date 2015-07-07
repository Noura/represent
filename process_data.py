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

    os.system("cp -rf data/*.txt templates/")

    # process people
    # advisor = {} # find the adviser separately to put him at the end
    with open(os.path.join(here, source, people_csv)) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        current = True
        for row in reader:
            if count < people_top_lines:
                count += 1
                continue
            if row[0] == people_old:
                current = False
                continue
            if row[0] == '' or row[6] != 'y':
                continue
            person = {}
            person['name'] = row[0]
            if row[1] != '':
                person['url'] = row[1]
            if row[5] != '':
                person['img_src'] = os.path.join('/', people_dir_out, row[5])
            # sort ppl into advisor or current members or alumni
            #if row[6] == 'y':
            #    advisor = person
            #elif current:
            if current:
                current_ppl.append(person)
            else:
                alumni.append(person)
    #rely on sorting in spreadsheet
    #current_ppl = sorted(current_ppl, key=lambda p: p['name'].split(' ')[-1])
    #alumni = sorted(alumni, key=lambda p: p['name'].split(' ')[-1])
    #current_ppl = sorted(current_ppl, key=lambda p: p['name'])
    #alumni = sorted(alumni, key=lambda p: p['name'])
    #current_ppl.append(advisor) # advisor gets shown at end of current members

    with open(os.path.join(here, source, projects_csv)) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        current = True
        for row in reader:
            if count < projects_top_lines:
                count += 1
                continue
            if row[0] == projects_old:
                current = False
                continue
            if row[0] == '' or row[8] != 'y':
                continue
            project = {}
            project['name'] = row[0]
            project['url'] = row[1]
            project['desc'] = row[6]
            if row[5] != '':
                project['img_src'] = os.path.join('/', projects_dir_out, row[5])
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

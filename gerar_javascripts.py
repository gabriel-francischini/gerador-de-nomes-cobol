import os
import json
import itertools
from itertools import *
from tqdm import tqdm
import unidecode
import json
import random
import django
from django.template import Template, Context
from django.conf import settings
# optional if you just render str instead of template file
from django.template.loader import get_template

settings.configure(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    # if you want to render using template file
    'DIRS': ['./']
}])
django.setup()

# variables that will be passed to template
vars = {'name':'mochtar'}

#print(Template("Using string = {{name}}").render(Context(vars)))

# file say_hello.tmpl located in folder /tmp/template_dirs as it's configured above
#print(get_template("pgm01.tmpl").render(vars))


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def read_names(limit=None):
    #print("Loading names...")
    for dirname, subdirs, filenames in os.walk('frequency/'):
        if not limit:
            limit = len(filenames)
        for filename in tqdm(filenames[:limit]):
            filepath = os.path.join(dirname, filename)

            with open(filepath, 'r') as filedata:
                try:
                    file_contents = filedata.read()
                    data = json.loads(file_contents)
                    if (len(data) > 0) and type(data) == list:
                        #print(data)
                        yield data[0]
                except json.decoder.JSONDecodeError as e:
                    if len(file_contents.strip()) > 0:
                        raise e
                except Exception as e:
                    raise Exception("File with issues: " + filepath) from e

def read_surnames(limit=None):
    with open('sobrenomes.json', 'r') as filedata:
        immigrants = filedata.read()
    _, immigrants = json.loads(immigrants)
    for page in immigrants:
        for record in page:
            surname = record['sobrenome']
            if type(surname) == str and len(surname.strip()) > 3:
                yield surname

    with open('sobrenomes_sem_metadata.txt', 'r') as datafile:
        for name in datafile:
            if len(name.strip()) > 3:
                yield name.strip()


def read_states():
    with open('estados-cidades.json', 'r') as filedata:
        data = json.loads(filedata.read())
        return data['estados']


def asciify(string):
    return unidecode.unidecode(string).upper()

# Use limit=8000 to load a testable amount of names
names = [i for i in read_names(limit=800)]
surnames = list(set([asciify(i).strip() for i in read_surnames()]))
surnames = [x for x in surnames if '[' not in x and '(' not in x and '?' not in x]
states = read_states()


vars = {'names': json.dumps(names),
        'states': json.dumps(states),
        'surnames': json.dumps(surnames)}

for dirname, subdirs, filenames in os.walk('./'):
    for filename in ([x for x in filenames if x.lower().endswith('.tmpl')]):
        outfile = filename.rsplit('.tmpl', 1)[0] + '.html'
        with open(outfile, 'w') as out:
            out.write(get_template("pgm01.tmpl").render(vars))
    break

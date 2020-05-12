import os
import json
import itertools
from itertools import *
from tqdm import tqdm
import unidecode
import json
import random


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
names = [i for i in read_names()]
surnames = list(set([asciify(i).strip() for i in read_surnames()]))
surnames = [x for x in surnames if '[' not in x and '(' not in x and '?' not in x]
states = read_states()


class SurnameError(IndexError):
    pass

def fill_surnames(name='', surname=[], limit=30, blacklist=[],
                  do_raise=False, level=0):
    global surnames

    while True:
        if len(surname) == 0:
            remaining = limit - (len(name)  + len(' '))
        else:
            remaining = limit - (len(name)  + len(' ')
                                 + len(' '.join((surname))) + len(' '))

        #print(f"We have {remaining} chars out of {limit}: {name + ' ' + ' '.join(surname)}")
        if remaining == 0:
            return (asciify(name), asciify(' '.join(surname)))

        if random.randint(0, 2) % 2 == 1:
            possibles = list(filter(lambda x: (len(x) == (remaining - 1))
                                              and (x not in blacklist),
                            surnames))
        else:
            possibles = []

        if len(possibles) <= 0:
            #print(f"Picked inexact possibilities for {remaining - 1}")
            possibles = list(filter(lambda x: (len(x) <= (remaining - 1))
                                    and (x not in blacklist),
                                surnames))
        else:
            pass
            #print(f"Picked exact possibilities for {remaining - 1}")


        if len(possibles) <= 0:
            raise SurnameError(name + ' ' + ' '.join(surname))

        if level % 2 == 0:
            weights = [len(x) for x in possibles]
        else:
            weights = [1/len(x) for x in possibles]
            level += 1

        new_surname = random.choices(possibles, weights, k=1)[0]
        try:
            return fill_surnames(name=name.strip(),
                                 surname=[asciify(x).strip()
                                          for x in surname]
                                 + [asciify(new_surname).strip()],
                                 limit=limit,
                                 blacklist=blacklist + [new_surname],
                                 do_raise=True,
                                 level = level)
        except SurnameError as e:
            if (not do_raise):
                pass
                #print(f"Name left no possibilities: {e.args[0]} ({len(e.args[0])})")
            else:
                raise e


def generate_RG():
    return ''.join([random.choice('123456789') for i in range(11)])

def generate_phonenumber():
    return ''.join([random.choice('123456789') for i in range(8)])


hist = {}
for name in names:
    uf = asciify(name['ufMax'])
    hist[uf] = hist.get(uf, 0) + 1

# print(hist)

for i in range(1000):
    state = random.choice(states)
    state_name = asciify(state['nome'])
    state_uf = asciify(state['sigla'])
    city = asciify(random.choice(state['cidades']))


    state_names = [name for name in names
                   if asciify(name['ufMax']) == state_name]

    
    state_names, weights = zip(*[(asciify(x['nome']).strip(),
                                 float(x['ufMaxProp'].replace(',', '.')))
                                for x in state_names])
    name = random.choices(state_names, weights)[0]
    #print(name)
    name, surname = fill_surnames(name, limit=30)

    capped_city = city[:min([len(city), 30])]
    capped_city = capped_city + ' ' * (30-len(capped_city))
    print(generate_RG() + name + ' ' + surname + ' '
          + state_uf[:min([2, len(state_uf)])] + capped_city + generate_phonenumber())

# hist = {}
# for name in surnames:
#     k = len(name)
#     hist[k] = hist.get(k, 0) + 1
# for x in (sorted(hist.items())):
#     print(x)

#print(hist)
#print(surnames)

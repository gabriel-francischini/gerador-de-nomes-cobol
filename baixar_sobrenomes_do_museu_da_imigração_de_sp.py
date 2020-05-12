from urllib.parse import urlencode, quote_plus
import urllib.request
import os
import json
import pyhash


# see https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3/40557716
def getPage(pageNum):
    # origin: http://www.inci.org.br/acervodigital/livros.php
    url="http://www.arquivoestado.sp.gov.br/site/acervo/memoria_do_imigrante/getHospedariaApi"

    # You need to generate a valid token. Do a legit search and analyze the POST
    # request in order to get this token.
    token="token=a%245aFj38o%26042bAe&nome=&sobrenome=&nacionalidade=&chegada=&vapor="
    payload={'frm': token,
             'page': str(pageNum),
             'limit':'20'}
    #final_url = url + '?' + urlencode(payload, quote_via=quote_plus)

    req = urllib.request.Request(url, data=(urlencode(payload,
                                                      quote_via=quote_plus)
                                            .encode('utf-8')))
    #print(req.get_full_url())
    #print(req.data)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        return the_page.decode('utf-8')

# see https://docs.python.org/3/howto/urllib2.html
def get_response(url):
    # with urllib.request.urlopen(url) as response:
    #     html = response.read()
    #     return html
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        return the_page

def print_wget(name):
    filename="frequency/{}.request".format(name)
    command="""
if [ ! -f {} ]; then
    echo "fetching {}"...
    curl -s {} -o "{}"
fi
"""
    print(command.format(filename, nameurl(name), nameurl(name), filename))


hasher = pyhash.fnv1_32()
def get_id(page):
    global hasher
    b = str(tuple(sorted([str(x) for x in page['dados']])))
    c = hasher(b)
    return c

savefile = "sobrenomes.json"
def saveData():
    global pg
    global acc
    with open(savefile, "w") as filedata:
        data = (pg, acc)
        filedata.write(json.dumps(data, indent=2, sort_keys=True))

if os.path.isfile(savefile):
    with open(savefile, "r") as filedata:
        pg, acc = tuple(json.load(filedata))
        pg = int(pg)
        acc = list(acc)
else:
    pg = 0
    acc = []
    saveData()


page = ''
previous_id = ''
current_id = 'dummy start'

same_pg_counter = 0
while (current_id != previous_id) or (same_pg_counter <= 3):
    if ((pg + 5) % 10) == 0:
        saveData()
        #break

    print("\nCarregando a página {}...".format(pg))

    page = json.loads(getPage(pg))

    previous_id = current_id
    current_id = get_id(page)

    print("previous_id: " + str(previous_id))
    print("current_id: " + str(current_id))
    pg += 1

    if current_id == previous_id:
        print("Oh-oh, this page is repeating...")
        same_pg_counter += 1
    else:
        same_pg_counter = 0
        acc.append(page['dados'])

#print(page)

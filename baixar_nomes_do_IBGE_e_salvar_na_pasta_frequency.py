from urllib.parse import urlencode, quote_plus
import urllib.request
import os


# see https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3/40557716
def nameurl(name):
    example="https://servicodados.ibge.gov.br/api/v1/censos/nomes/basica?nome=osvaldo"
    payload={'nome': name}
    return example.split('?')[0] + '?' + urlencode(payload, quote_via=quote_plus)

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



#print(get_response(nameurl("osvaldo")))
#print_wget("osvaldo")
#exit()
with open("somenames.txt", "r") as filedata:
    for line in filedata:
        print_wget(line.strip())

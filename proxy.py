import urllib3
urllib3.disable_warnings()
from time import strftime
from datetime import datetime
from base64 import b64encode
from requests import get, put
from json import loads, dumps
from os import environ
from time import sleep
token = environ.get('github', None)
apiurl = environ.get('apiurl', None)
data = get(url=apiurl, verify=False).json()
data.sort(key = lambda x: x['ping_time_ms'])
proxies = []
jsons = []
l = len(data)
for i,proxy in enumerate(data):
    if i == 50:
        break
    if proxy['iso_code'] == 'IR':
        print('Skipping IRAN')
        continue
    http_proxy  = "http://" + proxy['server'] + ':' + str(proxy['port'])
    proxyDict = {
        "http"  : http_proxy, 
        "https" : http_proxy
    }
    print('%s / %s | checking %s' % (i+1,l,http_proxy))
    try:
        r = get(url = 'https://raw.githubusercontent.com/h4mid007/free-proxy-list/master/!', verify=False, proxies=proxyDict, timeout=5)
        if r.status_code == 200 and 'passed!' in r.text:
            print(http_proxy)
            proxies.append(proxy['server'] + ':' + str(proxy['port']))
            proxy.pop('iso_code', None)
            proxy.pop('ping_time_ms', None)
            proxy.pop('protocol', None)
            proxy.pop('loss_ratio', None)
            jsons.append(proxy)
    except:
        pass
    sleep(3)
    
## txt proxies formatting
prox = ''
for proxy in proxies:
    prox = prox + proxy + '\n'
## pac proxies formatting
pacs = '''
function FindProxyForURL(url, host) {
return "{0}";
}
'''
pac = ''
for proxy in proxies:
    pac = pac + 'PROXY '+ proxy + ';'
pacs = pacs.format(pac)
proxies = b64encode(str(prox).encode())
jsons = b64encode(str(dumps(jsons)).encode())
pacs = b64encode(str(pacs).encode())
#Setting headers
headers = {"Content-Type" : "application/vnd.github.v3+json", "Authorization" : "token " + token}
#getting sha and updating txt
sha = get(url='https://api.github.com/repos/h4mid007/free-proxy-list/contents/proxies.txt', headers=headers, verify=False).json()['sha']
data = {"message": datetime.now().strftime("%D - %H:%M"), "content": proxies.decode(), "sha": sha}
a = put(url='https://api.github.com/repos/h4mid007/free-proxy-list/contents/proxies.txt', json=data, headers=headers, verify=False)
#getting sha and updating json
sha = get(url='https://api.github.com/repos/h4mid007/free-proxy-list/contents/proxies.json', headers=headers, verify=False).json()['sha']
data = {"message": datetime.now().strftime("%D - %H:%M"), "content": jsons.decode(), "sha": sha}
a = put(url='https://api.github.com/repos/h4mid007/free-proxy-list/contents/proxies.json', json=data, headers=headers, verify=False)
#getting sha and updating pac
sha = get(url='https://api.github.com/repos/h4mid007/free-proxy-list/contents/proxies.pac', headers=headers, verify=False).json()['sha']
data = {"message": datetime.now().strftime("%D - %H:%M"), "content": pacs.decode(), "sha": sha}
a = put(url='https://api.github.com/repos/h4mid007/free-proxy-list/contents/proxies.pac', json=data, headers=headers, verify=False)





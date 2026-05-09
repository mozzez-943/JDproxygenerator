import requests
import json
import re

filename = 'proxylist.jdproxies'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
             '(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'


def create_proxy_record(address, port, type, enabled):
    proxy_record = dict()
    proxy_preferences = dict()
    proxy_preferences["username"] = None
    proxy_preferences["password"] = None
    proxy_preferences["port"] = port
    proxy_preferences["address"] = address
    proxy_preferences["type"] = type
    proxy_preferences['preferNativeImplementation'] = False
    proxy_preferences['resolveHostName'] = False
    proxy_preferences['connectMethodPreferred'] = False
    proxy_record['proxy'] = proxy_preferences
    proxy_record['rangeRequestsSupported'] = True
    proxy_record['filter'] = None
    proxy_record['pac'] = False
    proxy_record['reconnectSupported'] = False
    proxy_record['enabled'] = enabled
    json_data = proxy_record
    return json_data


def create_json_structure(proxies):
    proxylist_json_structure = dict()
    proxylist_json_structure["customProxyList"] = proxies
    return proxylist_json_structure


def get_proxies_from_socks_proxy_net():
    proxy_site_url = 'https://socks-proxy.net/#list'
    res = requests.get(proxy_site_url, headers={'User-Agent': user_agent})
    proxy_list = list()
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', res.text, flags=re.IGNORECASE | re.DOTALL)
    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, flags=re.IGNORECASE | re.DOTALL)
        proxy_definition = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells[:8]]
        if len(proxy_definition) < 5 or not proxy_definition[1].isdigit():
            continue
        proxy_list.append(
            create_proxy_record(
                type=proxy_definition[4].upper(), address=proxy_definition[0], port=int(proxy_definition[1]), enabled=True
            )
        )
    return proxy_list


proxy_list = list([create_proxy_record(type="NONE", address=None, port=80, enabled=True)])
proxy_list = proxy_list + get_proxies_from_socks_proxy_net()
json_output = create_json_structure(proxy_list)
with open(filename, 'w') as f:
    json.dump(json_output, f, indent=2)

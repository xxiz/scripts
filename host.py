import requests

if __name__ == '__main__':
    r = requests.get('http://ip-api.com/json')
    print(r.json())
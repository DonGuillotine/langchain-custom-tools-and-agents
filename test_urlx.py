from decouple import config
import requests

BITLY_API_TOKEN = config("BITLY_API_TOKEN")

def shorten_url(url):
    global BITLY_API_TOKEN

    api_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {BITLY_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'long_url': url
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        short_url = response.json()['id']
        return short_url
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


url_to_shorten = "https://python.langchain.com/docs/modules/agents/toolkits/csv"

short_url = shorten_url(url_to_shorten)
if short_url:
    print(f"Short URL: {short_url}")
else:
    print("URL shortening failed.")

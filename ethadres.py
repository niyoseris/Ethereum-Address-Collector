import requests
from bs4 import BeautifulSoup
import re

print(
"""
Ethereum network address collector.
Helps you to find active addresses from recent transactions.

https://niyo.link

v1. March 2024


thank you ChatGPT
"""
)


min_value = 5
max_value = 10000



def get_multichain_portfolio_value(address):
    try:
        url = f"https://etherscan.io/address/{address}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            multichain_values = soup.find_all('span', class_='fw-medium')
            for va in multichain_values:
                if "$" in va.text.strip():
                    va = va.text.strip().replace("$", "").replace(",","").strip()
                    if float(va) < max_value and float(va) > min_value:
                        print(f"{address}")
        else:
            print(f"Failed to fetch data for address {address}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def get_recent_transactions_addresses():
    try:
        url = 'https://etherscan.io/txs'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            addresses = set()  # Using a set to avoid duplicate addresses
            # Find all links with href containing "address"
            links = soup.find_all('a', href=re.compile(r'address'))
            for link in links:
                address = re.findall(r'0x[a-fA-F0-9]{40}', link['href'])
                addresses.update(address)
            return list(addresses)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    return []

# Get the list of addresses from recent transactions
recent_transactions_addresses = get_recent_transactions_addresses()

# Get multichain portfolio value for each address
multichain_portfolio_values = {}
for address in recent_transactions_addresses:
    multichain_value = get_multichain_portfolio_value(address)
    if multichain_value is not None:
        multichain_portfolio_values[address] = multichain_value


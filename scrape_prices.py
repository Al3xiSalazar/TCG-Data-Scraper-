#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[5]:


def scrape_pokemon_card_prices(card_name, base_url="https://www.tcgplayer.com/search/pokemon/product", page=1):
    search_url = f"{base_url}?productLineName=pokemon&page={page}&view=grid&q={card_name}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status
        soup = BeautifulSoup(response.content, 'html.parser')

        card_data = []
        card_listings = soup.find_all('article', class_='product-detail')

        if not card_listings:
            print(f"No card listings found for '{card_name}'. Check the card name or try a different card.")
            return pd.DataFrame(card_data)

        for card in card_listings:
            try:
                card_title = card.find('h3', class_='product-name').text.strip()
                card_price = card.find('span', class_='price-point__data').text.strip()
                card_data.append({'Card Title': card_title, 'Price': card_price})
            except AttributeError as e:
                print(f"Error extracting data for card: {e}")
                continue

        if not card_data:
            print(f"No results found for '{card_name}'.")

        df = pd.DataFrame(card_data)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while scraping '{search_url}': {e}")
        return pd.DataFrame()

# Example usage: Scrape prices for a specific Pokémon card
pokemon_card_name = "Charizard"
pokemon_prices_df = scrape_pokemon_card_prices(pokemon_card_name)
print(pokemon_prices_df)


# In[ ]:





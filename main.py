import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://krisha.kz/prodazha/kvartiry/almaty/?page="

num_pages = 5

listings = []

for page in range(1, num_pages + 1):

    url = base_url + str(page)

    response = requests.get(url)

    if response.status_code == 200:
        print(f"Successfully retrieved page {page}.")
    else:
        print(f"Failed to retrieve page {page}.")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    listing_elements = soup.find_all('div', attrs={'data-product-id': True})

    print(len(listing_elements))

    for element in listing_elements:
        #print(element)

        #Square footage
        title = element.find('a', class_='a-card__title').text.strip()
        #Listing URL
        listing_url = 'https://krisha.kz' + element.find('a', class_='a-card__title')['href'].strip()
        #Property price
        price = element.find('div', class_='a-card__price').text.strip()
        #Location(address, city, state)
        location = element.find('div', class_='card-stats__item').text.strip()
        address = element.find('div', class_='a-card__subtitle').text.strip()
        text = element.find('div', class_='a-card__text-preview').text.strip()

        # print(f'Title: {title} \nListing URL: {listing_url}, \nPrice: {price} \nLocation: {location} '
        #       f'\nAddress: {address} \nText: {text}\n\n')

        listing = {
            'Title': title,
            'Listing URL': listing_url,
            'Price': price,
            'Location': location,
            'Address': address,
        }

        listings.append(listing)

print('Scraping ended')

csv_file_name = 'listings.csv'

csv_header = ['Title', 'Listing URL', 'Price', 'Location', 'Address']

with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_header)

    writer.writeheader()

    for listing in listings:
        writer.writerow(listing)

print(f'Data has been saved to {csv_file_name}.')
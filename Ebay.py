from bs4 import BeautifulSoup
import requests
import pandas as pd 

url = 'https://www.ebay.com/sch/i.html?_nkw=glasses&_sacat=0&_from=R40&_trksid=p4432023.m570.l1313'
r = requests.get(url)
Titles = []
Prices = []
Locations = []
Delivery = []
Links = []
Sellers = []

soup = BeautifulSoup(r.content,'html.parser')
for page in range(1,51):
    url = f'https://www.ebay.com/sch/i.html?_nkw=glasses&_sacat=0&_from=R40&_pgn={page}'
    titles = soup.find_all('a',class_='s-item__link')
    prices = soup.find_all('span',class_='s-item__price')
    locations = soup.find_all('span',class_='s-item__location s-item__itemLocation')
    delivery = soup.find_all('span',class_='s-item__shipping s-item__logisticsCost')
    img_links = soup.find_all('div',class_='s-item__image-wrapper image-treatment')
    sellers = soup.find_all('span',class_='s-item__seller-info-text')
    for title in titles:
        org_title = title.find('div',class_='s-item__title')
        if org_title:
            name = org_title.find('span',{'aria-level':'3'})
            Titles.append(name.getText())

    for price in prices:
        Prices.append(price.getText())

    for location in locations:
        if location:
            Locations.append(location.getText())

    for delv in delivery:
        Delivery.append(delv.getText())

    for img in img_links:
        org_img = img.find('img')
        if org_img and 'src' in org_img.attrs:
            Links.append(org_img['src'])

    for seller in sellers:
        Sellers.append(seller.getText())
min_len = min(len(Titles), len(Prices), len(Locations), len(Delivery), len(Links), len(Sellers))
df = pd.DataFrame({
    "Product_Names":Titles[:min_len],
    "Prices":Prices[:min_len],
    "Locations":Locations[:min_len],
    "Shipping_Cost":Delivery[:min_len],
    "Image_Links":Links[:min_len],
    "Sellers":Sellers[:min_len]
})
df.to_csv('C:\\Users\\HM Laptops\\Desktop\\Web Scrapping\\ebay.csv',index=False)

"""Collects car listings

Scrapes craigslist for car listing information
"""
import requests
import csv
import argparse
from bs4 import BeautifulSoup
from craigslist import CraigslistForSale

class SearchResult(object):
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

class CarDetails():
    def __init__(self, year, odometer):
        self.year = year
        self.odometer = odometer

class CarListing():
    def __init__(self, car_details, price):
        self.details = car_details
        self.price = price

def get_listings_old():
    r = requests.get("http://reference.craigslist.org/Categories")
    category_id = 0
    for item in r.json():
        if item["Abbreviation"] == "cto":
            category_id = item["CategoryID"]

    r = requests.get(f"http://reference.craigslist.org/Categories/{category_id}")
    print (r.json())

def get_listings(model, limit, zip_code, site):
    CraigslistForSale.show_filters(category="cto")
    listings = []
    cl_search = CraigslistForSale(site=site,
                                  category="cto",
                                  filters={
                                    "make" : "subaru",
                                    "model" : model,
                                    "search_distance" : 500,
                                    "zip_code": zip_code,
                                    "bundle_duplicates" : True})

    for result in cl_search.get_results(sort_by="newest", limit=limit):
        listings.append(SearchResult(result["name"], result["price"], result["url"])) 
    return listings

def get_car_attr_from_map_and_attrs_div(attrs_div):
    p_attrs = attrs_div.find_all("p", class_="attrgroup")
    # first entry is the year and name
    spans = p_attrs[0].find_all("span")
    year = spans[0].text.split(" ")[0]
    # second entry contains the mileage and model features
    odometer = 0
    for span in p_attrs[1].find_all("span"):
        attr_split = span.text.split(":")
        if len(attr_split) <= 1:
            continue
        keyword = attr_split[0]
        if (keyword == "odometer"):
            odometer = attr_split[1]
    return CarDetails(year, odometer)


def parse_listing(url):
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    attr_div = html_soup.find_all("div", class_="mapAndAttrs")[0]
    return get_car_attr_from_map_and_attrs_div(attr_div)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List Car posts.')
    parser.add_argument('--site', default="vancouver", help="Specify the craigslist site")
    parser.add_argument('--limit', type=int, default=200, help="Specify the number of entries")
    parser.add_argument('--zip_code', help="zip code to search from")
    parser.add_argument('--query', default="forester", help="query to use")

    args = parser.parse_args()
    listings = get_listings(args.query, args.limit, args.zip_code, args.site)
    parsed_listings = []
    for item in listings:
        print(item)
        details = parse_listing(item.url)
        parsed_listings.append(CarListing(details, item.price)) 
    with open("cars.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerow(["Price", "Year", "Odometer"])
        for listing in parsed_listings:
            csv_writer.writerow([listing.price, listing.details.year, listing.details.odometer])


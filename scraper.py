import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_organisations(url, label):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_='msl-gl-link')
        
        organisations = [f"{link.get_text(strip=True)} {label}" for link in links]
        return organisations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

def main():
    sports_url = "https://www.warwicksu.com/societies-sports/sports-clubs/"
    societies_url = "https://www.warwicksu.com/societies-sports/societies/"
    
    print("Fetching Sports Clubs...")
    sports_clubs = fetch_organisations(sports_url, "(Sports Club)")
    
    print("Fetching Societies...")
    societies = fetch_organisations(societies_url, "(Society)")
    
    combined_list = sports_clubs + societies
    combined_list.sort()
    
    # Structure the data neatly for API usage
    data = {
        "total_count": len(combined_list),
        "sports_clubs_count": len(sports_clubs),
        "societies_count": len(societies),
        "organizations": combined_list
    }
    
    # Save to a JSON file
    with open('warwick_orgs.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully saved {len(combined_list)} organizations to warwick_orgs.json")

if __name__ == "__main__":
    main()

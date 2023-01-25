import requests
import csv
import os
from getpass import getpass

def create_file():
    name = input("Enter name of your file: ")
    file_directory = f'{os.path.dirname(os.path.realpath(__file__))}'
 
    while os.path.exists(name):
        name = input("File already Exists in directory. Please enter a diferent name: ")

    file_name = os.path.join(file_directory, name)
    return file_name

def get_region_url(region):
    if region == "US":
        return "https://api.mailgun.net/v3/lists/pages"  
    elif region == "EU":
        return "https://api.eu.mailgun.net/v3/lists/pages"

def get_mailing_lists(url, key):
    return requests.get(
        f"{url}",
        auth=('api', key))

def write_to_file(file_name, address):
    with open(file_name, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([address])

def main():
    api_key = getpass(prompt = "Enter your API Key: ") 
    csv_file = create_file()
    url = get_region_url(input("Enter the region your domain is located in: ").upper())
    resp = get_mailing_lists(url, api_key)

    if resp.status_code == 200:
        response = resp.json()

        while len(response['items']):
            for i in range (len(response["items"])):
                write_to_file(csv_file, response["items"][i]['address'])
            next_url = response['paging']['next']
            response = get_mailing_lists(next_url, api_key).json()
    else:
        print(f"Error: {resp.status_code}, closing program")

if __name__ == "__main__":
    main()

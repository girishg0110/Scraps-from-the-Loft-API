import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import json

base_url = "https://scrapsfromtheloft.com"

def get_parsed_html(url):
    response = requests.request("GET", url)
    return BeautifulSoup(response.text, "html.parser")

def scrape_by_tag(tag):
    url = '/'.join([base_url, "tag", tag])
    parsed_html = get_parsed_html(url)
    links = [link['href'] for link in parsed_html.find_all(class_="elementor-post__thumbnail__link")]
    return links

def get_script(link):
    parsed_html = get_parsed_html(link)
    data = {}
    data["title"] = parsed_html.find("title").string
    data["description"] = parsed_html.find("meta", {"name" : "description"})["content"]
    data["text"] = {}
    script_lines = parsed_html.find_all("p", style="text-align: justify;")
    line_c = 0
    for line in script_lines:
        if line.string:
            data["text"][line_c] = line.string 
            line_c += 1

    return data

def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    artist_name = "bernie mac"
    scripts = scrape_by_tag('-'.join(artist_name.split(' ')))
    print(scripts)
    for scr in scripts:
        target_script = get_script(scr)
        save_to_json(target_script, f"{target_script['title']}.json")
import json
import pandas as pd
import requests
import os
import json
import re
from unidecode import unidecode
from bs4 import BeautifulSoup


def get_story_urls():
    main_urls = [
        "http://kumpulanceritabahasajawa.blogspot.com/search/label/LEGENDA",
        "http://kumpulanceritabahasajawa.blogspot.com/search/label/WAYANG",
        "http://kumpulanceritabahasajawa.blogspot.com/search/label/CERITA%20RAKYAT",
        "http://kumpulanceritabahasajawa.blogspot.com/search/label/CERITA%20CEKAK ",
        "http://kumpulanceritabahasajawa.blogspot.com/search/label/DONGENG",
    ]

    story_urls = []

    for url in main_urls:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            elements = soup.select("div#main h2.post-title > a")

            for element in elements:
                story_url = element.get('href')
                story_urls.append(story_url)

    return story_urls


def get_story_contents(story_urls):

    stories = {}

    for url in story_urls:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            elements = soup.select(
                'div.post-body.entry-content div[style="text-align: justify;"]')

            paragraphs = ""

            for i, element in enumerate(elements):
                # ignore opening and closing statement by writer
                if i == 0 or i == len(elements)-1:
                    continue

                paragraph = element.get_text().strip()

                is_long_enough = len(paragraph) > 3

                if is_long_enough:
                    paragraphs += " " + paragraph

            paragraphs = paragraphs.strip()
            paragraphs = unidecode(paragraphs)
            paragraphs = re.sub(r"\s+", " ", paragraphs)

        paragraph_chunks = split_text_into_chunks(paragraphs, 300)

        stories[url] = paragraph_chunks

    return stories


def split_text_into_chunks(text, words_per_chunk=30):
    chunks = []

    sentences = text.split('.')
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 0:

            if len(current_chunk.split()) + len(sentence.split()) <= words_per_chunk:
                current_chunk += sentence + '. '
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


story_urls = get_story_urls()
stories = get_story_contents(story_urls)

# print(json.dumps(stories, indent=2))
with open('kumpulanceritabahasajawa.json', 'w+') as f_json:
    stories_json = json.dumps(stories, indent=2)
    f_json.write(stories_json)
    f_json.close()


stories_arr = []
for key in stories:
    for row in stories[key]:
        stories_arr.append(row)

df = pd.DataFrame({
    'text_jw': stories_arr
})

df.to_csv('kumpulanceritabahasajawa.csv')

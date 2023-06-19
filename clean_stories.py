import os
import pandas as pd
from bs4 import BeautifulSoup


files = []
for dirname, _, filenames in os.walk('./data/stories'):
    for filename in filenames:
        files.append(os.path.join(dirname, filename))


def get_story_content(html_content: str) -> str:

    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select("div#content > article.post > p")

    paragraphs = []
    for element in elements:
        paragraphs.append(element.text)

    paragraphs = paragraphs[1:-2]

    text = ' '.join(paragraphs)
    return text


print(files[0])
new_file_path = os.path.join(
    './data/stories_extract_text', os.path.basename(files[0]))
new_file_path = os.path.splitext(new_file_path)[0] + '.txt'
print(new_file_path)


def get_output_file_path(old_path: str) -> str:
    new_file_path = os.path.join(
        './data/stories_extract_text', os.path.basename(old_path))
    new_file_path = os.path.splitext(new_file_path)[0] + '.txt'
    return new_file_path


for i, file in enumerate(files):
    if i % 10 == 0:
        print("progress:", i)

    with open(file, 'r') as f:
        html_content = f.read()
        f.close

    text = get_story_content(html_content=html_content)

    output_file_path = get_output_file_path(file)
    with open(output_file_path, "w") as writer:
        writer.write(text)
        writer.close()

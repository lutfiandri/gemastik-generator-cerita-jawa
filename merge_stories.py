import os
import pandas as pd
import re


files = []
for dirname, _, filenames in os.walk('./data/stories_extract_text'):
    for filename in filenames:
        files.append(os.path.join(dirname, filename))


df = pd.read_csv('./data/urls.csv', index_col=0)
texts = []


def clean_text(text):
    # Remove HTML tags
    cleaned_text = re.sub('<.*?>', '', text)

    # Remove special characters and punctuation
    cleaned_text = re.sub('[^A-Za-z0-9.,?!]+', ' ', cleaned_text)

    # Remove extra whitespaces
    cleaned_text = ' '.join(cleaned_text.split())

    # Convert to lowercase
    cleaned_text = cleaned_text.lower()

    return cleaned_text


for i, file in enumerate(files):
    if i % 10 == 0:
        print("progress:", i)

    with open(file, 'r') as f:
        text = f.read()
        f.close

    texts.append(text)

df['text'] = texts
df['text_id'] = df['text'].apply(clean_text)

df.to_csv('./data/stories_indonesia.csv')

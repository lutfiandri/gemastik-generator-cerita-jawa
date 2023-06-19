import pandas as pd
import requests
import os

df = pd.read_csv('./data/urls.csv')

for i, row in df.iterrows():
    if i % 10 == 0:
        print("downloaded:", i)

    url = row['url']

    response = requests.get(url)

    # Check if the request was successful (status code 200 indicates success)
    if response.status_code == 200:
        # Get the HTML content from the response
        html_content = response.text
        title = os.path.basename(url)
        filename = f"./data/stories/{i}-{title}"

        with open(filename, "w+") as file:
            file.write(html_content)
            file.close()

import fitz
import json
import re
from unidecode import unidecode
import pandas as pd

# constant
regex_url_pattern = r"\b(?:[a-zA-Z]+\.[a-zA-Z]{2,3}\b|\bwww\.[a-zA-Z]+\.[a-zA-Z]{2,3}\b)"
chapter_delimiter = "||||"


def clean_pdf(filename):
    doc = fitz.open(filename)
    num_pages = len(doc)

    # Extract content from each page, excluding image captions
    content = []
    for i in range(3, num_pages):  # Process pages 3 to 9
        page = doc[i]
        blocks = page.get_text("dict", flags=11)["blocks"]

        lines = []

        for block in blocks:
            for line in block['lines']:
                # alg to ignore title -> entire line is bold
                is_title_line = True
                for span in line['spans']:
                    if not 'bold' in span['font'].lower():
                        is_title_line = False

                if is_title_line:
                    lines.append(chapter_delimiter)

                # alg to ignore image subtitle -> entire line is italic
                is_line_pic_subtitle = True
                for span in line['spans']:
                    if not 'italic' in span['font'].lower():
                        is_line_pic_subtitle = False

                # alg to ignore line that contains url -> use regex
                is_line_contains_url = False
                for span in line['spans']:
                    urls = re.findall(regex_url_pattern, span['text'])
                    if len(urls) > 0:
                        is_line_contains_url = True

                if not (is_title_line or is_line_pic_subtitle or is_line_contains_url):
                    lineString = ' '.join(
                        [span['text'] for span in line['spans']])
                    lines.append(lineString)

        # Remove lines that only have minimum 4 chars (assuming page number max at 3 digits)
        lines = [line for line in lines if len(line.strip()) > 3]

        content.extend(lines)

    # Join the extracted lines into a single string
    joined_text = ' '.join(content)
    joined_text = unidecode(joined_text)
    joined_text = re.sub(r"\s+", " ", joined_text)

    splitted_text = split_text_into_chunks(joined_text, words_per_chunk=300)

    doc.close()

    return splitted_text


def split_text_into_chunks(text, words_per_chunk=30):
    chunks = []

    chapters = text.split(chapter_delimiter)
    chapters = [s for s in chapters if s.strip()]

    # print(text)

    for chapter in chapters:
        sentences = chapter.split('.')
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


# Usage example
filename = 'bebuka-tanah-djawi.pdf'
splitted_text = clean_pdf(filename)

# for row in splitted_text:
#     print(row)
#     print()

df = pd.DataFrame({
    'text_jw': splitted_text
})

df.to_csv('bebuka-tanah-djawi.csv')

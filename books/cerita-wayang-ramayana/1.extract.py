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

    ignored_pages = []
    ignored_pages.extend(list(range(0, 8)))
    ignored_pages.extend([16, 17])
    ignored_pages.extend([26, 27])
    ignored_pages.extend([37, 38])
    ignored_pages.extend([51, 52])
    ignored_pages.extend([63, 64])
    ignored_pages.extend(list(range(64, num_pages)))

    # Extract content from each page, excluding image captions
    content = []
    for i in range(num_pages):  # Process pages 3 to 9
        if i in ignored_pages:
            continue

        page = doc[i]
        blocks = page.get_text("dict", flags=0)["blocks"]

        lines = []

        for block in blocks:
            for line in block['lines']:
                # alg to ignore title -> entire line is bold
                is_title_line = True
                # FIXME: fitz can't read the title in the end of page
                for span in line['spans']:
                    if not 'bold' in span['font'].lower():
                        is_title_line = False

                # FIXME: fitz can't read the title in the end of page
                # if is_title_line:
                    # lines.append(chapter_delimiter)

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

                # alg to ignore footer -> above the page number
                is_line_footer = False
                line_tmp = ''
                for span in line['spans']:
                    line_tmp += span['text']
                pattern = r"^\*.*\*$"
                if bool(re.match(pattern, span['text'])):
                    is_line_footer = True

                if not (is_title_line or is_line_pic_subtitle or is_line_contains_url or is_line_footer):
                    lineString = ' '.join(
                        [span['text'] for span in line['spans']])
                    lines.append(lineString)

                    print(json.dumps(line['spans'], indent=2))

        # Remove lines that only have minimum 4 chars (assuming page number max at 3 digits)
        lines = [line for line in lines if len(line.strip()) > 3]

        content.extend(lines)

    # Join the extracted lines into a single string
    joined_text = ' '.join(content)
    joined_text = unidecode(joined_text)
    joined_text = re.sub(r"\s+", " ", joined_text)

    print(joined_text)
    print()

    splitted_text = split_text_into_chunks(joined_text, words_per_chunk=300)

    doc.close()

    return splitted_text


def split_text_into_chunks(text, words_per_chunk=30):
    chunks = []

    chapters = text.split(chapter_delimiter)
    chapters = [s for s in chapters if s.strip()]

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
filename = 'cerita-wayang-ramayana.pdf'
splitted_text = clean_pdf(filename)


for row in splitted_text:
    print(row)
    print()

df = pd.DataFrame({
    'text_jw': splitted_text
})

df.to_csv('cerita-wayang-ramayana.csv')

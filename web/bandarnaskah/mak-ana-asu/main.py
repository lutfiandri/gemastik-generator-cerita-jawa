from unidecode import unidecode
import re
import pandas as pd


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


lines = []
with open('file.txt', "r") as file:
    lines = file.readlines()
    file.close()


lines = [line.strip() for line in lines]
print(len(lines))

new_lines = []

for line in lines:
    arr = line.split(":")
    # print(arr)
    if len(arr) > 1:
        clean_arr = arr[1:]
        clean_text = ' '.join(clean_arr)
        clean_text = clean_text.replace("”", "")
        clean_text = clean_text.replace("“", "")
        clean_text = clean_text.strip()

        if clean_text.isupper():
            clean_text = clean_text.capitalize()

        new_lines.append(clean_text)

# print(new_lines)
story_text = " ".join(new_lines)


story_text = unidecode(story_text)
story_text = re.sub(r"\s+", " ", story_text)

story_arr = split_text_into_chunks(story_text, 300)
print(story_arr)

df = pd.DataFrame({
    'text_jw': story_arr
})

df.to_csv('mak-ana-asu.csv')

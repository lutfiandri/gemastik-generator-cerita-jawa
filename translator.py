from googletrans import Translator
import pandas as pd
from tqdm import tqdm

tqdm.pandas()


translator = Translator()


def remove_incomplete_sentence(text: str) -> str:
    result = text.rsplit(".", 1)[0]
    return result


def translate_id_to_jw(text: str) -> str:
    words = text.split()  # Split the text into words
    text = ' '.join(words[:300])
    # text = remove_incomplete_sentence(text)

    translation = translator.translate(text, dest="jw", src="id")

    return translation.text


df = pd.read_csv('./data/stories_indonesia.csv', index_col=0)

df['text_jw'] = df['text_id'].progress_apply(translate_id_to_jw)

df.to_csv('./data/stories_javanese.csv')

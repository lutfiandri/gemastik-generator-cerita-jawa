def split_text_into_chunks(text, words_per_chunk=30):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) <= words_per_chunk:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# Usage example
text = """
The quick brown fox jumps over the lazy dog. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed euismod, lacus sed lobortis condimentum, tortor tellus pharetra lacus, et feugiat dolor dui ac elit. 
Proin auctor vehicula justo, et pellentesque orci elementum id. Nullam faucibus mollis massa, in convallis 
quam pharetra in. Vestibulum consectetur erat non velit egestas finibus. Nam commodo lectus sit amet 
ligula rutrum, vitae placerat dui lobortis. Nulla porttitor neque vel enim ultrices, ac malesuada ipsum 
dictum. Sed et ultrices sapien, nec convallis lectus. Nunc eu scelerisque metus, in dignissim purus. 
"""

chunks = split_text_into_chunks(text, words_per_chunk=30)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")

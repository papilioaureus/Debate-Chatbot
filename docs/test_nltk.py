import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk
from nltk.chunk import tree2conlltags
from nltk.util import ngrams
from nltk.corpus import stopwords

nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_keywords_from_text(text):
    stop_words = set(stopwords.words('english'))

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Initialize a set to store unique keywords
    keywords = set()
    
    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)
        
        for chunk in ne_chunk(pos_tags, binary=False):
            if hasattr(chunk, 'label'):
                keywords.add(" ".join(c[0] for c in chunk))
            else:
                word, tag = chunk
                if tag in ['NNP', 'NNPS'] and word.lower() not in stop_words:
                    keywords.add(word)
        
        filtered_words = [word for word in words if word[0].isupper()]
        
        # Extracting N-Grams (bigrams and trigrams as example)
        for n in range(2, 4):
            n_grams = ngrams(filtered_words, n)
            for grams in n_grams:
                joined_grams = " ".join(grams)
                # Check if the joined grams start with an uppercase letter (simple heuristic)
                if joined_grams[0].isupper():
                    keywords.add(joined_grams)
        
        # Adding individual proper nouns and specific nouns
        proper_nouns_and_nouns = [word for word, tag in pos_tags if tag in ['NNP', 'NNPS', 'NN', 'CD']]
        keywords.update(proper_nouns_and_nouns)
        
    # Optionally, filter out stopwords from the keywords
    filtered_keywords = [kw for kw in keywords if kw.lower() not in stop_words]
    return list(set(filtered_keywords))

# Example usage
text = "As a result, Washington might come to believe (wrongly) that it was about to become the victim of a nuclear attack—an effect termed misinterpreted warning. For example, China or Russia might attack U.S. early-warning satellites to enable their regional non-nuclear ballistic missiles (or, perhaps, non-nuclear ICBMs or boost-glide weapons in the future) to penetrate U.S. missile defenses. However, such an attack might be misinterpreted by the United States as an attempt to disable missile defenses designed to protect the homeland against limited nuclear strikes."
keywords = extract_keywords_from_text(text)
print(keywords)

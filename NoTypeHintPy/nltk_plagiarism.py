import os
from os.path import exists
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
if (os.name == 'nt'):
    data_dir = (__file__.rsplit('\\', 1)[0] + '\\nltk_data')
else:
    data_dir = (__file__.rsplit('/', 1)[0] + '/nltk_data')
nltk.data.path.append(data_dir)

def update():
    "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Update NLTK data if necessary.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    This function checks if the NLTK data directory exists and downloads the required\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    data if it doesn't.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    "
    if (not exists((data_dir + '/tokenizers'))):
        nltk.download('punkt', data_dir)
        nltk.download('punkt_tab', data_dir)
    if (not exists((data_dir + '/corpora'))):
        nltk.download('stopwords', data_dir)
        nltk.download('wordnet', data_dir)

def preprocess_text(text):
    '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Preprocess a text by tokenizing, removing punctuation and stop words, and lemmatizing.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Args:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        text (str): The text to preprocess.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Returns:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        str: The preprocessed text.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    '
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if (word.isalnum() and (word.lower() not in stop_words))]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    processed_text = ' '.join(tokens)
    return processed_text

def calculate_similarity(query_features, reference_features):
    '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Calculate the cosine similarity between two sets of features.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Args:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        query_features (scipy.sparse.csr_matrix): The features of the query text.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        reference_features (scipy.sparse.csr_matrix): The features of the reference texts.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Returns:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        list: A list of similarity scores, one for each reference text.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    '
    if (query_features.shape[1] != reference_features.shape[1]):
        reference_features = reference_features.T
    if (query_features.shape[1] != reference_features.shape[1]):
        raise ValueError('Incompatible dimensions for query and reference features')
    similarity = cosine_similarity(query_features, reference_features)
    return similarity

def bow_features(texts):
    '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Extract bag-of-words features from a list of texts.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Args:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        texts (list): A list of texts.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Returns:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        tuple: A tuple containing the features and the vectorizer.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    '
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(texts)
    return (features, vectorizer)

def tfidf_features(texts):
    '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Extract TF-IDF features from a list of texts.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Args:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        texts (list): A list of texts.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Returns:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        tuple: A tuple containing the features and the vectorizer.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    '
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(texts)
    return (features, vectorizer)

def get_similarity_score(query_text, reference_texts):
    '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Calculate the cosine similarity between a query text and one or more reference texts.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Args:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        query_text (str): The query text.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        reference_texts (list): A list of reference texts.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    Returns:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n        list: A list of tuples, where each tuple contains the reference text and its corresponding similarity score.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    '
    preprocessed_query = preprocess_text(query_text)
    preprocessed_references = [preprocess_text(text) for text in reference_texts]
    (features_query, vectorizer) = tfidf_features(([preprocessed_query] + preprocessed_references))
    features_references = features_query[1:]
    features_query = features_query[:1]
    similarity_scores = calculate_similarity(features_query, features_references)
    plagiarism_results = []
    for (i, score) in enumerate(similarity_scores[0]):
        plagiarism_results.append([reference_texts[i], score])
    return plagiarism_results
if (__name__ == '__main__'):
    update()
    with open('test2_1.txt', 'r') as file:
        example_document = file.read()
    reference_texts = []
    files = ['test2_2.txt', 'test2_3.txt', 'test2_4.txt']
    for file in files:
        with open(file, 'r') as f:
            reference_texts.append(f.read())
    try:
        results = get_similarity_score(example_document, reference_texts)
        if results:
            print('Plagiarized content detected:')
            for result in results:
                print(f'Similarity Score: {(result[1] * 100):.2f}%')
                print()
        else:
            print('No plagiarism detected.')
    except ValueError as e:
        print('Error:', e)
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from os.path import exists

# Set data directory for NLTK data
if os.name == 'nt':
    data_dir = __file__.rsplit("\\", 1)[0] + "\\nltk_data"
else:
    data_dir = __file__.rsplit("/", 1)[0] + "/nltk_data"
nltk.data.path.append(data_dir)

def update():
    """
    Update NLTK data if necessary.
    
    This function checks if the NLTK data directory exists and downloads the required
    data if it doesn't.
    """
    if not exists(data_dir + "/tokenizers"):
        nltk.download('punkt', data_dir)
        nltk.download('punkt_tab', data_dir)
    if not exists(data_dir + "/corpora"):
        nltk.download('stopwords', data_dir)
        nltk.download('wordnet', data_dir)


def preprocess_text(text:str) -> str:
    """
    Preprocess a text by tokenizing, removing punctuation and stop words, and lemmatizing.
    
    Args:
        text (str): The text to preprocess.
    
    Returns:
        str: The preprocessed text.
    """
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()

    # Tokenization
    tokens = word_tokenize(text)

    # Removing punctuation and stop words
    tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]

    # Lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join the tokens back into a single string
    processed_text = ' '.join(tokens)

    return processed_text



def calculate_similarity(query_features, reference_features):
    """
    Calculate the cosine similarity between two sets of features.
    
    Args:
        query_features (scipy.sparse.csr_matrix): The features of the query text.
        reference_features (scipy.sparse.csr_matrix): The features of the reference texts.
    
    Returns:
        list: A list of similarity scores, one for each reference text.
    """
    # Check dimensions and transpose if necessary
    if query_features.shape[1] != reference_features.shape[1]:
        reference_features = reference_features.T

    # Check dimensions again after potential transposition
    if query_features.shape[1] != reference_features.shape[1]:
        raise ValueError("Incompatible dimensions for query and reference features")

    similarity = cosine_similarity(query_features, reference_features)
    return similarity


def bow_features(texts:str) -> tuple:
    """
    Extract bag-of-words features from a list of texts.
    
    Args:
        texts (list): A list of texts.
    
    Returns:
        tuple: A tuple containing the features and the vectorizer.
    """
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(texts)
    return features, vectorizer

def tfidf_features(texts:str) -> tuple:
    """
    Extract TF-IDF features from a list of texts.
    
    Args:
        texts (list): A list of texts.
    
    Returns:
        tuple: A tuple containing the features and the vectorizer.
    """
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(texts)
    return features, vectorizer

def get_similarity_score(query_text, reference_texts):
    """
    Calculate the cosine similarity between a query text and one or more reference texts.
    
    Args:
        query_text (str): The query text.
        reference_texts (list): A list of reference texts.
    
    Returns:
        list: A list of tuples, where each tuple contains the reference text and its corresponding similarity score.
    """
    preprocessed_query = preprocess_text(query_text)
    preprocessed_references = [preprocess_text(text) for text in reference_texts]

    # Extract TF-IDF features for query and reference texts
    features_query, vectorizer = tfidf_features([preprocessed_query] + preprocessed_references)
    features_references = features_query[1:]
    features_query = features_query[:1]  # Extract query feature separately

    # Calculate similarity
    similarity_scores = calculate_similarity(features_query, features_references)

    
    # Identify plagiarized content
    plagiarism_results = []
    for i, score in enumerate(similarity_scores[0]):
        plagiarism_results.append([reference_texts[i], score])
    return plagiarism_results

if __name__ == "__main__":
    update()
    # Read example document from file
    with open("test2_1.txt", "r") as file:
        example_document = file.read()
        
    # Define the reference texts
    reference_texts = []

    # Read reference texts from files
    files = ["test2_2.txt", "test2_3.txt", "test2_4.txt"]
    for file in files:
        with open(file, "r") as f:
            reference_texts.append(f.read())

    try:
        # Test plagiarism detection
        results = get_similarity_score(example_document, reference_texts)

        # Print results
        if results:
            print("Plagiarized content detected:")
            for result in results:
                print(f"Similarity Score: {(result[1]*100):.2f}%")
                print()
        else:
            print("No plagiarism detected.")
    except ValueError as e:
        print("Error:", e)

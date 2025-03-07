import nltk
from nltk.corpus import stopwords, framenet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def update():
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download("wordnet_ic")
    nltk.download("omw-1.4")
    nltk.download("lin_thesaurus")
    nltk.download("framenet_v17")
    nltk.download("universal_treebanks_v20")


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
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
    # Check dimensions and transpose if necessary
    if query_features.shape[1] != reference_features.shape[1]:
        reference_features = reference_features.T

    # Check dimensions again after potential transposition
    if query_features.shape[1] != reference_features.shape[1]:
        raise ValueError("Incompatible dimensions for query and reference features")

    similarity = cosine_similarity(query_features, reference_features)
    return similarity


def bow_features(texts):
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(texts)
    return features, vectorizer

def tfidf_features(texts):
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(texts)
    return features, vectorizer

def detect_plagiarism(query_text, reference_texts, threshold=0.8):
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
        if score >= threshold:
            plagiarism_results.append({
                'reference_text': reference_texts[i],
                'similarity_score': score
            })

    return plagiarism_results

if __name__ == "__main__":
    #update()
    # Read example document from file
    with open("test.txt", "r") as file:
        example_document = file.read()

    # Read reference texts from files
    with open("test2.txt", "r") as file:
        reference_text1 = file.read()

    # Define the reference texts
    reference_texts = [reference_text1]

    try:
        # Test plagiarism detection
        results = detect_plagiarism(example_document, reference_texts)

        # Print results
        if results:
            print("Plagiarized content detected:")
            for result in results:
                print("Similarity Score:", result['similarity_score'])
                print()
        else:
            print("No plagiarism detected.")
    except ValueError as e:
        print("Error:", e)
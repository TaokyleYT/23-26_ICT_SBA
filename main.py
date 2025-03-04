import re
import helpers

def read_file(file_path):
    """Read a text file and return its content as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        if not content.strip():
            print(f"Warning: File '{file_path}' is empty.")
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {str(e)}")
        return None

def clean_text(text):
    """Remove punctuation and convert text to lowercase."""
    if text is None:
        return ""
    # Replace all punctuation with spaces
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def count_words(text):
    """Count the frequency of each word in the text."""
    if not text:
        return ([],[])
    
    word_count = ([],[])
    words = text.split(" ")
    
    for word in words:
        if word in word_count[0]:
            word_count[1][helpers.linear_search(word_count[0], word)] += 1
        else:
            word_count[0].append(word)
            word_count[1].append(1)

    return word_count

def get_total_words(word_count):
    """Return the total number of words in a text."""
    total = 0
    for count in word_count[1]:
        total += count
    return total

def get_unique_words(word_count):
    """Return the number of unique words in a text."""
    return len(word_count)

def sort_alphabetically(word_count):
    """Sort words alphabetically using quick_sort from helpers."""
    words = word_count[0]
    sorted_words = helpers.quick_sort(words)
    result = []
    for word in sorted_words:
        result.append((word, word_count[1][helpers.linear_search(word_count[0], word)]))
    return result

def sort_by_frequency(word_count):
    """Sort words by frequency (highest to lowest)."""
    # Create a list of (word, count) tuples
    word_items = []
    for idx in range(len(word_count[0])):
        word_items.append((word_count[0][idx], word_count[1][idx]))
    
    # Sort based on count (second element in tuple)
    # Create a custom comparison function for the quick_sort
    def get_comparison_key(item):
        return (-item[1], item[0])  # Sort by -count, then by word
    
    # Create a list that can be sorted using the quick_sort function
    # We'll sort based on the negative count, so higher counts come first
    items_to_sort = []
    for i, item in enumerate(word_items):
        items_to_sort.append((get_comparison_key(item), i))
    
    sorted_indices = helpers.quick_sort(items_to_sort)
    
    # Reconstruct the result using the sorted indices
    result = []
    for _, idx in sorted_indices:
        result.append(word_items[idx])
    
    return result

def calculate_similarity(word_count1, word_count2):
    """Calculate the similarity percentage between two texts based on word frequencies."""
    if not word_count1 or not word_count2:
        return 0.0
    
    # Get all unique words from both texts
    all_words = []
    common_words = 0
    
    for word in word_count1:
        if word not in all_words:
            all_words.append(word)
    
    for word in word_count2:
        if word in word_count1:
            common_words += 1
        if word not in all_words:
            all_words.append(word)
    
    # Calculate similarity percentage
    similarity = (common_words / len(all_words)) * 100
    return similarity

def search_word(text, target_word):
    """Search for a target word in the text and return its positions."""
    if not text or not target_word:
        return []
    
    words = text.split()
    target_word = target_word.lower()
    positions = []
    
    for i, word in enumerate(words):
        if word.lower() == target_word:
            positions.append(i)
    
    return positions

def replace_word(text, target_word, replacement_word):
    """Replace a target word with a replacement word and return the modified text."""
    if not text or not target_word:
        return text
    
    words = text.split()
    target_word = target_word.lower()
    
    for i, word in enumerate(words):
        if word.lower() == target_word:
            words[i] = replacement_word
    
    return ' '.join(words)

def display_results(file_path, word_count, total_words, unique_words):
    """Display analysis results for a single file."""
    print(f"\n{'='*60}")
    print(f"Analysis of '{file_path}':")
    print(f"{'='*60}")
    print(f"Total words: {total_words}")
    print(f"Unique words: {unique_words}")
    
    # Display top 10 most frequent words
    print("\nTop 10 Most Frequent Words:")
    print(f"{'-'*30}")
    frequency_sorted = sort_by_frequency(word_count)
    for i, (word, count) in enumerate(frequency_sorted[:10]):
        print(f"{i+1}. '{word}': {count} times")
    
    # Display first 10 words alphabetically
    print("\nFirst 10 Words (Alphabetically):")
    print(f"{'-'*30}")
    alpha_sorted = sort_alphabetically(word_count)
    for i, (word, count) in enumerate(alpha_sorted[:10]):
        print(f"{i+1}. '{word}': {count} times")

def compare_files(file_path1, file_path2):
    """Compare two text files and calculate their similarity percentage."""
    # Read and process the files
    content1 = read_file(file_path1)
    content2 = read_file(file_path2)
    
    if content1 is None or content2 is None:
        print("Error: Cannot compare files due to reading errors.")
        return
    
    clean_content1 = clean_text(content1)
    clean_content2 = clean_text(content2)
    
    word_count1 = count_words(clean_content1)
    word_count2 = count_words(clean_content2)
    
    total_words1 = get_total_words(word_count1)
    total_words2 = get_total_words(word_count2)
    
    unique_words1 = get_unique_words(word_count1)
    unique_words2 = get_unique_words(word_count2)
    
    # Display analysis results for each file
    display_results(file_path1, word_count1, total_words1, unique_words1)
    display_results(file_path2, word_count2, total_words2, unique_words2)
    
    # Calculate and display similarity percentage
    similarity = calculate_similarity(word_count1, word_count2)
    
    print(f"\n{'='*60}")
    print(f"Comparison between '{file_path1}' and '{file_path2}':")
    print(f"{'='*60}")
    print(f"Similarity percentage: {similarity:.2f}%")
    
    # Determine plagiarism level based on similarity
    if similarity > 80:
        print("Plagiarism Level: HIGH - These texts are very similar")
    elif similarity > 50:
        print("Plagiarism Level: MEDIUM - These texts have significant overlap")
    elif similarity > 20:
        print("Plagiarism Level: LOW - These texts have some common elements")
    else:
        print("Plagiarism Level: MINIMAL - These texts are mostly different")

def analyze_file(file_path):
    """Analyze a single text file."""
    # Read and process the file
    content = read_file(file_path)
    
    if content is None:
        return
    
    clean_content = clean_text(content)
    word_count = count_words(clean_content)
    total_words = get_total_words(word_count)
    unique_words = get_unique_words(word_count)
    
    # Display analysis results
    display_results(file_path, word_count, total_words, unique_words)
    
    return word_count, clean_content

def main():
    """Main function to run the Word Analysis and Plagiarism Detection System."""
    print("Word Analysis and Plagiarism Detection System")
    print("--------------------------------------------")
    
    while True:
        print("\nMenu:")
        print("1. Analyze a single file")
        print("2. Compare two files for plagiarism")
        print("3. Search for a word in a file")
        print("4. Replace a word in a file")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            file_path = input("Enter the path to the text file: ").strip()
            analyze_file(file_path)
        
        elif choice == '2':
            file_path1 = input("Enter the path to the first text file: ").strip()
            file_path2 = input("Enter the path to the second text file: ").strip()
            compare_files(file_path1, file_path2)
        
        elif choice == '3':
            file_path = input("Enter the path to the text file: ").strip()
            content = read_file(file_path)
            
            if content is not None:
                target_word = input("Enter the word to search for: ").strip()
                clean_content = clean_text(content)
                positions = search_word(clean_content, target_word)
                
                if positions:
                    print(f"The word '{target_word}' appears {len(positions)} times at positions: {positions}")
                else:
                    print(f"The word '{target_word}' was not found in the file.")
        
        elif choice == '4':
            file_path = input("Enter the path to the text file: ").strip()
            content = read_file(file_path)
            
            if content is not None:
                target_word = input("Enter the word to replace: ").strip()
                replacement_word = input("Enter the replacement word: ").strip()
                
                clean_content = clean_text(content)
                modified_content = replace_word(clean_content, target_word, replacement_word)
                
                print("\nOriginal text (cleaned):")
                print(clean_content[:100] + "..." if len(clean_content) > 100 else clean_content)
                
                print("\nModified text:")
                print(modified_content[:100] + "..." if len(modified_content) > 100 else modified_content)
                
                save_option = input("\nDo you want to save the modified text to a new file? (y/n): ").strip().lower()
                if save_option == 'y':
                    new_file_path = input("Enter the path for the new file: ").strip()
                    try:
                        with open(new_file_path, 'w', encoding='utf-8') as file:
                            file.write(modified_content)
                        print(f"Modified text saved to '{new_file_path}'")
                    except Exception as e:
                        print(f"Error saving file: {str(e)}")
        
        elif choice == '5':
            print("Thank you for using the Word Analysis and Plagiarism Detection System!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
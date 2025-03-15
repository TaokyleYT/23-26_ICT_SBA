import os  # Import module for terminal size detection and file operations
import helpers  # Import custom helper functions that avoid using built-in functions
from helpers import animated_print as print, animated_input as input  # Use animated versions of print/input
import tkinter as tk  # Import tkinter for GUI implementation
from tkinter import ttk, filedialog, messagebox  # Import specific tkinter components
import matplotlib.pyplot as plt  # Import matplotlib for data visualization
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # For embedding matplotlib in tkinter
import argparse  # For command-line argument parsing


def read_file(file_path):
    """
    Read a text file and return its content as a string.
    
    Args:
        file_path (str): Path to the file to be read
        
    Returns:
        str or None: The content of the file as a string, or None if an error occurred
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        if not content.strip():
            print(f"\x1b[33;40mWarning: File '{file_path}' is empty.\x1b[m")
        return content
    except FileNotFoundError:
        print(f"\x1b[31;40mError: File '{file_path}' not found.\x1b[m")
        return None
    except Exception as e:
        print(f"\x1b[31;40mError reading file '{file_path}': {str(e)}\x1b[m")
        return None


def clean_text(text):
    """
    Remove punctuation and convert text to lowercase.
    
    Args:
        text (str or None): Text to be cleaned
        
    Returns:
        str: Cleaned text with punctuation removed, converted to lowercase
             and with no extra spaces
    """
    if text is None:
        return ""

    # Replace any character that isn't a letter, digit, or space with a space
    cleaned_text = "".join((char if 'a' <= char <= 'z' or '0' <= char <= '9'
                            or char == ' ' else ' ') for char in text.lower())

    # Remove extra spaces (replace double spaces with single until no doubles remain)
    while '  ' in cleaned_text:
        cleaned_text = cleaned_text.replace('  ', ' ')

    return cleaned_text.strip()


def count_words(text):
    """
    Count the frequency of each word in the text.
    
    Args:
        text (str): Cleaned text to analyze
        
    Returns:
        tuple: A tuple containing two lists:
            - List of unique words
            - List of corresponding frequencies
    """
    if not text:
        return ([], [])

    # Initialize result structure as a tuple of two lists
    word_count = ([], [])
    words = text.split(" ")

    # Count frequency of each word
    for n in range(len(words)):
        word = words[n]
        if word in word_count[0]:
            # If word already exists in our list, increment its count
            word_index = helpers.linear_search(word_count[0], word)
            word_count[1][word_index] += 1
        else:
            # Otherwise, add it to our list with a count of 1
            word_count[0].append(word)
            word_count[1].append(1)

    return word_count


def get_total_words(word_count):
    """
    Calculate the total number of words in a text.
    
    Args:
        word_count (tuple): A tuple of (words, frequencies) as returned by count_words()
        
    Returns:
        int: Total word count (sum of all frequencies)
    """
    total = 0
    for count in word_count[1]:
        total += count
    return total


def get_unique_words(word_count):
    """
    Get the number of unique words in a text.
    
    Args:
        word_count (tuple): A tuple of (words, frequencies) as returned by count_words()
        
    Returns:
        int: Number of unique words
    """
    return len(word_count[0])


def sort_alphabetically(word_count):
    """
    Sort words alphabetically using quick_sort from helpers.
    
    Args:
        word_count (tuple): A tuple of (words, frequencies) as returned by count_words()
        
    Returns:
        list: List of (word, frequency) tuples sorted alphabetically
    """
    words = word_count[0]
    # Sort words alphabetically
    sorted_words = helpers.quick_sort(words)

    # Create list of (word, frequency) pairs
    result = []
    for n in range(len(sorted_words)):
        word = sorted_words[n]
        # Find the index of the word in the original list to get its frequency
        result.append(
            (word, word_count[1][helpers.linear_search(word_count[0], word)]))
    return result


def sort_by_frequency(word_count):
    """
    Sort words by frequency (highest to lowest).
    
    Args:
        word_count (tuple): A tuple of (words, frequencies) as returned by count_words()
        
    Returns:
        list: List of (word, frequency) tuples sorted by frequency (highest first)
    """
    # Create a list of (word, count) tuples
    word_items = []
    for idx in range(len(word_count[0])):
        word_items.append((word_count[0][idx], word_count[1][idx]))

    # Create a function that generates a comparison key for sorting
    def get_comparison_key(item):
        return (-item[1], item[0]
                )  # Sort by -count (for descending), then by word

    # Create a list that can be sorted using the quick_sort function
    # Using indices to maintain the original items
    items_to_sort = []
    for i, item in enumerate(word_items):
        items_to_sort.append((get_comparison_key(item), i))

    # Sort the indices
    sorted_indices = helpers.quick_sort(items_to_sort)

    # Reconstruct the result using the sorted indices
    result = []
    for _, idx in sorted_indices:
        result.append(word_items[idx])

    return result


def calculate_similarity(word_count1, word_count2):
    """
    Calculate the similarity percentage between two texts based on word frequencies.
    
    Args:
        word_count1 (tuple): Word count data for the first text
        word_count2 (tuple): Word count data for the second text
        
    Returns:
        float: Similarity percentage (0-100)
    """
    # Get all unique words from both texts
    all_words = []
    common_words = 0

    # Add all words from first text to all_words list
    for word in word_count1[0]:
        if word not in all_words:
            all_words.append(word)

    # Count common words and add unique words from second text
    for word in word_count2[0]:
        if word in word_count1[0]:
            common_words += 1
        if word not in all_words:
            all_words.append(word)

    # Calculate similarity percentage
    return (common_words / len(all_words)) * 100


class WordAnalysisApp:
    """
    GUI application for word analysis and plagiarism detection.
    
    This class implements a tkinter-based graphical user interface for:
    - Analyzing individual text files (word count, sorting, frequency graphs)
    - Comparing two files for potential plagiarism
    """

    def __init__(self, root, size="1000x700"):
        """
        Initialize the application with the tkinter root window.
        
        Args:
            root: Tkinter root window
            size (str): Window size in format "widthxheight"
        """
        self.root = root
        self.root.title("Word Analysis and Plagiarism Detection")
        self.root.geometry(size)

        # Create the main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.create_analyze_tab()
        self.create_compare_tab()

        # Variables to store file paths and analysis results
        self.file_path1 = ""
        self.file_path2 = ""
        self.word_count1 = None
        self.word_count2 = None
        self.clean_content1 = ""
        self.clean_content2 = ""

        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TNotebook", background="#f0f0f0")
        style.configure("TFrame", background="#f0f0f0")

    def create_analyze_tab(self):
        """
        Create the Analyze tab for single file analysis.
        
        This tab contains:
        - File selection controls
        - Word statistics display
        - Word frequency and alphabetical lists
        - Word frequency graph
        """
        analyze_tab = ttk.Frame(self.notebook)
        self.notebook.add(analyze_tab, text="Analyze File")

        # File selection
        file_frame = ttk.Frame(analyze_tab)
        file_frame.pack(fill=tk.X, pady=10)

        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.file_entry1 = ttk.Entry(file_frame, width=50)
        self.file_entry1.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        browse_btn = ttk.Button(file_frame,
                                text="Browse",
                                command=self.browse_file1)
        browse_btn.pack(side=tk.LEFT, padx=5)

        analyze_btn = ttk.Button(file_frame,
                                 text="Analyze",
                                 command=self.analyze_file)
        analyze_btn.pack(side=tk.LEFT, padx=5)

        # Results section
        results_frame = ttk.Frame(analyze_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Left side - stats and lists
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        stats_frame = ttk.LabelFrame(left_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, pady=5)

        self.stats_text = tk.Text(stats_frame,
                                  height=5,
                                  width=40,
                                  wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        lists_frame = ttk.Frame(left_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Frequency list
        freq_frame = ttk.LabelFrame(lists_frame, text="Most Frequent Words")
        freq_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.freq_list = tk.Listbox(freq_frame, height=15)
        self.freq_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Alphabetical list
        alpha_frame = ttk.LabelFrame(lists_frame, text="Alphabetical Words")
        alpha_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.alpha_list = tk.Listbox(alpha_frame, height=15)
        self.alpha_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right side - graph
        right_frame = ttk.Frame(results_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        graph_frame = ttk.LabelFrame(right_frame, text="Word Frequency Graph")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.graph_canvas1 = tk.Canvas(graph_frame)
        self.graph_canvas1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_compare_tab(self):
        """
        Create the Compare tab for plagiarism detection.
        
        This tab contains:
        - File selection for two files
        - Statistics for both files
        - Similarity comparison results
        - Word frequency comparison graph
        """
        compare_tab = ttk.Frame(self.notebook)
        self.notebook.add(compare_tab, text="Compare Files")

        # File selection frame
        files_frame = ttk.Frame(compare_tab)
        files_frame.pack(fill=tk.X, pady=10)

        # File 1
        file1_frame = ttk.Frame(files_frame)
        file1_frame.pack(fill=tk.X, pady=5)

        ttk.Label(file1_frame, text="File 1:").pack(side=tk.LEFT, padx=5)
        self.compare_file_entry1 = ttk.Entry(file1_frame, width=50)
        self.compare_file_entry1.pack(side=tk.LEFT,
                                      padx=5,
                                      fill=tk.X,
                                      expand=True)

        browse_btn1 = ttk.Button(file1_frame,
                                 text="Browse",
                                 command=self.browse_compare_file1)
        browse_btn1.pack(side=tk.LEFT, padx=5)

        # File 2
        file2_frame = ttk.Frame(files_frame)
        file2_frame.pack(fill=tk.X, pady=5)

        ttk.Label(file2_frame, text="File 2:").pack(side=tk.LEFT, padx=5)
        self.compare_file_entry2 = ttk.Entry(file2_frame, width=50)
        self.compare_file_entry2.pack(side=tk.LEFT,
                                      padx=5,
                                      fill=tk.X,
                                      expand=True)

        browse_btn2 = ttk.Button(file2_frame,
                                 text="Browse",
                                 command=self.browse_compare_file2)
        browse_btn2.pack(side=tk.LEFT, padx=5)

        compare_btn = ttk.Button(files_frame,
                                 text="Compare Files",
                                 command=self.compare_files)
        compare_btn.pack(pady=10)

        # Results section
        results_frame = ttk.Frame(compare_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Side by side comparison of file statistics
        stats_frame = ttk.Frame(results_frame)
        stats_frame.pack(fill=tk.X, pady=5)

        # File 1 stats
        file1_stats_frame = ttk.LabelFrame(stats_frame,
                                           text="File 1 Statistics")
        file1_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.file1_stats_text = tk.Text(file1_stats_frame,
                                        height=5,
                                        width=40,
                                        wrap=tk.WORD)
        self.file1_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # File 2 stats
        file2_stats_frame = ttk.LabelFrame(stats_frame,
                                           text="File 2 Statistics")
        file2_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.file2_stats_text = tk.Text(file2_stats_frame,
                                        height=5,
                                        width=40,
                                        wrap=tk.WORD)
        self.file2_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Comparison results
        comparison_frame = ttk.LabelFrame(results_frame,
                                          text="Comparison Results")
        comparison_frame.pack(fill=tk.X, pady=10)

        self.comparison_text = tk.Text(comparison_frame,
                                       height=6,
                                       wrap=tk.WORD)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Graph comparing word frequencies
        graph_frame = ttk.LabelFrame(results_frame,
                                     text="Word Frequency Comparison")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.compare_canvas = tk.Canvas(graph_frame)
        self.compare_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def browse_file1(self):
        """
        Open a file dialog to browse for a file to analyze.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):
            self.file_entry1.delete(0, tk.END)
            self.file_entry1.insert(0, file_path)
            self.file_path1 = file_path

    def browse_compare_file1(self):
        """
        Open a file dialog to browse for the first file to compare.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):
            self.compare_file_entry1.delete(0, tk.END)
            self.compare_file_entry1.insert(0, file_path)

    def browse_compare_file2(self):
        """
        Open a file dialog to browse for the second file to compare.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):
            self.compare_file_entry2.delete(0, tk.END)
            self.compare_file_entry2.insert(0, file_path)

    def analyze_file(self):
        """
        Analyze a single file and display the results.
        
        This method:
        1. Reads the file content
        2. Cleans and analyzes the text
        3. Updates the statistics display
        4. Updates the word lists
        5. Creates and displays the frequency graph
        """
        file_path = self.file_entry1.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        # Read and process file
        content = read_file(file_path)
        if content is None:
            messagebox.showerror("Error", f"Could not read file: {file_path}")
            return

        clean_content = clean_text(content)
        word_count = count_words(clean_content)
        total_words = get_total_words(word_count)
        unique_words = get_unique_words(word_count)

        # Display statistics
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END,
                               f"File: {os.path.basename(file_path)}\n")
        self.stats_text.insert(tk.END, f"Total words: {total_words}\n")
        self.stats_text.insert(tk.END, f"Unique words: {unique_words}\n")

        # Display word lists
        self.freq_list.delete(0, tk.END)
        freq_sorted = sort_by_frequency(word_count)
        for i, (word, count) in enumerate(freq_sorted):
            self.freq_list.insert(tk.END, f"{i+1}. '{word}': {count} times")

        self.alpha_list.delete(0, tk.END)
        alpha_sorted = sort_alphabetically(word_count)
        for i, (word, count) in enumerate(alpha_sorted):
            self.alpha_list.insert(tk.END, f"{i+1}. '{word}': {count} times")

        # Create and display the frequency graph
        self.create_frequency_graph(word_count, self.graph_canvas1)

        # Store for later use
        self.word_count1 = word_count
        self.clean_content1 = clean_content

    def create_frequency_graph(self, word_count, canvas_widget, max_words=10):
        """
        Create a bar graph of word frequencies.
        
        Args:
            word_count (tuple): Word count data
            canvas_widget: Tkinter canvas to display the graph
            max_words (int): Maximum number of words to display in the graph
        """
        # Clear previous graph
        for widget in canvas_widget.winfo_children():
            widget.destroy()

        # Get the top words
        freq_sorted = sort_by_frequency(word_count)
        top_words = freq_sorted[:max_words]

        if not top_words:
            return

        # Create figure
        fig, ax = plt.subplots(figsize=(5, 4))

        words = [word for word, _ in top_words]
        counts = [count for _, count in top_words]

        # Create horizontal bar chart
        bars = ax.barh(words, counts, color='skyblue')

        # Add labels
        ax.set_xlabel('Frequency')
        ax.set_title('Top Word Frequencies')

        # Add count labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5,
                    bar.get_y() + bar.get_height() / 2,
                    f'{width}',
                    ha='left',
                    va='center')

        plt.tight_layout()

        # Embed the graph in the canvas
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def compare_files(self):
        """
        Compare two files for plagiarism detection.
        
        This method:
        1. Reads both files
        2. Cleans and analyzes the texts
        3. Calculates similarity percentage
        4. Updates the statistics and comparison displays
        5. Creates and displays the comparison graph
        """
        file_path1 = self.compare_file_entry1.get()
        file_path2 = self.compare_file_entry2.get()

        if not file_path1 or not file_path2:
            messagebox.showerror("Error", "Please select both files.")
            return

        # Read and process both files
        content1 = read_file(file_path1)
        content2 = read_file(file_path2)

        if content1 is None or content2 is None:
            messagebox.showerror("Error", "Could not read one or both files.")
            return

        clean_content1 = clean_text(content1)
        clean_content2 = clean_text(content2)

        word_count1 = count_words(clean_content1)
        word_count2 = count_words(clean_content2)

        total_words1 = get_total_words(word_count1)
        total_words2 = get_total_words(word_count2)

        unique_words1 = get_unique_words(word_count1)
        unique_words2 = get_unique_words(word_count2)

        # Display statistics for file 1
        self.file1_stats_text.delete(1.0, tk.END)
        self.file1_stats_text.insert(
            tk.END, f"File: {os.path.basename(file_path1)}\n")
        self.file1_stats_text.insert(tk.END, f"Total words: {total_words1}\n")
        self.file1_stats_text.insert(tk.END,
                                     f"Unique words: {unique_words1}\n")

        # Display statistics for file 2
        self.file2_stats_text.delete(1.0, tk.END)
        self.file2_stats_text.insert(
            tk.END, f"File: {os.path.basename(file_path2)}\n")
        self.file2_stats_text.insert(tk.END, f"Total words: {total_words2}\n")
        self.file2_stats_text.insert(tk.END,
                                     f"Unique words: {unique_words2}\n")

        # Calculate and display similarity
        similarity = calculate_similarity(word_count1, word_count2)

        self.comparison_text.delete(1.0, tk.END)
        self.comparison_text.insert(
            tk.END, f"Similarity percentage: {similarity:.2f}%\n\n")

        # Determine plagiarism level
        if similarity > 80:
            level = "HIGH - These texts are very similar"
        elif similarity > 50:
            level = "MEDIUM - These texts have significant overlap"
        elif similarity > 20:
            level = "LOW - These texts have some common elements"
        else:
            level = "MINIMAL - These texts are mostly different"

        self.comparison_text.insert(tk.END, f"Plagiarism Level: {level}")

        # Create comparison graph
        self.create_comparison_graph(word_count1, word_count2,
                                     self.compare_canvas)

    def create_comparison_graph(self,
                                word_count1,
                                word_count2,
                                canvas_widget,
                                max_words=5):
        """
        Create a comparison graph of word frequencies between two files.
        
        Args:
            word_count1 (tuple): Word count data for the first file
            word_count2 (tuple): Word count data for the second file
            canvas_widget: Tkinter canvas to display the graph
            max_words (int): Maximum number of words to display from each file
        """
        # Clear previous graph
        for widget in canvas_widget.winfo_children():
            widget.destroy()

        # Get top words from both files
        freq_sorted1 = sort_by_frequency(word_count1)
        freq_sorted2 = sort_by_frequency(word_count2)

        # Create sets of top words
        top_words1 = {word for word, _ in freq_sorted1[:max_words]}
        top_words2 = {word for word, _ in freq_sorted2[:max_words]}

        # Combine top words
        combined_top_words = list(top_words1.union(top_words2))

        if not combined_top_words:
            return

        # Get counts for each word in both files
        counts1 = []
        counts2 = []

        for word in combined_top_words:
            # Get count in file 1
            if word in word_count1[0]:
                idx = helpers.linear_search(word_count1[0], word)
                counts1.append(word_count1[1][idx])
            else:
                counts1.append(0)

            # Get count in file 2
            if word in word_count2[0]:
                idx = helpers.linear_search(word_count2[0], word)
                counts2.append(word_count2[1][idx])
            else:
                counts2.append(0)

        # Create figure
        fig, ax = plt.subplots(figsize=(5, 4))

        x = range(len(combined_top_words))
        width = 0.35

        # Create bar chart
        ax.bar(
            [i - width / 2 for i in x],
            counts1,
            width,
            label='File 1',
            color='skyblue',
        )
        ax.bar(
            [i + width / 2 for i in x],
            counts2,
            width,
            label='File 2',
            color='lightgreen',
        )

        # Add labels and legend
        ax.set_ylabel('Frequency')
        ax.set_title('Word Frequency Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(combined_top_words, rotation=45, ha='right')
        ax.legend()

        plt.tight_layout()

        # Embed the graph in the canvas
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        
        
def configure():
    #idk help me
    pass


def display_results(file_path,
                    word_count,
                    total_words,
                    unique_words,
                    show_nums=10,
                    warp=os.get_terminal_size().columns):
    """
    Display analysis results for a single file in CLI mode.
    
    Args:
        file_path (str): Path to the analyzed file
        word_count (tuple): Word count data
        total_words (int): Total number of words
        unique_words (int): Number of unique words
        show_nums (int): Number of top words to display
        warp (int): Number of columns to use for text wrapping
    """
    # Limit number of words to display to available words
    show_nums = helpers.min(show_nums, len(word_count[0]))
    hyphen_warp = helpers.min(warp, len(str(show_nums)) + 30)

    # Print header and statistics
    print(f"\
\n\
{'='*helpers.min(warp, len(file_path)+15)}\n\
Analysis of '{file_path}':\n\
{'='*helpers.min(warp, len(file_path)+15)}\n\
Total words: {total_words}\n\
Unique words: {unique_words}\n\
\n\
\n\
Top {show_nums} Most Frequent Words:\n\
{'-'*hyphen_warp}")

    # Print frequency-sorted words
    frequency_sorted = sort_by_frequency(word_count)
    txt = "".join(f"{i + 1}. '{word}': {count} times\n"
                  for i, (word,
                          count) in enumerate(frequency_sorted[:show_nums]))
    print(txt)

    # Print alphabetically-sorted words
    txt = f"\nFirst {show_nums} Words (Alphabetically):\n{'-'*hyphen_warp}\n"
    alpha_sorted = sort_alphabetically(word_count)
    for i, (word, count) in enumerate(alpha_sorted[:show_nums]):
        txt += f"{i+1}. '{word}': {count} times\n"
    print(txt)


def compare_files(file_path1, file_path2):
    """
    Compare two text files and calculate their similarity percentage for CLI mode.
    
    Args:
        file_path1 (str): Path to the first file
        file_path2 (str): Path to the second file
    """
    columns = os.get_terminal_size().columns

    # Read and process the files
    content1 = read_file(file_path1)
    content2 = read_file(file_path2)

    if content1 is None or content2 is None:
        print(
            "\x1b[31;40mError: Cannot compare files due to reading errors.\x1b[m"
        )
        return

    # Clean and analyze texts
    clean_content1 = clean_text(content1)
    clean_content2 = clean_text(content2)

    word_count1 = count_words(clean_content1)
    word_count2 = count_words(clean_content2)

    total_words1 = get_total_words(word_count1)
    total_words2 = get_total_words(word_count2)

    unique_words1 = get_unique_words(word_count1)
    unique_words2 = get_unique_words(word_count2)

    # Display analysis results for each file
    display_results(file_path1, word_count1, total_words1, unique_words1, config.compare_file_display_line)
    display_results(file_path2, word_count2, total_words2, unique_words2, config.compare_file_display_line)

    # Calculate and display similarity percentage
    similarity = calculate_similarity(word_count1, word_count2)

    print(
        f"\n{'='*helpers.min(columns, len(file_path1)+len(file_path2)+30)}\nComparison between '{file_path1}' and '{file_path2}':\n{'='*helpers.min(columns, len(file_path1)+len(file_path2)+30)}\nSimilarity percentage: {similarity:.2f}%"
    )

    # Determine and display plagiarism level with color coding
    if similarity > 80:
        print(
            "\x1b[31;40mPlagiarism Level: HIGH - These texts are very similar\x1b[m"
        )
    elif similarity > 50:
        print(
            "\x1b[33;40mPlagiarism Level: MEDIUM - These texts have significant overlap\x1b[m"
        )
    elif similarity > 20:
        print(
            "\x1b[92;40mPlagiarism Level: LOW - These texts have some common elements\x1b[m"
        )
    else:
        print(
            "\x1b[32;40mPlagiarism Level: MINIMAL - These texts are mostly different\x1b[m"
        )


def analyze_file(file_path):
    """
    Analyze a single text file for CLI mode.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        tuple: Word count data and cleaned content, or None if an error occurred
    """
    # Read and process the file
    content = read_file(file_path)

    if content is None:
        return

    clean_content = clean_text(content)
    word_count = count_words(clean_content)
    total_words = get_total_words(word_count)
    unique_words = get_unique_words(word_count)

    # Display analysis results
    display_results(file_path, word_count, total_words, unique_words, config.single_file_display_line)
    return word_count, 

def GUIexit(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        messagebox.showwarning("Thank you, app closing...", message="Thank you for using WAPDS")
        root.destroy()
        exit()


def mainGUI():
    """
    Start the GUI version of the Word Analysis and Plagiarism Detection System.
    
    Creates a tkinter window and initializes the application with a confirmation
    dialog when attempting to close the window.
    """
    root = tk.Tk()
    app = WordAnalysisApp(
        root)  # app is unused because tkinter handles the UI events

    # Set up close confirmation dialog
    root.protocol("WM_DELETE_WINDOW", lambda: GUIexit(root))

    # Start the main event loop
    root.mainloop()


def mainCLI():
    """
    Start the CLI version of the Word Analysis and Plagiarism Detection System.
    
    Presents a menu-based interface for file analysis and comparison.
    """
    columns = os.get_terminal_size().columns
    print("Word Analysis and Plagiarism Detection System\n" +
          "-" * helpers.min(columns, 45))

    while True:
        # Display main menu
        print("\
\nMenu:\n\
1. Analyze a single file\n\
2. Compare two files for plagiarism\n\
3. Configure settings\n\
4. Exit\n")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            file_path = input("Enter the path to the text file: ").strip()
            analyze_file(file_path)

        elif choice == '2':
            file_path1 = input(
                "Enter the path to the first text file: ").strip()
            file_path2 = input(
                "Enter the path to the second text file: ").strip()
            compare_files(file_path1, file_path2)

        elif choice == '3':
            configure()
        elif choice == '4':
            print(
                "Thank you for using WAPDS!"
            )
            break
        else:
            print(
                f"Invalid choice {repr(choice)}. Please enter a number between 1 and 4."
            )
            
            
class config:
    with open("WAPDS.config", "r") as f:
        config_data = f.readline().split(";")
    single_file_display_line = config_data[0]
    compare_file_display_line = config_data[1]


if __name__ == "__main__":
    # Parse command line arguments to determine whether to run GUI or CLI
    parser = argparse.ArgumentParser(
        description="Word Analysis and Plagiarism Detection System (WAPDS)")
    parser.add_argument(
        "run_type",
        help=
        'enter "GUI" or "CLI", determine whether a CLI or GUI version should run. default is GUI',
        nargs="?",
        default="GUI")
    args = parser.parse_args()

    # Start appropriate interface based on argument
    if args.run_type == "GUI":
        mainGUI()
    elif args.run_type == "CLI":
        mainCLI()
    else:
        parser.error(
            f'Please enter either "GUI" or "CLI" for run type, not {repr(args.run_type)}'
        )

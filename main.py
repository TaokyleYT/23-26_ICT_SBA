import re #regex
import os #get terminal size for text overflowing on CLI mode
import helpers #a bunch of non-functions (by me ofc) that prevents me from losing ALOT of marks due to using built-in functions
from helpers import animated_print as print #animate print lol
import tkinter as tk #tkinter is a module that allows me to go GUI WOOOOOOO
from tkinter import ttk, filedialog, messagebox #frequently used stuff I dont wanna type "tkinter." everytime I use them
import matplotlib.pyplot as plt #graphs and charts so I dont need to suffer using pure tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #used whenever I make a chart, COMEON NOBODY WANNA TYPE THIS LONG AHH THING EVERYTIME
import argparse #so I know if u want CLI or GUI :) you are on CLI if u can use this   anyways

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
    return len(word_count[0])

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
    # Get all unique words from both texts
    all_words = []
    common_words = 0
    
    for word in word_count1[0]:
        if word not in all_words:
            all_words.append(word)
    
    for word in word_count2[0]:
        if word in word_count1[0]:
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

class TextAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Analysis and Plagiarism Detection")
        self.root.geometry("1000x700")
        
        # Create the main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_analyze_tab()
        self.create_compare_tab()
        self.create_search_tab()
        self.create_replace_tab()
        
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
        """Create the Analyze tab for single file analysis."""
        analyze_tab = ttk.Frame(self.notebook)
        self.notebook.add(analyze_tab, text="Analyze File")
        
        # File selection
        file_frame = ttk.Frame(analyze_tab)
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.file_entry1 = ttk.Entry(file_frame, width=50)
        self.file_entry1.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file1)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        analyze_btn = ttk.Button(file_frame, text="Analyze", command=self.analyze_file)
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.Frame(analyze_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - stats and lists
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        stats_frame = ttk.LabelFrame(left_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=5, width=40, wrap=tk.WORD)
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
        """Create the Compare tab for plagiarism detection."""
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
        self.compare_file_entry1.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn1 = ttk.Button(file1_frame, text="Browse", command=self.browse_compare_file1)
        browse_btn1.pack(side=tk.LEFT, padx=5)
        
        # File 2
        file2_frame = ttk.Frame(files_frame)
        file2_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file2_frame, text="File 2:").pack(side=tk.LEFT, padx=5)
        self.compare_file_entry2 = ttk.Entry(file2_frame, width=50)
        self.compare_file_entry2.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn2 = ttk.Button(file2_frame, text="Browse", command=self.browse_compare_file2)
        browse_btn2.pack(side=tk.LEFT, padx=5)
        
        compare_btn = ttk.Button(files_frame, text="Compare Files", command=self.compare_files)
        compare_btn.pack(pady=10)
        
        # Results section
        results_frame = ttk.Frame(compare_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Side by side comparison of file statistics
        stats_frame = ttk.Frame(results_frame)
        stats_frame.pack(fill=tk.X, pady=5)
        
        # File 1 stats
        file1_stats_frame = ttk.LabelFrame(stats_frame, text="File 1 Statistics")
        file1_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.file1_stats_text = tk.Text(file1_stats_frame, height=5, width=40, wrap=tk.WORD)
        self.file1_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # File 2 stats
        file2_stats_frame = ttk.LabelFrame(stats_frame, text="File 2 Statistics")
        file2_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.file2_stats_text = tk.Text(file2_stats_frame, height=5, width=40, wrap=tk.WORD)
        self.file2_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Comparison results
        comparison_frame = ttk.LabelFrame(results_frame, text="Comparison Results")
        comparison_frame.pack(fill=tk.X, pady=10)
        
        self.comparison_text = tk.Text(comparison_frame, height=6, wrap=tk.WORD)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Graph comparing word frequencies
        graph_frame = ttk.LabelFrame(results_frame, text="Word Frequency Comparison")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.compare_canvas = tk.Canvas(graph_frame)
        self.compare_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_search_tab(self):
        """Create the Search tab for word searching."""
        search_tab = ttk.Frame(self.notebook)
        self.notebook.add(search_tab, text="Search Word")
        
        # File selection
        file_frame = ttk.Frame(search_tab)
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.search_file_entry = ttk.Entry(file_frame, width=50)
        self.search_file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_search_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(search_tab)
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="Search for word:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_word)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(search_tab, text="Search Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.search_results = tk.Text(results_frame, wrap=tk.WORD)
        self.search_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_replace_tab(self):
        """Create the Replace tab for word replacement."""
        replace_tab = ttk.Frame(self.notebook)
        self.notebook.add(replace_tab, text="Replace Word")
        
        # File selection
        file_frame = ttk.Frame(replace_tab)
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.replace_file_entry = ttk.Entry(file_frame, width=50)
        self.replace_file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_replace_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Replace frame
        replace_frame = ttk.Frame(replace_tab)
        replace_frame.pack(fill=tk.X, pady=10)
        
        # Word to replace
        word_frame = ttk.Frame(replace_frame)
        word_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(word_frame, text="Word to replace:").pack(side=tk.LEFT, padx=5)
        self.word_entry = ttk.Entry(word_frame, width=30)
        self.word_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Replacement word
        replacement_frame = ttk.Frame(replace_frame)
        replacement_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(replacement_frame, text="Replacement word:").pack(side=tk.LEFT, padx=5)
        self.replacement_entry = ttk.Entry(replacement_frame, width=30)
        self.replacement_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        replace_btn = ttk.Button(replace_frame, text="Replace", command=self.replace_word)
        replace_btn.pack(pady=5)
        
        # Text display frames
        text_frame = ttk.Frame(replace_tab)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original text
        original_frame = ttk.LabelFrame(text_frame, text="Original Text (Cleaned)")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.original_text = tk.Text(original_frame, wrap=tk.WORD)
        self.original_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Modified text
        modified_frame = ttk.LabelFrame(text_frame, text="Modified Text")
        modified_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.modified_text = tk.Text(modified_frame, wrap=tk.WORD)
        self.modified_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Save button
        save_frame = ttk.Frame(replace_tab)
        save_frame.pack(fill=tk.X, pady=10)
        
        save_btn = ttk.Button(save_frame, text="Save Modified Text", command=self.save_modified_text)
        save_btn.pack()
        
    def browse_file1(self):
        """Browse for a file to analyze."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_entry1.delete(0, tk.END)
            self.file_entry1.insert(0, file_path)
            self.file_path1 = file_path
            
    def browse_compare_file1(self):
        """Browse for the first file to compare."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.compare_file_entry1.delete(0, tk.END)
            self.compare_file_entry1.insert(0, file_path)
            
    def browse_compare_file2(self):
        """Browse for the second file to compare."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.compare_file_entry2.delete(0, tk.END)
            self.compare_file_entry2.insert(0, file_path)
            
    def browse_search_file(self):
        """Browse for a file to search."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.search_file_entry.delete(0, tk.END)
            self.search_file_entry.insert(0, file_path)
            
    def browse_replace_file(self):
        """Browse for a file to perform word replacement."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.replace_file_entry.delete(0, tk.END)
            self.replace_file_entry.insert(0, file_path)
            
            # Load and display the original text
            content = read_file(file_path)
            if content:
                clean_content = clean_text(content)
                self.original_text.delete(1.0, tk.END)
                self.original_text.insert(tk.END, clean_content)
            
    def analyze_file(self):
        """Analyze a single file and display the results."""
        file_path = self.file_entry1.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return
            
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
        self.stats_text.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
        self.stats_text.insert(tk.END, f"Total words: {total_words}\n")
        self.stats_text.insert(tk.END, f"Unique words: {unique_words}\n")
        
        # Display word lists
        self.freq_list.delete(0, tk.END)
        freq_sorted = sort_by_frequency(word_count)
        for i, (word, count) in enumerate(freq_sorted[:20]):  # Show top 20
            self.freq_list.insert(tk.END, f"{i+1}. '{word}': {count} times")
            
        self.alpha_list.delete(0, tk.END)
        alpha_sorted = sort_alphabetically(word_count)
        for i, (word, count) in enumerate(alpha_sorted[:20]):  # Show first 20
            self.alpha_list.insert(tk.END, f"{i+1}. '{word}': {count} times")
            
        # Create and display the frequency graph
        self.create_frequency_graph(word_count, self.graph_canvas1)
        
        # Store for later use
        self.word_count1 = word_count
        self.clean_content1 = clean_content
        
    def create_frequency_graph(self, word_count, canvas_widget, max_words=10):
        """Create a bar graph of word frequencies."""
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
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{width}', ha='left', va='center')
        
        plt.tight_layout()
        
        # Embed the graph in the canvas
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def compare_files(self):
        """Compare two files for plagiarism detection."""
        file_path1 = self.compare_file_entry1.get()
        file_path2 = self.compare_file_entry2.get()
        
        if not file_path1 or not file_path2:
            messagebox.showerror("Error", "Please select both files.")
            return
            
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
        self.file1_stats_text.insert(tk.END, f"File: {os.path.basename(file_path1)}\n")
        self.file1_stats_text.insert(tk.END, f"Total words: {total_words1}\n")
        self.file1_stats_text.insert(tk.END, f"Unique words: {unique_words1}\n")
        
        # Display statistics for file 2
        self.file2_stats_text.delete(1.0, tk.END)
        self.file2_stats_text.insert(tk.END, f"File: {os.path.basename(file_path2)}\n")
        self.file2_stats_text.insert(tk.END, f"Total words: {total_words2}\n")
        self.file2_stats_text.insert(tk.END, f"Unique words: {unique_words2}\n")
        
        # Calculate and display similarity
        similarity = calculate_similarity(word_count1, word_count2)
        
        self.comparison_text.delete(1.0, tk.END)
        self.comparison_text.insert(tk.END, f"Similarity percentage: {similarity:.2f}%\n\n")
        
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
        self.create_comparison_graph(word_count1, word_count2, self.compare_canvas)
        
    def create_comparison_graph(self, word_count1, word_count2, canvas_widget, max_words=5):
        """Create a comparison graph of word frequencies between two files."""
        # Clear previous graph
        for widget in canvas_widget.winfo_children():
            widget.destroy()
            
        # Get top words from both files
        freq_sorted1 = sort_by_frequency(word_count1)
        freq_sorted2 = sort_by_frequency(word_count2)
        
        # Create sets of top words
        top_words1 = set([word for word, _ in freq_sorted1[:max_words]])
        top_words2 = set([word for word, _ in freq_sorted2[:max_words]])
        
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
        ax.bar([i - width/2 for i in x], counts1, width, label=f'File 1', color='skyblue')
        ax.bar([i + width/2 for i in x], counts2, width, label=f'File 2', color='lightgreen')
        
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
        
    def search_word(self):
        """Search for a word in the selected file."""
        file_path = self.search_file_entry.get()
        target_word = self.search_entry.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return
            
        if not target_word:
            messagebox.showerror("Error", "Please enter a word to search for.")
            return
            
        content = read_file(file_path)
        if content is None:
            messagebox.showerror("Error", f"Could not read file: {file_path}")
            return
            
        clean_content = clean_text(content)
        positions = search_word(clean_content, target_word)
        
        self.search_results.delete(1.0, tk.END)
        
        if positions:
            self.search_results.insert(tk.END, f"The word '{target_word}' appears {len(positions)} times at positions: {positions}\n\n")
            
            # Show each occurrence in context
            words = clean_content.split()
            for pos in positions:
                # Get a window of words around the occurrence
                start = max(0, pos - 3)
                end = min(len(words), pos + 4)
                context = " ".join(words[start:end])
                
                if pos > 3:
                    context = "... " + context
                if pos + 4 < len(words):
                    context = context + " ..."
                    
                self.search_results.insert(tk.END, f"Position {pos}: {context}\n")
        else:
            self.search_results.insert(tk.END, f"The word '{target_word}' was not found in the file.")
            
    def replace_word(self):
        """Replace occurrences of a word in the selected file."""
        file_path = self.replace_file_entry.get()
        target_word = self.word_entry.get()
        replacement_word = self.replacement_entry.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return
            
        if not target_word:
            messagebox.showerror("Error", "Please enter a word to replace.")
            return
            
        content = read_file(file_path)
        if content is None:
            messagebox.showerror("Error", f"Could not read file: {file_path}")
            return
            
        clean_content = clean_text(content)
        modified_content = helpers.replace_word(clean_content, target_word, replacement_word)
        
        # Display modified content
        self.modified_text.delete(1.0, tk.END)
        self.modified_text.insert(tk.END, modified_content)
        
    def save_modified_text(self):
        """Save the modified text to a new file."""
        if not self.modified_text.get(1.0, tk.END).strip():
            messagebox.showerror("Error", "No modified text to save.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.modified_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Modified text saved to '{file_path}'")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

def display_results(file_path, word_count, total_words, unique_words, show_nums=10, warp=os.get_terminal_size().columns):
    """Display analysis results for a single file."""
    if show_nums > len(word_count[0]):
        show_nums = len(word_count[0])
    hyphen_warp = warp if warp<len(str(show_nums))+30 else len(str(show_nums))+30
    print(f"\
\n\
{'='*warp}\n\
Analysis of '{file_path}':\n\
{'='*warp}\n\
Total words: {total_words}\n\
Unique words: {unique_words}\n\
\n\
\n\
Top {show_nums} Most Frequent Words:\n\
{'-'*hyphen_warp}")
    txt = ""
    frequency_sorted = sort_by_frequency(word_count)
    for i, (word, count) in enumerate(frequency_sorted[:show_nums]):
        txt += f"{i+1}. '{word}': {count} times\n"
    print(txt)

    txt = f"\nFirst {show_nums} Words (Alphabetically):\n{'-'*hyphen_warp}\n"
    alpha_sorted = sort_alphabetically(word_count)
    for i, (word, count) in enumerate(alpha_sorted[:show_nums]):
        txt += f"{i+1}. '{word}': {count} times\n"
    print(txt)

def compare_files(file_path1, file_path2):
    """Compare two text files and calculate their similarity percentage."""
    columns = os.get_terminal_size().columns
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
    display_results(file_path1, word_count1, total_words1, unique_words1, 5)
    display_results(file_path2, word_count2, total_words2, unique_words2, 5)

    # Calculate and display similarity percentage
    similarity = calculate_similarity(word_count1, word_count2)

    print(f"\n{'='*columns}\nComparison between '{file_path1}' and '{file_path2}':\n{'='*columns}\nSimilarity percentage: {similarity:.2f}%")

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


def mainGUI():
    """Main function to run the Word Analysis and Plagiarism Detection System GUI."""
    root = tk.Tk()
    app = TextAnalysisApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy() if messagebox.askokcancel("Quit", "Do you want to quit?") else None)
    root.mainloop()


def mainCLI():
    columns = os.get_terminal_size().columns
    """Main function to run the Word Analysis and Plagiarism Detection System."""
    print("Word Analysis and Plagiarism Detection System\n"+"-"*(columns if columns<45 else 45))

    while True:
        print("\
\nMenu:\n\
1. Analyze a single file\n\
2. Compare two files for plagiarism\n\
3. Search for a word in a file\n\
4. Replace a word in a file\n\
5. Exit\n")

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
                modified_content = helpers.replace_word(clean_content, target_word, replacement_word)

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
    parser = argparse.ArgumentParser(description="Word Analysis and Plagiarism Detection System")
    parser.add_argument("run_type", help='enter "GUI" or "CLI", determine whether a CLI or GUI version should run. default is GUI', nargs="?", default="GUI")
    args = parser.parse_args()
    if args.run_type == "GUI":
        mainGUI()
    elif args.run_type == "CLI":
        mainCLI()
    else:
        parser.error(f'Please enter either "GUI" or "CLI" for run type, not {repr(args.run_type)}')
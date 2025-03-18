import os  # Import module for terminal size detection and file operations
import helpers  # Import custom helper functions that avoid using built-in functions
import tkinter as tk  # Import tkinter for GUI implementation
from tkinter import ttk, filedialog, messagebox  # Import specific tkinter components
import matplotlib.pyplot as plt  # Import matplotlib for data visualization
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # For embedding matplotlib in tkinter
import argparse  # For command-line argument parsing


class config:
    """
    Configuration management class for WAPDS.
    
    This class handles loading, storing, and saving application settings.
    It maintains default values and provides methods to reset settings.
    
    Attributes:
        CLI_DEFAULTS (list): Default values for CLI settings
        GUI_DEFAULTS (list): Default values for GUI settings
        single_file_display_line (int): Number of words to display in single file analysis (CLI)
        compare_file_display_line (int): Number of words to display in file comparison (CLI)
        window_size (str): Size of the GUI window in format "widthxheight"
        graph_max_words (int): Maximum number of words to display in graphs
        graph_figsize (tuple): Size of matplotlib figures (width, height)
        analyze_max_words (int): Maximum number of words to display in analysis lists
        graph_bar_color_single (str): Color for bars in single file analysis
        graph_bar_color_compare1 (str): Color for bars of first file in comparison
        graph_bar_color_compare2 (str): Color for bars of second file in comparison
        graph_title_fontsize (int): Font size for graph titles
        graph_label_fontsize (int): Font size for graph labels
    """
    # Default values
    CLI_DEFAULTS = [10, 5]  # [single_file_display_line, compare_file_display_line]
    GUI_DEFAULTS = ["1000x700", 10, (5, 4), 5, 'skyblue', 'skyblue', 'lightgreen', 12, 10]
    # [window_size, graph_max_words, graph_figsize, analyze_max_words, 
    #  graph_bar_color_single, graph_bar_color_compare1, graph_bar_color_compare2,
    #  graph_title_fontsize, graph_label_fontsize]

    try:
        # Attempt to load configuration from file
        with open("WAPDS.config", "r") as f:
            config_data = f.readline().split(";")
            # CLI settings
            single_file_display_line = int(config_data[0])
            compare_file_display_line = int(config_data[1])
            # GUI settings
            window_size = str(config_data[2])
            graph_max_words = int(config_data[3])
            graph_figsize = (float(config_data[4]), float(config_data[5]))
            analyze_max_words = int(config_data[6])
            graph_bar_color_single = str(config_data[7])
            graph_bar_color_compare1 = str(config_data[8])
            graph_bar_color_compare2 = str(config_data[9])
            graph_title_fontsize = int(config_data[10])
            graph_label_fontsize = int(config_data[11])

    except:
        # Use defaults if file doesn't exist or is corrupted
        single_file_display_line = CLI_DEFAULTS[0]
        compare_file_display_line = CLI_DEFAULTS[1]
        window_size = GUI_DEFAULTS[0]
        graph_max_words = GUI_DEFAULTS[1]
        graph_figsize = GUI_DEFAULTS[2]
        analyze_max_words = GUI_DEFAULTS[3]
        graph_bar_color_single = GUI_DEFAULTS[4]
        graph_bar_color_compare1 = GUI_DEFAULTS[5]
        graph_bar_color_compare2 = GUI_DEFAULTS[6]
        graph_title_fontsize = GUI_DEFAULTS[7]
        graph_label_fontsize = GUI_DEFAULTS[8]

    # Write/update config file with current settings
    with open("WAPDS.config", "w") as f:
        f.write(f"{single_file_display_line};{compare_file_display_line};{window_size};{graph_max_words};{graph_figsize[0]};{graph_figsize[1]};{analyze_max_words};{graph_bar_color_single};{graph_bar_color_compare1};{graph_bar_color_compare2};{graph_title_fontsize};{graph_label_fontsize}")

    @classmethod
    def reset_to_defaults(cls):
        """
        Reset all settings to their default values.
        
        This method restores all configuration parameters to the predefined
        default values but does not save them to the configuration file.
        """
        # CLI defaults
        cls.single_file_display_line = cls.CLI_DEFAULTS[0]
        cls.compare_file_display_line = cls.CLI_DEFAULTS[1]
        # GUI defaults
        cls.window_size = cls.GUI_DEFAULTS[0]
        cls.graph_max_words = cls.GUI_DEFAULTS[1]
        cls.graph_figsize = cls.GUI_DEFAULTS[2]
        cls.analyze_max_words = cls.GUI_DEFAULTS[3]
        cls.graph_bar_color_single = cls.GUI_DEFAULTS[4]
        cls.graph_bar_color_compare1 = cls.GUI_DEFAULTS[5]
        cls.graph_bar_color_compare2 = cls.GUI_DEFAULTS[6]
        cls.graph_title_fontsize = cls.GUI_DEFAULTS[7]
        cls.graph_label_fontsize = cls.GUI_DEFAULTS[8]
    
    @classmethod  
    def save(cls):
        """
        Save current configuration settings to the config file.
        
        This method writes all current configuration parameters to the
        WAPDS.config file in a semicolon-delimited format.
        """
        with open("WAPDS.config", "w") as f:
            f.write(f"{cls.single_file_display_line};{cls.compare_file_display_line};" + 
                   f"{cls.window_size};{cls.graph_max_words};" +
                   f"{cls.graph_figsize[0]};{cls.graph_figsize[1]};" +
                   f"{cls.analyze_max_words};{cls.graph_bar_color_single};" +
                   f"{cls.graph_bar_color_compare1};{cls.graph_bar_color_compare2};" +
                   f"{cls.graph_title_fontsize};{cls.graph_label_fontsize}")


def read_file(file_path):
    """
    Read a text file and return its content as a string.
    
    Args:
        file_path (str): Path to the file to be read
        
    Returns:
        str or None: The content of the file as a string, or None if an error occurred
    
    This function handles file reading with error checking for file not found
    and other exceptions. It also warns if the file is empty.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        if not content.strip():
            print(f"\x1b[33mWarning: File '{file_path}' is empty.\x1b[m")
        return content
    except FileNotFoundError:
        print(f"\x1b[31mError: File '{file_path}' not found.\x1b[m")
        return None
    except Exception as e:
        print(f"\x1b[31mError reading file '{file_path}': {str(e)}\x1b[m")
        return None


def clean_text(text):
    """
    Remove punctuation and convert text to lowercase.
    
    Args:
        text (str or None): Text to be cleaned
        
    Returns:
        str: Cleaned text with punctuation removed, converted to lowercase
             and with no extra spaces
    
    This function normalizes text by:
    1. Converting to lowercase
    2. Replacing all non-alphanumeric characters with spaces
    3. Removing extra spaces
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
    
    This function splits the text into words and counts how many times
    each word appears, using custom helper functions instead of built-ins.
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


def sort_alphabetically(word_count):
    """
    Sort words alphabetically using quick_sort from helpers.
    
    Args:
        word_count (tuple): A tuple of (words, frequencies) as returned by count_words()
        
    Returns:
        list: List of (word, frequency) tuples sorted alphabetically
    
    This function sorts the words in alphabetical order and returns a list of
    (word, frequency) pairs maintaining the original frequency information.
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
    
    This function sorts words by their frequency in descending order and returns
    a list of (word, frequency) pairs.
    """
    # Create a list of (word, count) tuples
    word_items = []
    for idx in range(len(word_count[0])):
        word_items.append((word_count[0][idx], word_count[1][idx]))

    # Create a list that can be sorted using the quick_sort function
    # Using indices to maintain the original items
    items_to_sort = []
    for i, item in enumerate(word_items):
        items_to_sort.append(((item[1], item[0]), i))

    # Sort the indices
    sorted_indices = helpers.quick_sort(items_to_sort, ascending=False)

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
    
    This function calculates similarity by finding the ratio of common words
    to the total number of unique words across both texts.
    """
    # Get all unique words from both texts
    all_words = []
    common_words = 0

    # Add all words from first text to all_words list
    for word in word_count1[0]:
        if word not in all_words:
            if word in word_count1[1]:
                common_words += 1
            all_words.append(word)

    # Count common words and add unique words from second text
    for word in word_count2[0]:
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
    - Configuring application settings
    
    Attributes:
        root: Tkinter root window
        notebook: Main tabbed interface
        file_path1: Path to the first file
        file_path2: Path to the second file
        word_count1: Word count data for the first file
        word_count2: Word count data for the second file
        clean_content1: Cleaned text content of the first file
        clean_content2: Cleaned text content of the second file
    """

    def __init__(self, root, size):
        """
        Initialize the application with the tkinter root window.
        
        Args:
            root: Tkinter root window
            size (str): Window size in format "{width}x{height}"
        
        This constructor sets up the main window, creates the tabbed interface,
        and initializes all UI components and variables.
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
        self.create_config_tab()

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
        
        The tab is organized into sections for file selection, statistics,
        word lists, and visualization.
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
        
        The tab is organized into sections for file selection, statistics,
        comparison results, and visualization.
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

        # Left side - stats and lists
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        lists_frame = ttk.Frame(left_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # File 1 stats
        file1_stats_frame = ttk.LabelFrame(lists_frame,
                                           text="File 1 Statistics")
        file1_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.file1_stats_text = tk.Text(file1_stats_frame,
                                        height=5,
                                        width=40,
                                        wrap=tk.WORD)
        self.file1_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # File 2 stats
        file2_stats_frame = ttk.LabelFrame(lists_frame,
                                           text="File 2 Statistics")
        file2_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.file2_stats_text = tk.Text(file2_stats_frame,
                                        height=5,
                                        width=40,
                                        wrap=tk.WORD)
        self.file2_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        

        # Comparison results
        comparison_frame = ttk.LabelFrame(left_frame,
                                          text="Comparison Results")
        comparison_frame.pack(fill=tk.X, pady=10)

        self.comparison_text = tk.Text(comparison_frame,
                                       height=6,
                                       wrap=tk.WORD)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right side - graph
        right_frame = ttk.Frame(results_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Graph comparing word frequencies
        graph_frame = ttk.LabelFrame(right_frame, text="Word Frequency Comparison")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.compare_canvas = tk.Canvas(graph_frame)
        self.compare_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_config_tab(self):
        """
        Create the Configuration tab for changing application settings.

        This tab allows users to modify:
        - CLI settings (display lines for analysis and comparison)
        - GUI settings (window size, graph appearance, font sizes)
        
        The tab includes input fields for all configurable parameters and
        buttons to save, cancel, or reset settings.
        """
        config_tab = ttk.Frame(self.notebook)
        self.notebook.add(config_tab, text="Configuration")
        
        CLI_settings_frame = ttk.LabelFrame(config_tab, text="CLI Settings")
        CLI_settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        GUI_settings_frame = ttk.LabelFrame(config_tab, text="GUI Settings")
        GUI_settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Single file display setting
        single_file_frame = ttk.Frame(CLI_settings_frame)
        single_file_frame.pack(fill=tk.X, pady=10)

        ttk.Label(single_file_frame, 
                  text="Number of words to display in Analyze File tab:").pack(side=tk.LEFT, padx=5)

        self.single_file_display_var = tk.StringVar(value=str(config.single_file_display_line))
        self.single_file_display_entry = ttk.Entry(single_file_frame, 
                                                   width=10, 
                                                   textvariable=self.single_file_display_var)
        self.single_file_display_entry.pack(side=tk.LEFT, padx=5)

        # Compare files display setting
        compare_file_frame = ttk.Frame(CLI_settings_frame)
        compare_file_frame.pack(fill=tk.X, pady=10)

        ttk.Label(compare_file_frame, 
                  text="Number of words to display in Compare Files tab:").pack(side=tk.LEFT, padx=5)

        self.compare_file_display_var = tk.StringVar(value=str(config.compare_file_display_line))
        self.compare_file_display_entry = ttk.Entry(compare_file_frame, 
                                                    width=10, 
                                                    textvariable=self.compare_file_display_var)
        self.compare_file_display_entry.pack(side=tk.LEFT, padx=5)

        # Graph settings frame
        graph_settings_frame = ttk.LabelFrame(GUI_settings_frame, text="Graph Settings")
        graph_settings_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Words display settings
        words_frame = ttk.Frame(graph_settings_frame)
        words_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(words_frame, text="Max words in graph:").pack(side=tk.LEFT, padx=5)
        self.graph_max_words_var = tk.StringVar(value=str(config.graph_max_words))
        self.graph_max_words_entry = ttk.Entry(words_frame, width=10, textvariable=self.graph_max_words_var)
        self.graph_max_words_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(words_frame, text="Max words to show in text:").pack(side=tk.LEFT, padx=5)
        self.analyze_max_words_var = tk.StringVar(value=str(config.analyze_max_words))
        self.analyze_max_words_entry = ttk.Entry(words_frame, width=10, textvariable=self.analyze_max_words_var)
        self.analyze_max_words_entry.pack(side=tk.LEFT, padx=5)

        # Graph size settings
        size_frame = ttk.Frame(graph_settings_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="Graph size (width, height):").pack(side=tk.LEFT, padx=5)
        self.graph_width_var = tk.StringVar(value=str(config.graph_figsize[0]))
        self.graph_width_entry = ttk.Entry(size_frame, width=5, textvariable=self.graph_width_var)
        self.graph_width_entry.pack(side=tk.LEFT, padx=2)
        
        self.graph_height_var = tk.StringVar(value=str(config.graph_figsize[1]))
        self.graph_height_entry = ttk.Entry(size_frame, width=5, textvariable=self.graph_height_var)
        self.graph_height_entry.pack(side=tk.LEFT, padx=2)

        # Font settings
        font_frame = ttk.Frame(graph_settings_frame)
        font_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(font_frame, text="Title font size:").pack(side=tk.LEFT, padx=5)
        self.title_font_var = tk.StringVar(value=str(config.graph_title_fontsize))
        self.title_font_entry = ttk.Entry(font_frame, width=5, textvariable=self.title_font_var)
        self.title_font_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(font_frame, text="Label font size:").pack(side=tk.LEFT, padx=5)
        self.label_font_var = tk.StringVar(value=str(config.graph_label_fontsize))
        self.label_font_entry = ttk.Entry(font_frame, width=5, textvariable=self.label_font_var)
        self.label_font_entry.pack(side=tk.LEFT, padx=5)

        # Color settings
        colors_frame = ttk.Frame(graph_settings_frame)
        colors_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(colors_frame, text="Bar colors:").pack(side=tk.LEFT, padx=5)
        self.bar_color_single_var = tk.StringVar(value=str(config.graph_bar_color_single))
        ttk.Entry(colors_frame, width=10, textvariable=self.bar_color_single_var).pack(side=tk.LEFT, padx=2)
        
        self.bar_color_compare1_var = tk.StringVar(value=str(config.graph_bar_color_compare1))
        ttk.Entry(colors_frame, width=10, textvariable=self.bar_color_compare1_var).pack(side=tk.LEFT, padx=2)
        
        self.bar_color_compare2_var = tk.StringVar(value=str(config.graph_bar_color_compare2))
        ttk.Entry(colors_frame, width=10, textvariable=self.bar_color_compare2_var).pack(side=tk.LEFT, padx=2)

        # Buttons frame
        buttons_frame = ttk.Frame(config_tab)
        buttons_frame.pack(fill=tk.X, pady=20)

        save_btn = ttk.Button(buttons_frame, 
                              text="Save settings", 
                              command=self.save_config)
        save_btn.pack(side=tk.RIGHT, padx=5)

        cancel_btn = ttk.Button(buttons_frame, 
                                text="Cancel changes", 
                                command=self.reset_last_save_config)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        reset_btn = ttk.Button(buttons_frame, 
                                text="Reset values to default", 
                                command=self.reset_default_config)
        reset_btn.pack(side=tk.RIGHT, padx=5)

        # Add an info text
        info_frame = ttk.Frame(config_tab)
        info_frame.pack(fill=tk.X, pady=10)

        info_text = tk.Text(info_frame, height=5, wrap=tk.WORD)
        info_text.pack(fill=tk.X, padx=10)
        info_text.insert(tk.END, 
                        "These settings control how many words are displayed in the word lists and graphs. " 
                        "Changes will be saved to the configuration file and applied immediately once the save button is pressed.")
        info_text.config(state=tk.DISABLED) # make the text read-only


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
        total_words = len(clean_content.split(" "))
        unique_words = len(word_count[0])

        # Display statistics
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
        self.stats_text.insert(tk.END, f"Total words: {total_words}\n")
        self.stats_text.insert(tk.END, f"Unique words: {unique_words}\n")

        # Display word lists
        self.freq_list.delete(0, tk.END)
        freq_sorted = sort_by_frequency(word_count)[:config.analyze_max_words]
        for i, (word, count) in enumerate(freq_sorted):
            self.freq_list.insert(tk.END, f"{i+1}. '{word}': {count} times")

        self.alpha_list.delete(0, tk.END)
        alpha_sorted = sort_alphabetically(word_count)[:config.analyze_max_words]
        for i, (word, count) in enumerate(alpha_sorted):
            self.alpha_list.insert(tk.END, f"{i+1}. '{word}': {count} times")

        # Create and display the frequency graph
        self.create_frequency_graph(word_count, self.graph_canvas1)

        # Store for later use
        self.word_count1 = word_count
        self.clean_content1 = clean_content

    def create_frequency_graph(self, word_count, canvas_widget, max_words=config.graph_max_words):
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
        fig, ax = plt.subplots(figsize=config.graph_figsize)

        words = [word for word, _ in top_words]
        counts = [count for _, count in top_words]

        # Create horizontal bar chart
        bars = ax.barh(words, counts, color=config.graph_bar_color_single)

        # Add labels
        ax.set_xlabel('Frequency', fontsize=config.graph_label_fontsize)
        ax.set_title('Top Word Frequencies', fontsize=config.graph_title_fontsize)
        ax.tick_params(labelsize=config.graph_label_fontsize)

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

        total_words1 = len(clean_content1.split(" "))
        total_words2 = len(clean_content2.split(" "))

        unique_words1 = len(word_count1[0])
        unique_words2 = len(word_count2[0])

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
                                max_words=config.graph_max_words):
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
        fig, ax = plt.subplots(figsize=config.graph_figsize)

        x = range(len(combined_top_words))
        width = 0.35

        # Create bar chart
        ax.bar(
            [i - width / 2 for i in x],
            counts1,
            width,
            label='File 1',
            color=config.graph_bar_color_compare1,
        )
        ax.bar(
            [i + width / 2 for i in x],
            counts2,
            width,
            label='File 2',
            color=config.graph_bar_color_compare2,
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
        
    def save_config(self):
        """
        Save the configuration settings to the config file.
        """
        try:
            # Get and validate values from entry fields
            single_file_display = int(self.single_file_display_var.get())
            compare_file_display = int(self.compare_file_display_var.get())
            graph_max_words = int(self.graph_max_words_var.get())
            analyze_max_words = int(self.analyze_max_words_var.get())
            graph_width = float(self.graph_width_var.get())
            graph_height = float(self.graph_height_var.get())
            title_fontsize = float(self.title_font_var.get())
            label_fontsize = float(self.label_font_var.get())

            if helpers.any(x <= 0 for x in [
                single_file_display, compare_file_display, 
                graph_max_words, analyze_max_words,
                graph_width, graph_height,
                title_fontsize, label_fontsize]):
                messagebox.showerror("Error", "All numeric settings must be positive numbers.")
                return

            # Update config
            config.single_file_display_line = single_file_display
            config.compare_file_display_line = compare_file_display
            config.graph_max_words = graph_max_words
            config.analyze_max_words = analyze_max_words
            config.graph_figsize = (graph_width, graph_height)
            config.graph_title_fontsize = title_fontsize
            config.graph_label_fontsize = label_fontsize
            config.graph_bar_color_single = self.bar_color_single_var.get()
            config.graph_bar_color_compare1 = self.bar_color_compare1_var.get()
            config.graph_bar_color_compare2 = self.bar_color_compare2_var.get()

            # Write to config file
            config.save()

            messagebox.showinfo("Configuration", "Settings saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for both settings.")

    def reset_last_save_config(self):
        """
        Reset the configuration fields to their current values.
        """
        self.single_file_display_var.set(str(config.single_file_display_line))
        self.compare_file_display_var.set(str(config.compare_file_display_line))
        self.graph_max_words_var.set(str(config.graph_max_words))
        self.analyze_max_words_var.set(str(config.analyze_max_words))
        self.graph_width_var.set(str(config.graph_figsize[0]))
        self.graph_height_var.set(str(config.graph_figsize[1]))
        self.title_font_var.set(str(config.graph_title_fontsize))
        self.label_font_var.set(str(config.graph_label_fontsize))
        self.bar_color_single_var.set(str(config.graph_bar_color_single))
        self.bar_color_compare1_var.set(str(config.graph_bar_color_compare1))
        self.bar_color_compare2_var.set(str(config.graph_bar_color_compare2))
        
    def reset_default_config(self):
        """
        Reset the configuration fields to their default values.
        """
        config.reset_to_defaults()
        self.reset_last_save_config()

        messagebox.showinfo("Configuration", "Settings reset to default values.")
        
        
def configure_test_input(prompt:str, type, was:str, error:str = ""):
    try:
        temp_unsaved = input(f"{prompt} (was {was}): ")
        if type == int:
            if temp_unsaved > 0:
                return int(temp_unsaved)
            else:
                raise ValueError
        elif type == float:
            if temp_unsaved > 0:
                return float(temp_unsaved)
            else:
                raise ValueError
        else:
            return temp_unsaved
    except ValueError:
        print("Invalid input. ", end="")
        if error:
            print(error)
        elif type == int:
            print("Please enter a positive integer.")
        elif type == float:
            print("Please enter a positive float.")
        else:
            print(error)
        
        
def configure():
    """
    Configure the settings for the program.
    """
    unsaved_single_file_display_line: int|None = None
    unsaved_compare_file_display_line: int|None = None
    unsaved_graph_max_words: int|None = None
    unsaved_graph_figsize_h: int|None = None
    unsaved_graph_figsize_w: int|None = None
    unsaved_analyze_max_words: int|None = None
    unsaved_graph_bar_color_single: int|None = None
    unsaved_graph_bar_color_compare1: int|None = None
    unsaved_graph_bar_color_compare2: int|None = None
    unsaved_graph_title_fontsize: int|None = None
    unsaved_graph_label_fontsize: int|None = None
    while True:
        print(
        [f"Change settings{'' if unsaved_single_file_display_line is None and unsaved_compare_file_display_line is None else ' (unsaved)'}:",
        [],
        [*"CLI settings:"],
        ["\x1b[1;4;97mA\x1b[m", *f"nalyse file: show first {config.single_file_display_line if unsaved_single_file_display_line is None else f'{unsaved_single_file_display_line} (was {config.single_file_display_line})'} sorted words appeared"],
        ["\x1b[1;4;97mC\x1b[m", *f"ompare files: show first {config.compare_file_display_line if unsaved_compare_file_display_line is None else f'{unsaved_compare_file_display_line} (was {config.compare_file_display_line})'} sorted words appeared"],
        [],
        [*"GUI settings:"],
        ["a", "\x1b[1;4;97mN\x1b[m", *f"alyse file: show first {config.analyze_max_words if unsaved_analyze_max_words is None else f'{unsaved_analyze_max_words} (was {config.analyze_max_words})'} sorted words appeared"],
        [*"Graph: ", "\x1b[1;4;97mM\x1b[m", *f"ax word: show first {config.graph_max_words if unsaved_graph_max_words is None else f'{unsaved_graph_max_words} (was {config.graph_max_words})'} sorted words appeared"],
        [*"Graph figure size: set the figure ", "\x1b[1;4;97mH\x1b[m", *f"eight to {config.graph_figsize[1] if unsaved_graph_figsize_h is None else f'{unsaved_graph_figsize_h} (was {config.graph_figsize[1]})'}"],
        [*"Graph figure size: set the figure ", "\x1b[1;4;97mW\x1b[m", *f"idth to {config.graph_figsize[0] if unsaved_graph_figsize_w is None else f'{unsaved_graph_figsize_w} (was {config.graph_figsize[0]})'}"],
        [*"Graph bar: set color of ", "\x1b[1;4;97mS\x1b[m", *f"ingle bar (analyse file) to {config.graph_bar_color_single if unsaved_graph_bar_color_single is None else f'{unsaved_graph_bar_color_single} (was {config.graph_bar_color_single})'}"],
        [*"Graph bar: set color of File", "\x1b[1;4;97m1\x1b[m", *f"'s bar (compare file) to {config.graph_bar_color_compare1 if unsaved_graph_bar_color_compare1 is None else f'{unsaved_graph_bar_color_compare1} (was {config.graph_bar_color_compare1})'}"],
        [*"Graph bar: set color of File", "\x1b[1;4;97m2\x1b[m", *f"'s bar (compare file) to {config.graph_bar_color_compare2 if unsaved_graph_bar_color_compare2 is None else f'{unsaved_graph_bar_color_compare2} (was {config.graph_bar_color_compare2})'}"],
        [*"Graph ", "\x1b[1;4;97mT\x1b[m", *f"itle: set font size to {config.graph_title_fontsize if unsaved_graph_title_fontsize is None else f'{unsaved_graph_title_fontsize} (was {config.graph_title_fontsize})'}"],
        [*"Graph ", "\x1b[1;4;97mL\x1b[m", *f"itle: set font size to {config.graph_label_fontsize if unsaved_graph_label_fontsize is None else f'{unsaved_graph_label_fontsize} (was {config.graph_label_fontsize})'}"],
        ["\x1b[1;4mS\x1b[m", *"ave and exit"],
        ["\x1b[1;4;97mE\x1b[m", *"xit without saving"]], _override=True) # because multi-line print containing ANSI is not supported, input text is sliced manually to make it work
        config_option = input("Enter option: ", single_letter=True).upper().strip()

        if config_option == "A":
            unsaved_single_file_display_line = configure_test_input("Enter number of sorted words to display in Analyze File mode", int, str(config.single_file_display_line))
        elif config_option == "C":
            unsaved_compare_file_display_line = configure_test_input("Enter number of sorted words to display in Compare Files mode", int, str(config.compare_file_display_line))
        elif config_option == "N":
            unsaved_analyze_max_words = configure_test_input("Enter number of sorted words to display in Analyze File mode", int, str(config.analyze_max_words))
        elif config_option == "M":
            unsaved_graph_max_words = configure_test_input("Enter number of sorted words to display in the result figure", int, str(config.graph_max_words))
        elif config_option == "H":
            unsaved_graph_figsize_h = configure_test_input("Enter height of the figure", float, str(config.graph_figsize[1]))
        elif config_option == "W":
            unsaved_graph_figsize_w = configure_test_input("Enter width of the figure", float, str(config.graph_figsize[0]))
        elif config_option == "S":
            unsaved_graph_bar_color_single = configure_test_input("Enter color of the bar in Analyze File mode", str, str(config.graph_bar_color_single))
        elif config_option == "1":
            unsaved_graph_bar_color_compare1 = configure_test_input("Enter color of File1's bar in Compare Files mode", str, str(config.graph_bar_color_compare1))
        elif config_option == "2":
            unsaved_graph_bar_color_compare2 = configure_test_input("Enter color of File2's bar in Compare Files mode", str, str(config.graph_bar_color_compare2))
        elif config_option == "T":
            unsaved_graph_title_fontsize = configure_test_input("Enter font size of the figure's title", float, str(config.graph_title_fontsize))
        elif config_option == "L":
            unsaved_graph_label_fontsize = configure_test_input("Enter font size of the figure's labels", float, str(config.graph_label_fontsize))
        elif config_option in "ES":
            break
        else:
            print(f"Invalid option {repr(config_option)}. Please try again.")
    if config_option == "S":
        if unsaved_single_file_display_line is not None:
            config.single_file_display_line = unsaved_single_file_display_line
        if unsaved_compare_file_display_line is not None:
            config.compare_file_display_line = unsaved_compare_file_display_line
        if unsaved_analyze_max_words is not None:
            config.analyze_max_words = unsaved_analyze_max_words
        if unsaved_graph_max_words is not None:
            config.graph_max_words = unsaved_graph_max_words
        if unsaved_graph_figsize_h is not None:
            config.graph_figsize[1] = unsaved_graph_figsize_h
        if unsaved_graph_figsize_w is not None:
            config.graph_figsize[0] = unsaved_graph_figsize_w
        if unsaved_graph_bar_color_single is not None:
            config.graph_bar_color_single = unsaved_graph_bar_color_single
        if unsaved_graph_bar_color_compare1 is not None:
            config.graph_bar_color_compare1 = unsaved_graph_bar_color_compare1
        if unsaved_graph_bar_color_compare2 is not None:
            config.graph_bar_color_compare2 = unsaved_graph_bar_color_compare2
        if unsaved_graph_title_fontsize is not None:
            config.graph_title_fontsize = unsaved_graph_title_fontsize
        if unsaved_graph_label_fontsize is not None:
            config.graph_label_fontsize = unsaved_graph_label_fontsize
        config.save()
    return


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
            "\x1b[31mError: Cannot compare files due to reading errors.\x1b[m"
        )
        return

    # Clean and analyze texts
    clean_content1 = clean_text(content1)
    clean_content2 = clean_text(content2)

    word_count1 = count_words(clean_content1)
    word_count2 = count_words(clean_content2)

    total_words1 = len(clean_content1.split(" "))
    total_words2 = len(clean_content2.split(" "))

    unique_words1 = len(word_count1[0])
    unique_words2 = len(word_count2[0])

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
            "\x1b[31mPlagiarism Level: HIGH - These texts are very similar\x1b[m"
        )
    elif similarity > 50:
        print(
            "\x1b[33mPlagiarism Level: MEDIUM - These texts have significant overlap\x1b[m"
        )
    elif similarity > 20:
        print(
            "\x1b[92mPlagiarism Level: LOW - These texts have some common elements\x1b[m"
        )
    else:
        print(
            "\x1b[32mPlagiarism Level: MINIMAL - These texts are mostly different\x1b[m"
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
    total_words = len(clean_content.split(" "))
    unique_words = len(word_count[0])

    # Display analysis results
    display_results(file_path, word_count, total_words, unique_words, config.single_file_display_line)


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
    app = WordAnalysisApp(root, config.window_size)  # app is unused because tkinter handles the UI events

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

        choice = input("\nEnter your choice (1-4): ", single_letter=True).strip()


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
            
            

if __name__ == "__main__":
    # Parse command line arguments to determine whether to run GUI or CLI
    some_text = "{width}x{height}" #still can't figure out how to put {} in f-strings :)
    parser = argparse.ArgumentParser(
        description="Word Analysis and Plagiarism Detection System (WAPDS)")
    parser.add_argument(
        "run_type",
        help=
        'enter "GUI" or "CLI", determine whether a CLI or GUI version should run. default is GUI',
        nargs="?",
        default="GUI")
    parser.add_argument(
        "GUI_window_size",
        help=
        f'enter in format of {some_text}, set the GUI window size and will be saved, defaults to last window size (currently {repr(config.window_size)})',
        nargs="?",
        default=config.window_size)
    args = parser.parse_args()

    # Start appropriate interface based on argument
    if args.run_type == "GUI":
        try:
            GUI_window_size_check = args.GUI_window_size.strip().split("x")
            GUI_window_size_check = [int(dimension) for dimension in GUI_window_size_check] #errors if not correct size
            if len(GUI_window_size_check) != 2:
                raise ValueError
            for n in GUI_window_size_check:
                if n <= 0:
                    raise ValueError
        except ValueError:
            parser.error(
            f'Please enter GUI window size in the format of {some_text}, not {repr(args.GUI_window_size)}'
        )
        config.window_size = args.GUI_window_size.strip()
        config.save()
        mainGUI()
    elif args.run_type == "CLI":
        from helpers import animated_print as print, animated_input as input  # Use animated versions of print/input (CLI only)
        mainCLI()
    else:
        parser.error(
            f'Please enter either "GUI" or "CLI" for run type, not {repr(args.run_type)}'
        )

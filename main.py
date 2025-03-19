import os  # Import module for terminal size detection and file operations
import helpers  # Import custom helper functions that avoid using built-in functions
import tkinter as tk  # Import tkinter for GUI implementation
from tkinter import ttk, filedialog, messagebox  # Import specific tkinter components
import matplotlib.pyplot as plt  # Import matplotlib for data visualization
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # For embedding matplotlib in tkinter
import argparse  # For command-line argument parsing


class config:
    """
    Configuration management class for WAPDS (Word Analysis and Plagiarism Detection System).

    This class handles loading, storing, and saving application settings.
    It maintains default values and provides methods to reset settings.

    Attributes:
        CLI_DEFAULTS (list): Default values for Command Line Interface (CLI) settings
        GUI_DEFAULTS (list): Default values for Graphical User Interface (GUI) settings
        single_file_display_line (int): Number of words to display in single file analysis (CLI)
        compare_file_display_line (int): Number of words to display in file comparison (CLI)
        window_size (str): Size of the GUI window in "widthxheight" format
        graph_max_words (int): Maximum number of words to display in graphs
        graph_figsize (tuple): Size of matplotlib figures (width, height)
        analyze_max_words (int): Maximum number of words to display in analysis lists
        graph_bar_color_single (str): Color for bars in single file analysis
        graph_bar_color_compare1 (str): Color for bars of first file in comparison
        graph_bar_color_compare2 (str): Color for bars of second file in comparison
        graph_title_fontsize (int): Font size for graph titles
        graph_label_fontsize (int): Font size for graph labels
    """

    # Default values for CLI and GUI settings
    CLI_DEFAULTS = [10, 5]  # [single_file_display_line, compare_file_display_line]
    GUI_DEFAULTS = ["1000x700", 10, (5, 4), 5, 'skyblue', 'skyblue', 'lightgreen', 12, 10]  # [window_size, graph_max_words, graph_figsize, analyze_max_words, graph_bar_color_single, graph_bar_color_compare1, graph_bar_color_compare2, graph_title_fontsize, graph_label_fontsize]

    try:
        # Attempt to load configuration from file
        with open("WAPDS.config", "r") as f:
            # Read settings from the configuration file, split by semicolon
            config_data = f.readline().split(";")
            # Parse settings, converting to appropriate types
            single_file_display_line = int(config_data[0])  # Line count for single file analysis
            compare_file_display_line = int(config_data[1])  # Line count for file comparison
            window_size = str(config_data[2])  # GUI window size
            graph_max_words = int(config_data[3])  # Max words to display in graphs
            graph_figsize = (float(config_data[4]), float(config_data[5]))  # Figure size for graphs
            analyze_max_words = int(config_data[6])  # Max words to show in analysis lists
            graph_bar_color_single = str(config_data[7])  # Bar color for single analysis
            graph_bar_color_compare1 = str(config_data[8])  # First file comparison bar color
            graph_bar_color_compare2 = str(config_data[9])  # Second file comparison bar color
            graph_title_fontsize = int(config_data[10])  # Font size for graph titles
            graph_label_fontsize = int(config_data[11])  # Font size for graph labels

    except:
        # Use default settings if the configuration file doesn't exist or is corrupted
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
        f.write(f"{single_file_display_line};{compare_file_display_line};{window_size};"
                 f"{graph_max_words};{graph_figsize[0]};{graph_figsize[1]};"
                 f"{analyze_max_words};{graph_bar_color_single};"
                 f"{graph_bar_color_compare1};{graph_bar_color_compare2};"
                 f"{graph_title_fontsize};{graph_label_fontsize}")

    @classmethod
    def reset_to_defaults(cls):
        """
        Reset all settings to their default values.

        This method restores all configuration parameters to the predefined default values
        but does not save them to the configuration file.
        """
        # Restore CLI default values
        cls.single_file_display_line = cls.CLI_DEFAULTS[0]
        cls.compare_file_display_line = cls.CLI_DEFAULTS[1]
        # Restore GUI default values
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

        This method writes all current configuration parameters to the WAPDS.config file
        in a semicolon-delimited format.
        """
        with open("WAPDS.config", "w") as f:
            f.write(f"{cls.single_file_display_line};{cls.compare_file_display_line};"
                     f"{cls.window_size};{cls.graph_max_words};"
                     f"{cls.graph_figsize[0]};{cls.graph_figsize[1]};"
                     f"{cls.analyze_max_words};{cls.graph_bar_color_single};"
                     f"{cls.graph_bar_color_compare1};{cls.graph_bar_color_compare2};"
                     f"{cls.graph_title_fontsize};{cls.graph_label_fontsize}")


def read_file(file_path):
    """
    Read a text file and return its content as a string.

    Args:
        file_path (str): Path to the file to be read

    Returns:
        str or None: The content of the file as a string, or None if an error occurred.

    This function handles file reading with error checking for file not found
    and other exceptions. It also warns if the file is empty.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Read the entire file content
        if not content.strip():  # Check if the file is empty
            print(f"\x1b[33mWarning: File '{file_path}' is empty.\x1b[m")
        return content  # Return file content

    except FileNotFoundError:  # File not found error handling
        print(f"\x1b[31mError: File '{file_path}' not found.\x1b[m")
        return None  # Return None for error

    except Exception as e:  # Handle other exceptions
        print(f"\x1b[31mError reading file '{file_path}': {str(e)}\x1b[m")
        return None  # Return None for error


def clean_text(text):
    """
    Remove punctuation and convert text to lowercase.

    Args:
        text (str or None): Text to be cleaned

    Returns:
        str: Cleaned text with punctuation removed, converted to lowercase
             and with no extra spaces.

    This function normalizes text by:
    1. Converting to lowercase
    2. Replacing all non-alphanumeric characters with spaces
    3. Removing extra spaces
    """
    if text is None:  # If input text is None, return empty string
        return ""

    # Replace any character that isn't a letter, digit, or space with a space
    cleaned_text = "".join((char if 'a' <= char <= 'z' or '0' <= char <= '9'
                            or char == ' ' else ' ') for char in text.lower())

    # Remove extra spaces (replace double spaces with single until no doubles remain)
    while '  ' in cleaned_text:
        cleaned_text = cleaned_text.replace('  ', ' ')

    return cleaned_text.strip()  # Return cleaned and stripped text


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
    if not text:  # If text is empty, return empty structure
        return ([], [])

    # Initialize result structure as a tuple of two lists
    word_count = ([], [])  # ([words], [frequencies])
    words = text.split(" ")  # Split text into individual words

    # Count frequency of each word using a for loop
    for n in range(len(words)):
        word = words[n]
        if word in word_count[0]:  # Check if word already exists in our list
            # If word already exists, increment its count
            word_index = helpers.linear_search(word_count[0], word)
            word_count[1][word_index] += 1
        else:
            # Otherwise, add it to our list with a count of 1
            word_count[0].append(word)
            word_count[1].append(1)

    return word_count  # Return the word counts


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
    words = word_count[0]  # Extract words from word_count
    # Sort words alphabetically using a helper function
    sorted_words = helpers.quick_sort(words)

    # Create list of (word, frequency) pairs
    result = []
    for n in range(len(sorted_words)):
        word = sorted_words[n]
        # Find the index of the word in the original list to get its frequency
        result.append(
            (word, word_count[1][helpers.linear_search(word_count[0], word)]))
    return result  # Return sorted word frequency pairs


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

    return result  # Return sorted pairs by frequency


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
    all_words = []  # List of all words
    common_words = 0  # Count of common words

    # Add all words from first text to all_words list
    for word in word_count1[0]:
        if word not in all_words:
            if word in word_count2[0]: #if it is a common word between 2 text
                common_words += 1  # Increment count of common matched words
            all_words.append(word)  # Append word to all_words

    # Count common words and add unique words from the second text
    for word in word_count2[0]:
        if word not in all_words:
            all_words.append(word)

    # Calculate similarity percentage
    return (common_words / len(all_words)) * 100  # Return similarity rate


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
        self.root = root  # Set root window
        self.root.title("Word Analysis and Plagiarism Detection")  # Set window title
        self.root.geometry(size)  # Set window size defined by the user

        # Create the main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs for various functionalities
        self.create_analyze_tab()  # Tab for analyzing single file
        self.create_compare_tab()  # Tab for comparing two files
        self.create_config_tab()  # Tab for configuring settings

        # Variables to store file paths and analysis results
        self.file_path1 = ""
        self.file_path2 = ""
        self.word_count1 = None
        self.word_count2 = None
        self.clean_content1 = ""
        self.clean_content2 = ""

        # Style configuration for GUI components
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
        analyze_tab = ttk.Frame(self.notebook)  # Create tab frame
        self.notebook.add(analyze_tab, text="Analyze File")  # Add tab to notebook

        # File selection frame
        file_frame = ttk.Frame(analyze_tab)
        file_frame.pack(fill=tk.X, pady=10)

        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)  # Label for file selection
        self.file_entry1 = ttk.Entry(file_frame, width=50)  # Entry field for selected file path
        self.file_entry1.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Button to browse for file
        browse_btn = ttk.Button(file_frame,
                                text="Browse",
                                command=self.browse_file1)
        browse_btn.pack(side=tk.LEFT, padx=5)

        # Button to trigger file analysis
        analyze_btn = ttk.Button(file_frame,
                                 text="Analyze",
                                 command=self.analyze_file)
        analyze_btn.pack(side=tk.LEFT, padx=5)

        # Results section for displaying statistics and lists
        results_frame = ttk.Frame(analyze_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Left side - stats and lists display
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        stats_frame = ttk.LabelFrame(left_frame, text="Statistics")  # Frame for statistics
        stats_frame.pack(fill=tk.X, pady=5)

        # Text area for displaying statistics
        self.stats_text = tk.Text(stats_frame,
                                  height=5,
                                  width=40,
                                  wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        lists_frame = ttk.Frame(left_frame)  # Frame for word lists
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Frequency list frame
        freq_frame = ttk.LabelFrame(lists_frame, text="Most Frequent Words")
        freq_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Listbox to display frequent words
        self.freq_list = tk.Listbox(freq_frame, height=15)
        self.freq_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Alphabetical list frame
        alpha_frame = ttk.LabelFrame(lists_frame, text="Alphabetical Words")
        alpha_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Listbox to display words in alphabetical order
        self.alpha_list = tk.Listbox(alpha_frame, height=15)
        self.alpha_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right side - graph display
        right_frame = ttk.Frame(results_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        graph_frame = ttk.LabelFrame(right_frame, text="Word Frequency Graph")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Canvas to draw the frequency graph
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
        compare_tab = ttk.Frame(self.notebook)  # Create compare tab frame
        self.notebook.add(compare_tab, text="Compare Files")  # Add to notebook

        # File selection frame
        files_frame = ttk.Frame(compare_tab)
        files_frame.pack(fill=tk.X, pady=10)

        # File 1 selection
        file1_frame = ttk.Frame(files_frame)
        file1_frame.pack(fill=tk.X, pady=5)

        ttk.Label(file1_frame, text="File 1:").pack(side=tk.LEFT, padx=5)  # Label for File 1 selection
        self.compare_file_entry1 = ttk.Entry(file1_frame, width=50)  # Entry for File 1 path
        self.compare_file_entry1.pack(side=tk.LEFT,
                                      padx=5,
                                      fill=tk.X,
                                      expand=True)

        # Button to browse for File 1
        browse_btn1 = ttk.Button(file1_frame,
                                 text="Browse",
                                 command=self.browse_compare_file1)
        browse_btn1.pack(side=tk.LEFT, padx=5)

        # File 2 selection
        file2_frame = ttk.Frame(files_frame)
        file2_frame.pack(fill=tk.X, pady=5)

        ttk.Label(file2_frame, text="File 2:").pack(side=tk.LEFT, padx=5)  # Label for File 2 selection
        self.compare_file_entry2 = ttk.Entry(file2_frame, width=50)  # Entry for File 2 path
        self.compare_file_entry2.pack(side=tk.LEFT,
                                      padx=5,
                                      fill=tk.X,
                                      expand=True)

        # Button to browse for File 2
        browse_btn2 = ttk.Button(file2_frame,
                                 text="Browse",
                                 command=self.browse_compare_file2)
        browse_btn2.pack(side=tk.LEFT, padx=5)

        # Button to perform comparison
        compare_btn = ttk.Button(files_frame,
                                 text="Compare Files",
                                 command=self.compare_files)
        compare_btn.pack(pady=10)

        # Results section for displaying statistics and comparison results
        results_frame = ttk.Frame(compare_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Left side - stats and comparison display
        left_frame = ttk.Frame(results_frame)   
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        lists_frame = ttk.Frame(left_frame)  # Frame for statistics lists
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # File 1 stats display
        file1_stats_frame = ttk.LabelFrame(lists_frame, text="File 1 Statistics")
        file1_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Text area for displaying statistics of File 1
        self.file1_stats_text = tk.Text(file1_stats_frame,
                                        height=5,
                                        width=40,
                                        wrap=tk.WORD)  
        self.file1_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # File 2 stats display
        file2_stats_frame = ttk.LabelFrame(lists_frame, text="File 2 Statistics")
        file2_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Text area for displaying statistics of File 2
        self.file2_stats_text = tk.Text(file2_stats_frame,
                                        height=5,
                                        width=40,
                                        wrap=tk.WORD)
        self.file2_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Comparison results display
        comparison_frame = ttk.LabelFrame(left_frame, text="Comparison Results")
        comparison_frame.pack(fill=tk.X, pady=10)

        # Text area for displaying similarity results
        self.comparison_text = tk.Text(comparison_frame,
                                       height=6,
                                       wrap=tk.WORD)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right side - comparison graph display
        right_frame = ttk.Frame(results_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Graph comparing word frequencies
        graph_frame = ttk.LabelFrame(right_frame, text="Word Frequency Comparison")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Canvas to draw the comparison graph
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
        config_tab = ttk.Frame(self.notebook)  # Create config tab frame
        self.notebook.add(config_tab, text="Configuration")  # Add to notebook

        # Frame for CLI settings
        CLI_settings_frame = ttk.LabelFrame(config_tab, text="CLI Settings")
        CLI_settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame for GUI settings
        GUI_settings_frame = ttk.LabelFrame(config_tab, text="GUI Settings")
        GUI_settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Single file display setting
        single_file_frame = ttk.Frame(CLI_settings_frame)  
        single_file_frame.pack(fill=tk.X, pady=10)

        # Label and entry for number of words to display in Analyze File tab
        ttk.Label(single_file_frame, 
                  text="Number of words to display in Analyze File tab:").pack(side=tk.LEFT, padx=5)
        self.single_file_display_var = tk.StringVar(value=str(config.single_file_display_line))  # Bind entry with current value
        self.single_file_display_entry = ttk.Entry(single_file_frame, 
                                                   width=10, 
                                                   textvariable=self.single_file_display_var)
        self.single_file_display_entry.pack(side=tk.LEFT, padx=5)

        # Compare files display setting
        compare_file_frame = ttk.Frame(CLI_settings_frame)  
        compare_file_frame.pack(fill=tk.X, pady=10)

        # Label and entry for number of words to display in Compare Files tab
        ttk.Label(compare_file_frame, 
                  text="Number of words to display in Compare Files tab:").pack(side=tk.LEFT, padx=5)
        self.compare_file_display_var = tk.StringVar(value=str(config.compare_file_display_line))  # Bind entry with current value
        self.compare_file_display_entry = ttk.Entry(compare_file_frame, 
                                                    width=10, 
                                                    textvariable=self.compare_file_display_var)
        self.compare_file_display_entry.pack(side=tk.LEFT, padx=5)

        # Frame for graph settings
        graph_settings_frame = ttk.LabelFrame(GUI_settings_frame, text="Graph Settings")  
        graph_settings_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Words display settings
        words_frame = ttk.Frame(graph_settings_frame)  
        words_frame.pack(fill=tk.X, pady=5)

        # Label and entry for max words in graph
        ttk.Label(words_frame, text="Max words in graph:").pack(side=tk.LEFT, padx=5)
        self.graph_max_words_var = tk.StringVar(value=str(config.graph_max_words))  # Bind entry with current value
        self.graph_max_words_entry = ttk.Entry(words_frame, width=10, textvariable=self.graph_max_words_var)
        self.graph_max_words_entry.pack(side=tk.LEFT, padx=5)

        # Label and entry for max words to show in text
        ttk.Label(words_frame, text="Max words to show in text:").pack(side=tk.LEFT, padx=5)
        self.analyze_max_words_var = tk.StringVar(value=str(config.analyze_max_words))  # Bind entry with current value
        self.analyze_max_words_entry = ttk.Entry(words_frame, width=10, textvariable=self.analyze_max_words_var)
        self.analyze_max_words_entry.pack(side=tk.LEFT, padx=5)

        # Frame for graph size settings
        size_frame = ttk.Frame(graph_settings_frame)  
        size_frame.pack(fill=tk.X, pady=5)

        # Label and entry for graph size
        ttk.Label(size_frame, text="Graph size (width, height):").pack(side=tk.LEFT, padx=5)
        self.graph_width_var = tk.StringVar(value=str(config.graph_figsize[0]))  # Bind entry with current value
        self.graph_width_entry = ttk.Entry(size_frame, width=5, textvariable=self.graph_width_var)
        self.graph_width_entry.pack(side=tk.LEFT, padx=2)

        self.graph_height_var = tk.StringVar(value=str(config.graph_figsize[1]))  # Bind entry with current value
        self.graph_height_entry = ttk.Entry(size_frame, width=5, textvariable=self.graph_height_var)
        self.graph_height_entry.pack(side=tk.LEFT, padx=2)

        # Frame for font settings
        font_frame = ttk.Frame(graph_settings_frame)  
        font_frame.pack(fill=tk.X, pady=5)

        # Label and entry for title font size
        ttk.Label(font_frame, text="Title font size:").pack(side=tk.LEFT, padx=5)
        self.title_font_var = tk.StringVar(value=str(config.graph_title_fontsize))  # Bind entry with current value
        self.title_font_entry = ttk.Entry(font_frame, width=5, textvariable=self.title_font_var)
        self.title_font_entry.pack(side=tk.LEFT, padx=5)

        # Label and entry for label font size
        ttk.Label(font_frame, text="Label font size:").pack(side=tk.LEFT, padx=5)
        self.label_font_var = tk.StringVar(value=str(config.graph_label_fontsize))  # Bind entry with current value
        self.label_font_entry = ttk.Entry(font_frame, width=5, textvariable=self.label_font_var)
        self.label_font_entry.pack(side=tk.LEFT, padx=5)

        # Frame for color settings
        colors_frame = ttk.Frame(graph_settings_frame)  
        colors_frame.pack(fill=tk.X, pady=5)

        # Label and entry for bar colors
        ttk.Label(colors_frame, text="Bar colors:").pack(side=tk.LEFT, padx=5)
        self.bar_color_single_var = tk.StringVar(value=str(config.graph_bar_color_single))  # Bind entry with current value
        ttk.Entry(colors_frame, width=10, textvariable=self.bar_color_single_var).pack(side=tk.LEFT, padx=2)

        self.bar_color_compare1_var = tk.StringVar(value=str(config.graph_bar_color_compare1))  # Bind entry with current value
        ttk.Entry(colors_frame, width=10, textvariable=self.bar_color_compare1_var).pack(side=tk.LEFT, padx=2)

        self.bar_color_compare2_var = tk.StringVar(value=str(config.graph_bar_color_compare2))  # Bind entry with current value
        ttk.Entry(colors_frame, width=10, textvariable=self.bar_color_compare2_var).pack(side=tk.LEFT, padx=2)

        # Buttons frame for actions
        buttons_frame = ttk.Frame(config_tab)  
        buttons_frame.pack(fill=tk.X, pady=20)

        # Button to save settings
        save_btn = ttk.Button(buttons_frame, 
                              text="Save settings", 
                              command=self.save_config)
        save_btn.pack(side=tk.RIGHT, padx=5)

        # Button to cancel changes
        cancel_btn = ttk.Button(buttons_frame, 
                                text="Cancel changes", 
                                command=self.reset_last_save_config)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

        # Button to reset to default values
        reset_btn = ttk.Button(buttons_frame, 
                                text="Reset values to default", 
                                command=self.reset_default_config)
        reset_btn.pack(side=tk.RIGHT, padx=5)

        # Add an info text section
        info_frame = ttk.Frame(config_tab)  
        info_frame.pack(fill=tk.X, pady=10)

        # Read-only text area for informational text
        info_text = tk.Text(info_frame, height=5, wrap=tk.WORD)
        info_text.pack(fill=tk.X, padx=10)
        info_text.insert(tk.END, 
                        "These settings control how many words are displayed in the word lists and graphs. " 
                        "Changes will be saved to the configuration file and applied immediately once the save button is pressed.")
        info_text.config(state=tk.DISABLED)  # Make the text read-only

    def browse_file1(self):
        """
        Open a file dialog to browse for a file to analyze.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):  # Open dialog for file selection
            self.file_entry1.delete(0, tk.END)  # Clear entry
            self.file_entry1.insert(0, file_path)  # Insert selected path
            self.file_path1 = file_path  # Store the selected path

    def browse_compare_file1(self):
        """
        Open a file dialog to browse for the first file to compare.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):  # Open dialog for file selection
            self.compare_file_entry1.delete(0, tk.END)  # Clear entry
            self.compare_file_entry1.insert(0, file_path)  # Insert selected path

    def browse_compare_file2(self):
        """
        Open a file dialog to browse for the second file to compare.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):  # Open dialog for file selection
            self.compare_file_entry2.delete(0, tk.END)  # Clear entry
            self.compare_file_entry2.insert(0, file_path)  # Insert selected path

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
        file_path = self.file_entry1.get()  # Get the selected file path
        if not file_path:  # Check if a file path has been provided
            messagebox.showerror("Error", "Please select a file first.")  # Show error message
            return  # Exit method if no file selected

        # Read and process file
        content = read_file(file_path)  # Read the file using a helper function
        if content is None:  # Check if content read successfully
            messagebox.showerror("Error", f"Could not read file: {file_path}")  # Show error message
            return  # Exit method on error

        clean_content = clean_text(content)  # Clean the text content
        word_count = count_words(clean_content)  # Analyze word count from the cleaned text
        total_words = len(clean_content.split(" "))  # Count total words
        unique_words = len(word_count[0])  # Count unique words

        # Display statistics in the statistics text area
        self.stats_text.delete(1.0, tk.END)  # Clear previous statistics
        self.stats_text.insert(tk.END, f"File: {os.path.basename(file_path)}\n")  # Display file name
        self.stats_text.insert(tk.END, f"Total words: {total_words}\n")  # Display total words
        self.stats_text.insert(tk.END, f"Unique words: {unique_words}\n")  # Display unique words

        # Display word lists in their respective listboxes
        self.freq_list.delete(0, tk.END)  # Clear previous frequency list
        freq_sorted = sort_by_frequency(word_count)[:config.analyze_max_words]  # Get sorted frequency list
        for i, (word, count) in enumerate(freq_sorted):  # Iterate through sorted list
            self.freq_list.insert(tk.END, f"{i + 1}. '{word}': {count} times")  # Insert words and counts

        self.alpha_list.delete(0, tk.END)  # Clear previous alphabetical list
        alpha_sorted = sort_alphabetically(word_count)[:config.analyze_max_words]  # Get sorted alphabetical list
        for i, (word, count) in enumerate(alpha_sorted):  # Iterate through sorted list
            self.alpha_list.insert(tk.END, f"{i + 1}. '{word}': {count} times")  # Insert words and counts

        # Create and display the frequency graph
        self.create_frequency_graph(word_count, self.graph_canvas1)  # Draw graph for the current file

        # Store data for later use
        self.word_count1 = word_count  # Store word count data
        self.clean_content1 = clean_content  # Store cleaned content

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

        # Get the top words by frequency
        freq_sorted = sort_by_frequency(word_count)  # Sort word counts
        top_words = freq_sorted[:max_words]  # Limit to max words

        if not top_words:  # If no top words, exit function
            return

        # Create a figure for the graph
        fig, ax = plt.subplots(figsize=config.graph_figsize)

        words = [word for word, _ in top_words]  # List of top words
        counts = [count for _, count in top_words]  # List of counts for top words

        # Create a horizontal bar chart
        bars = ax.barh(words, counts, color=config.graph_bar_color_single)

        # Set labels and titles for the graph
        ax.set_xlabel('Frequency', fontsize=config.graph_label_fontsize)  # X-axis label
        ax.set_title('Top Word Frequencies', fontsize=config.graph_title_fontsize)  # Graph title
        ax.tick_params(labelsize=config.graph_label_fontsize)  # Set tick params for labels

        # Add count labels on bars
        for bar in bars:
            width = bar.get_width()  # Get bar width
            ax.text(width + 0.5,
                    bar.get_y() + bar.get_height() / 2,
                    f'{width}',
                    ha='left',
                    va='center')  # Display count on bar

        plt.tight_layout()  # Adjust layout

        # Embed the graph in the canvas
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)  # Create canvas for matplotlib figure
        canvas.draw()  # Draw the figure
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Pack canvas into the Tkinter widget

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
        file_path1 = self.compare_file_entry1.get()  # Get path for the first file
        file_path2 = self.compare_file_entry2.get()  # Get path for the second file

        if not file_path1 or not file_path2:  # Check if both file paths have been provided
            messagebox.showerror("Error", "Please select both files.")  # Show error if missing
            return  # Exit method on error

        # Read and process both files
        content1 = read_file(file_path1)  # Read first file content
        content2 = read_file(file_path2)  # Read second file content

        if content1 is None or content2 is None:  # Check if readings were successful
            messagebox.showerror("Error", "Could not read one or both files.")  # Show error message
            return  # Exit method on error

        clean_content1 = clean_text(content1)  # Clean content of the first file
        clean_content2 = clean_text(content2)  # Clean content of the second file
        
        word_count1 = count_words(clean_content1)  # Count words in the first cleaned text
        word_count2 = count_words(clean_content2)  # Count words in the second cleaned text
        
        total_words1 = len(clean_content1.split(" "))  # Count total words in the first text
        total_words2 = len(clean_content2.split(" "))  # Count total words in the second text
        
        unique_words1 = len(word_count1[0])  # Count unique words in the first text
        unique_words2 = len(word_count2[0])  # Count unique words in the second text

        # Display statistics for file 1
        self.file1_stats_text.delete(1.0, tk.END)  # Clear previous statistics 
        self.file1_stats_text.insert(tk.END, f"File: {os.path.basename(file_path1)}\n")  # Display file name
        self.file1_stats_text.insert(tk.END, f"Total words: {total_words1}\n")  # Display total words
        self.file1_stats_text.insert(tk.END, f"Unique words: {unique_words1}\n")  # Display unique words

        # Display statistics for file 2
        self.file2_stats_text.delete(1.0, tk.END)  # Clear previous statistics 
        self.file2_stats_text.insert(tk.END, f"File: {os.path.basename(file_path2)}\n")  # Display file name
        self.file2_stats_text.insert(tk.END, f"Total words: {total_words2}\n")  # Display total words
        self.file2_stats_text.insert(tk.END, f"Unique words: {unique_words2}\n")  # Display unique words

        # Calculate and display similarity
        similarity = calculate_similarity(word_count1, word_count2)  # Calculate similarity percentage

        self.comparison_text.delete(1.0, tk.END)  # Clear previous comparison results
        self.comparison_text.insert(tk.END, f"Similarity percentage: {similarity:.2f}%\n\n")  # Display similarity percentage

        # Determine plagiarism level based on similarity percentage
        if similarity > 80:
            level = "HIGH - These texts are very similar"
            self.comparison_text.tag_configure("color", foreground="red")
        elif similarity > 50:
            level = "MEDIUM - These texts have significant overlap"
            self.comparison_text.tag_configure("color", foreground="orange")
        elif similarity > 20:
            level = "LOW - These texts have some common elements"
            self.comparison_text.tag_configure("color", foreground="yellow")
        else:
            level = "MINIMAL - These texts are mostly different"
            self.comparison_text.tag_configure("color", foreground="green")

        self.comparison_text.insert(tk.END, f"Plagiarism Level: {level}")  # Display plagiarism level
        self.comparison_text.tag_add("color", "end -1 lines", tk.END)
        
        # Create comparison graph
        self.create_comparison_graph(word_count1, word_count2, self.compare_canvas)  # Draw graph for comparisons

    def create_comparison_graph(self, word_count1, word_count2, canvas_widget, max_words=config.graph_max_words):
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
        freq_sorted1 = sort_by_frequency(word_count1)  # Sort word counts from first file
        freq_sorted2 = sort_by_frequency(word_count2)  # Sort word counts from second file

        # Create sets of top words for both files
        top_words1 = {word for word, _ in freq_sorted1[:max_words]}  # Extract top words for first file
        top_words2 = {word for word, _ in freq_sorted2[:max_words]}  # Extract top words for second file

        # Combine top words into a single list
        combined_top_words = list(top_words1.union(top_words2))  # Union of both sets

        if not combined_top_words:  # If no words to compare
            return  # Exit function

        # Get counts for each word in both files
        counts1 = []  
        counts2 = []

        for word in combined_top_words:  # Iterate through combined top words
            # Get count in the first file
            if word in word_count1[0]:
                idx = helpers.linear_search(word_count1[0], word)  # Find index in word count
                counts1.append(word_count1[1][idx])  # Append count
            else:
                counts1.append(0)  # Append zero count if word not present

            # Get count for the second file
            if word in word_count2[0]:
                idx = helpers.linear_search(word_count2[0], word)  # Find index in word count
                counts2.append(word_count2[1][idx])  # Append count
            else:
                counts2.append(0)  # Append zero count if word not present

        # Create figure for comparison graph
        fig, ax = plt.subplots(figsize=config.graph_figsize)

        x = range(len(combined_top_words))  # X-axis positions for bars
        width = 0.35  # Width of bars

        # Create bar chart for both files
        ax.bar([i - width / 2 for i in x], counts1, width, label='File 1', color=config.graph_bar_color_compare1)  # Bars for first file
        ax.bar([i + width / 2 for i in x], counts2, width, label='File 2', color=config.graph_bar_color_compare2)  # Bars for second file

        # Add labels and legend
        ax.set_ylabel('Frequency')  # Y-axis label
        ax.set_title('Word Frequency Comparison')  # Graph title
        ax.set_xticks(x)  # Set positions for x-ticks
        ax.set_xticklabels(combined_top_words, rotation=45, ha='right')  # Set labels for x-ticks
        ax.legend()  # Display legend

        plt.tight_layout()  # Adjust layout for better spacing

        # Embed the graph in the canvas
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)  # Create canvas for matplotlib figure
        canvas.draw()  # Draw the figure
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Pack canvas into the Tkinter widget
        
    def save_config(self):
        """
        Save the configuration settings to the config file.

        This method retrieves current user settings from the input fields,
        validates them, and updates the config accordingly. All changes are
        saved in the WAPDS.config file.
        """
        try:
            # Get and validate values from entry fields
            single_file_display = int(self.single_file_display_var.get())  # Get single file display line count
            compare_file_display = int(self.compare_file_display_var.get())  # Get compare file display line count
            graph_max_words = int(self.graph_max_words_var.get())  # Get max graph words
            analyze_max_words = int(self.analyze_max_words_var.get())  # Get max analyze words
            graph_width = float(self.graph_width_var.get())  # Get graph width
            graph_height = float(self.graph_height_var.get())  # Get graph height
            title_fontsize = float(self.title_font_var.get())  # Get title font size
            label_fontsize = float(self.label_font_var.get())  # Get label font size

            # Check for non-positive numbers in the configuration settings
            if helpers.any(x <= 0 for x in [
                single_file_display, compare_file_display,
                graph_max_words, analyze_max_words,
                graph_width, graph_height,
                title_fontsize, label_fontsize]):
                messagebox.showerror("Error", "All numeric settings must be positive numbers.")
                return  # Exit method on error

            # Update config with new values
            config.single_file_display_line = single_file_display
            config.compare_file_display_line = compare_file_display
            config.graph_max_words = graph_max_words
            config.analyze_max_words = analyze_max_words
            config.graph_figsize = (graph_width, graph_height)  # Update figure size
            config.graph_title_fontsize = title_fontsize
            config.graph_label_fontsize = label_fontsize
            config.graph_bar_color_single = self.bar_color_single_var.get()  # Update single color
            config.graph_bar_color_compare1 = self.bar_color_compare1_var.get()  # Update compare file 1 color
            config.graph_bar_color_compare2 = self.bar_color_compare2_var.get()  # Update compare file 2 color

            config.save()  # Save to config file

            messagebox.showinfo("Configuration", "Settings saved successfully!")  # Notify successful save
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for both settings.")  # Notify of invalid input

    def reset_last_save_config(self):
        """
        Reset the configuration fields to their current values.

        This method resets the input fields to the last saved values
        from the configuration.
        """
        self.single_file_display_var.set(str(config.single_file_display_line))  # Restore single file display setting
        self.compare_file_display_var.set(str(config.compare_file_display_line))  # Restore compare file display setting
        self.graph_max_words_var.set(str(config.graph_max_words))  # Restore graph max words setting
        self.analyze_max_words_var.set(str(config.analyze_max_words))  # Restore analyze max words setting
        self.graph_width_var.set(str(config.graph_figsize[0]))  # Restore graph width
        self.graph_height_var.set(str(config.graph_figsize[1]))  # Restore graph height
        self.title_font_var.set(str(config.graph_title_fontsize))  # Restore title font size
        self.label_font_var.set(str(config.graph_label_fontsize))  # Restore label font size
        self.bar_color_single_var.set(str(config.graph_bar_color_single))  # Restore single bar color
        self.bar_color_compare1_var.set(str(config.graph_bar_color_compare1))  # Restore color for first compare file
        self.bar_color_compare2_var.set(str(config.graph_bar_color_compare2))  # Restore color for second compare file

    def reset_default_config(self):
        """
        Reset the configuration fields to their default values.

        This method resets all fields in the configuration tab to their preset
        default values defined in the config class.
        """
        config.reset_to_defaults()  # Reset config class to defaults
        self.reset_last_save_config()  # Restore the input fields to the default values

        messagebox.showinfo("Configuration", "Settings reset to default values.")  # Notify user
        
        
def configure_test_input(prompt: str, type, was: str, error: str = ""):
    """Prompt the user for input in the command line interface (CLI)
    and validate if the input is of the specified type.

    Args:
        prompt (str): The input prompt message for the user.
        type (type): The expected data type of the input (e.g., int, float, str).
        was (str): The previous value that was set for context.
        error (str, optional): Custom error message if input is invalid. Defaults to an empty string.

    Raises:
        ValueError: If the input does not meet the expected format or constraints.

    Returns:
        type: The validated input converted to the specified type.
    """
    try:
        # Request user input with the given prompt
        temp_unsaved = input(f"{prompt} (was {was}): ")

        # Handling for different types of input
        if type == int:
            temp_unsaved = int(temp_unsaved)
            if temp_unsaved > 0:  # Validate that input is a positive integer
                return temp_unsaved
            else:
                raise ValueError  # Trigger exception for invalid input
        elif type == float:
            temp_unsaved = float(temp_unsaved)
            if temp_unsaved > 0:  # Validate that input is a positive float
                return temp_unsaved
            else:
                raise ValueError  # Trigger exception for invalid input
        else:
            return type(temp_unsaved)  # Convert input to the specified type

    except ValueError:
        # Handle and print error message for invalid input
        print("\x1b[31mInvalid input. ", end="")
        # Customized error message if provided
        if error:
            print(error, end="")
        elif type == int:
            print("Please enter a positive integer.", end="")
        elif type == float:
            print("Please enter a positive float.", end="")
        else:
            print("Please enter a valid string.", end="")  # General error for other types
        print("\x1b[m")  # Reset terminal color

def configure():
    """
    Configure the settings for the program via user input in CLI.

    This function presents a menu of configurable options to the user and captures
    their input using the `configure_test_input` function to validate and set 
    various configuration parameters including display lines, graph settings, and colors.

    The settings include:
    - Display lines for a single file
    - Display lines for file comparison
    - Maximum words for graph display
    - Figure size for graphs
    - Colors for graph bars
    - Font sizes for titles and labels
    """
    # Initialize unsaved configuration values
    unsaved_single_file_display_line = None
    unsaved_compare_file_display_line = None
    unsaved_graph_max_words = None
    unsaved_graph_figsize_h = None
    unsaved_graph_figsize_w = None
    unsaved_analyze_max_words = None
    unsaved_graph_bar_color_single = None
    unsaved_graph_bar_color_compare1 = None
    unsaved_graph_bar_color_compare2 = None
    unsaved_graph_title_fontsize = None
    unsaved_graph_label_fontsize = None

    while True:
        # Display the current configurable settings and menu options
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
            [*"Graph ", "\x1b[1;4;97mL\x1b[m", *f"abel: set font size to {config.graph_label_fontsize if unsaved_graph_label_fontsize is None else f'{unsaved_graph_label_fontsize} (was {config.graph_label_fontsize})'}"],
            ["\x1b[1;4mS\x1b[m", *"ave and exit"],
            ["\x1b[1;4;97mE\x1b[m", *"xit without saving"]], _override=True)  # Formatting the options menu
        
        # Prompt for configuration option from user
        config_option = input("Enter option: ", single_letter=True).upper().strip()

        # Checking user choice and prompting for corresponding input
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
        elif config_option in "ES":  # If user selects Exit or Save, break the loop
            break
        else:
            print(f"Invalid option {repr(config_option)}. Please try again.")  # Inform user of invalid input
        
    # If changes need to be saved, update the configuration
    if config_option == "S":
        # Update configuration variables with unsaved values
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

        # Save updated configuration to persistent storage
        config.save()

def display_results(file_path, word_count, total_words, unique_words, show_nums=10, warp=os.get_terminal_size().columns):
    """
    Display analysis results for a single text file in CLI mode.
    
    This function shows:
    - The analysis heading and statistics
    - The most frequent words
    - Words sorted alphabetically
    
    Args:
        file_path (str): The path to the analyzed text file
        word_count (tuple): Word count data as returned by count_words()
        total_words (int): Total number of words in the file
        unique_words (int): Number of unique words in the file
        show_nums (int): Number of top words to display (default is 10)
        warp (int): The terminal width to wrap text (default is the current terminal size)
    """
    # Limit number of words to display to available words
    show_nums = helpers.min(show_nums, len(word_count[0]))  # Maximum words to show is the smaller of user request or available data
    hyphen_warp = helpers.min(warp, len(str(show_nums)) + 30)  # Text wrapping limit

    # Print header and statistics
    print(f"\
\n\
{'=' * helpers.min(warp, len(file_path) + 15)}\n\
Analysis of '{file_path}':\n\
{'=' * helpers.min(warp, len(file_path) + 15)}\n\
Total words: {total_words}\n\
Unique words: {unique_words}\n\
\n\
\n\
Top {show_nums} Most Frequent Words:\n\
{'-' * hyphen_warp}")

    # Print frequency-sorted words
    frequency_sorted = sort_by_frequency(word_count)  # Get list of words sorted by frequency
    txt = "".join(f"{i + 1}. '{word}': {count} times\n" for i, (word, count) in enumerate(frequency_sorted[:show_nums]))  # Format output
    print(txt)  # Display formatted word frequency information

    # Print alphabetically-sorted words
    txt = f"\nFirst {show_nums} Words (Alphabetically):\n{'-' * hyphen_warp}\n"  # Setup string for display
    alpha_sorted = sort_alphabetically(word_count)  # Get list of words sorted alphabetically
    for i, (word, count) in enumerate(alpha_sorted[:show_nums]):  # Iterate and format
        txt += f"{i + 1}. '{word}': {count} times\n"  # Append formatted string
    print(txt)  # Display the final formatted alphabetical listings

def compare_files(file_path1, file_path2):
    """
    Compare two text files and calculate their similarity percentage for CLI mode.
    
    This function reads both files, cleans and analyzes their content,
    and displays word frequencies. It provides comparison results along
    with a calculated similarity percentage.

    Args:
        file_path1 (str): The path to the first text file
        file_path2 (str): The path to the second text file
    """
    columns = os.get_terminal_size().columns  # Get the current terminal width

    # Read and process the files
    content1 = read_file(file_path1)  # Read the first text file's content
    content2 = read_file(file_path2)  # Read the second text file's content

    # Check if both files were successfully read
    if content1 is None or content2 is None:
        print("\x1b[31mError: Cannot compare files due to reading errors.\x1b[m")  # Display error message
        return  # Exit function early due to error

    # Clean and analyze the text from both files
    clean_content1 = clean_text(content1)  # Clean text content of the first file
    clean_content2 = clean_text(content2)  # Clean text content of the second file

    word_count1 = count_words(clean_content1)  # Count words from the first cleaned text
    word_count2 = count_words(clean_content2)  # Count words from the second cleaned text

    total_words1 = len(clean_content1.split(" "))  # Count total words in the first text
    total_words2 = len(clean_content2.split(" "))  # Count total words in the second text

    unique_words1 = len(word_count1[0])  # Count unique words in the first text
    unique_words2 = len(word_count2[0])  # Count unique words in the second text

    # Display analysis results for each file
    display_results(file_path1, word_count1, total_words1, unique_words1, config.compare_file_display_line)  # Show results for the first file
    display_results(file_path2, word_count2, total_words2, unique_words2, config.compare_file_display_line)  # Show results for the second file

    # Calculate and display the similarity percentage between the two files
    similarity = calculate_similarity(word_count1, word_count2)  # Get similarity percentage from both word counts

    # Print heading for comparison results
    print(
        f"\n{'=' * helpers.min(columns, len(file_path1) + len(file_path2) + 30)}\n\
Comparison between '{file_path1}' and '{file_path2}':\n\
{'=' * helpers.min(columns, len(file_path1) + len(file_path2) + 30)}\n\
Similarity percentage: {similarity:.2f}%"
    )

    # Determine and display the plagiarism level using the similarity percentage
    if similarity > 80:
        print("\x1b[31mPlagiarism Level: HIGH - These texts are very similar\x1b[m")  # High similarity
    elif similarity > 50:
        print("\x1b[33mPlagiarism Level: MEDIUM - These texts have significant overlap\x1b[m")  # Medium similarity
    elif similarity > 20:
        print("\x1b[92mPlagiarism Level: LOW - These texts have some common elements\x1b[m")  # Low similarity
    else:
        print("\x1b[32mPlagiarism Level: MINIMAL - These texts are mostly different\x1b[m")  # Minimal similarity

def analyze_file(file_path):
    """
    Analyze a single text file for CLI mode.
    
    This function reads the specified file, cleans its content,
    counts words, determines total and unique word counts,
    and then displays results using display_results().

    Args:
        file_path (str): The path to the file to analyze

    Returns:
        tuple: A tuple containing word count data and cleaned content,
               or None if an error occurred.
    """
    # Read and process the file content
    content = read_file(file_path)  # Attempt to read the file content

    if content is None:  # If reading fails, exit function
        return

    clean_content = clean_text(content)  # Clean the raw file content
    word_count = count_words(clean_content)  # Count words in the cleaned content
    total_words = len(clean_content.split(" "))  # Calculate total words
    unique_words = len(word_count[0])  # Calculate unique words

    # Display analysis results for the analyzed file
    display_results(file_path, word_count, total_words, unique_words, config.single_file_display_line)  # Show results

def GUI_exit(root):
    """
    Exit the GUI application with a confirmation dialog.

    Args:
        root: The main window of the tkinter application.

    This function prompts the user with a message box asking for confirmation
    before quitting the application and thanking them for using it.
    """
    # Ask user for confirmation to quit
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        messagebox.showwarning("Thank you, app closing...", message="Thank you for using WAPDS")  # Thanking message
        root.destroy()  # Destroy the root window to close the application
        exit()  # Exit the script completely

def mainGUI():
    """
    Start the GUI version of the Word Analysis and Plagiarism Detection System.

    This function initializes the tkinter window, creates an instance of the application,
    and sets up a dialog confirmation when the user attempts to close the window.
    """
    root = tk.Tk()  # Create main tkinter window
    app = WordAnalysisApp(root, config.window_size)  # Instantiate main Application class

    # Configure window close behavior to confirm exit
    root.protocol("WM_DELETE_WINDOW", lambda: GUI_exit(root))  # Set exit protocol to use custom exit function

    # Begin the main event loop to run the application
    root.mainloop()

def mainCLI():
    """
    Start the CLI version of the Word Analysis and Plagiarism Detection System.

    This function presents a text-based menu interface for users to choose
    file analysis, comparison, configuration, and exit options.
    """
    columns = os.get_terminal_size().columns  # Get terminal width for formatting
    print("Word Analysis and Plagiarism Detection System\n" +
          "-" * helpers.min(columns, 45))  # Print intro header

    while True:
        # Display the main menu options
        print("\
\nMenu:\n\
1. Analyze a single file\n\
2. Compare two files for plagiarism\n\
3. Configure settings\n\
4. Exit\n")

        # Prompt user for choice and capture input
        choice = input("\nEnter your choice (1-4): ", single_letter=True).strip()

        # Handle each choice using if-elif statements
        if choice == '1':
            file_path = input("Enter the path to the text file: ").strip()  # Capture path for analysis
            analyze_file(file_path)  # Call the analyze function for the selected file

        elif choice == '2':
            file_path1 = input("Enter the path to the first text file: ").strip()  # Path for first file
            file_path2 = input("Enter the path to the second text file: ").strip()  # Path for second file
            compare_files(file_path1, file_path2)  # Call compare function on selected files

        elif choice == '3':
            configure()  # Call configuration function

        elif choice == '4':
            print("Thank you for using WAPDS!")  # Goodbye message
            break  # Exit the loop

        else:
            print(f"Invalid choice {repr(choice)}. Please enter a number between 1 and 4.")  # Input error handling

if __name__ == "__main__":
    # Parse command line arguments to determine whether to run GUI or CLI version of the application
    some_text = "{width}x{height}"  # Template for GUI window dimension formatting
    parser = argparse.ArgumentParser(description="Word Analysis and Plagiarism Detection System (WAPDS)")  # Setup argument parser
    parser.add_argument(
        "run_type",
        help='Enter "GUI" or "CLI" to determine which version should run, defaults to GUI',
        nargs="?",  # Optional argument with default
        default="GUI")  # Default to GUI if not provided
    parser.add_argument(
        "GUI_window_size",
        help=f'Enter in format of {some_text}, set the GUI window size and will be saved, defaults to last window size (currently {repr(config.window_size)})',
        nargs="?",  # Optional argument for GUI window size configuration
        default=config.window_size)  # Default size of the window
    args = parser.parse_args()  # Parse the command-line arguments

    # Start the appropriate interface based on the argument provided
    if args.run_type == "GUI":
        try:
            # Set GUI window size 
            GUI_window_size_check = args.GUI_window_size.strip().split("x")  # Split input into width and height
            GUI_window_size_check = [int(dimension) for dimension in GUI_window_size_check]  # Convert dimensions into integers
            if len(GUI_window_size_check) != 2:  # Check for two dimensions
                raise ValueError  # Raise an error if not valid
            for n in GUI_window_size_check:  # Validate each dimension
                if n <= 0:  # Ensure dimensions are positive
                    raise ValueError
        except ValueError:
            # If parsing fails, inform the user of the formatting error
            parser.error(f'Please enter GUI window size in the format of {some_text}, not {repr(args.GUI_window_size)}')
        config.window_size = args.GUI_window_size.strip()  # Set the new window size in the config
        config.save()  # Save the new configurations
        mainGUI()  # Launch GUI application
    elif args.run_type == "CLI":
        # Import animated print and input functions for better user experience in CLI mode
        from helpers import animated_print as print, animated_input as input
        mainCLI()  # Launch CLI application
    else:
        # If an invalid run type is provided, inform the user
        parser.error(f'Please enter either "GUI" or "CLI" for run type, not {repr(args.run_type)}')
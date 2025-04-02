import os  # Import module for terminal size detection and file operations
import helpers  # Import custom helper functions that avoid using built-in functions
import tkinter as tk  # Import tkinter for GUI implementation
import re  # Import regex module for pattern matching
# (I heard that GUI use of it is fine probably)
from tkinter import ttk, filedialog, messagebox  # Import some tkinter components specificly
try:
    from nltk_plagiarism import get_similarity_score # For advance stuff
except (ImportError, ModuleNotFoundError):
    get_similarity_score = None  # Set get_similarity_score to None so we can check if the entirety of nltk is available later
try:
    import matplotlib.pyplot as plt  # Import matplotlib for data visualization
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # For embedding matplotlib in tkinter
    from matplotlib.backends._backend_tk import NavigationToolbar2Tk  # For embedding toolbar for matplotlib
except (ImportError, ModuleNotFoundError):
    plt = None  # Set plt to None so we can check if matplotlib is available later
import argparse  # For command-line argument parsing


class config:
    """
    Configuration management class for WAPDS (Word Analysis and Plagiarism Detection System).

    This class handles loading, storing, and saving application settings.
    It maintains default values and provides methods to reset settings.

    Attributes:
        DEFAULTS["CLI"] (list): Default values for Command Line Interface (CLI) settings
        DEFAULTS["GUI"] (list): Default values for Graphical User Interface (GUI) settings
        single_file_display_line (int): Number of words to display in single file analysis (CLI)
        compare_file_display_line (int): Number of words to display in file comparison (CLI)
        window_size (str): Size of the GUI window in "widthxheight" format
        graph_max_words (int): Maximum number of words to display in graphs
        graph_figsize (list): Size of matplotlib figures [width, height]
        analyze_max_words (int): Maximum number of words to display in analysis lists
        graph_bar_color_single (str): Color for bars in single file analysis
        graph_bar_color_compare1 (str): Color for bars of first file in comparison
        graph_bar_color_compare2 (str): Color for bars of second file in comparison
        graph_title_fontsize (int): Font size for graph titles
        graph_label_fontsize (int): Font size for graph labels
        dark_mode (bool): Whether dark mode is enabled
        text_font_size (int): Font size for text labels
    """

    # Default values for CLI and GUI settings
    DEFAULTS = {"CLI": {
        "single_file_display_line": 10, 
        "compare_file_display_line": 5
                    },
                "GUI": {
        "window_size": "1000x700", 
        "graph_max_words": "10", 
        "graph_figsize": [5, 4], 
        "analyze_max_words": 5, 
        "graph_bar_color_single": "skyblue", 
        "graph_bar_color_compare1": "skyblue", 
        "graph_bar_color_compare2": "lightgreen", 
        "graph_title_fontsize": 12, 
        "graph_label_fontsize": 10, 
        "dark_mode": False, 
        "text_font_size": 10
                    }
                }

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
            graph_figsize = [float(config_data[4]), float(config_data[5])]  # Figure size for graphs
            analyze_max_words = int(config_data[6])  # Max words to show in analysis lists
            graph_bar_color_single = str(config_data[7])  # Bar color for single analysis
            graph_bar_color_compare1 = str(config_data[8])  # First file comparison bar color
            graph_bar_color_compare2 = str(config_data[9])  # Second file comparison bar color
            graph_title_fontsize = int(config_data[10])  # Font size for graph titles
            graph_label_fontsize = int(config_data[11])  # Font size for graph labels
            dark_mode = bool(int(config_data[12]))  # Dark mode setting (stored as 0/1)
            text_font_size = int(config_data[13])  # Font size for text labels

    except:
        # Use default settings if the configuration file doesn"t exist or is corrupted
        single_file_display_line = DEFAULTS["CLI"]["single_file_display_line"]
        compare_file_display_line = DEFAULTS["CLI"]["compare_file_display_line"]
        window_size = DEFAULTS["GUI"]["window_size"]
        graph_max_words = DEFAULTS["GUI"]["graph_max_words"]
        graph_figsize = DEFAULTS["GUI"]["graph_figsize"]
        analyze_max_words = DEFAULTS["GUI"]["analyze_max_words"]
        graph_bar_color_single = DEFAULTS["GUI"]["graph_bar_color_single"]
        graph_bar_color_compare1 = DEFAULTS["GUI"]["graph_bar_color_compare1"]
        graph_bar_color_compare2 = DEFAULTS["GUI"]["graph_bar_color_compare2"]
        graph_title_fontsize = DEFAULTS["GUI"]["graph_title_fontsize"]
        graph_label_fontsize = DEFAULTS["GUI"]["graph_label_fontsize"]
        dark_mode = DEFAULTS["GUI"]["dark_mode"]
        text_font_size = DEFAULTS["GUI"]["text_font_size"]

    # Write/update config file with current settings
    with open("WAPDS.config", "w") as f:
        f.write(f"{single_file_display_line};{compare_file_display_line};{window_size};"
                f"{graph_max_words};{graph_figsize[0]};{graph_figsize[1]};"
                f"{analyze_max_words};{graph_bar_color_single};"
                f"{graph_bar_color_compare1};{graph_bar_color_compare2};"
                f"{graph_title_fontsize};{graph_label_fontsize};{int(dark_mode)};{text_font_size}")

    @classmethod
    def reset_to_defaults(cls):
        """
        Reset all settings to their default values.

        This method restores all configuration parameters to the predefined default values
        but does not save them to the configuration file.
        """
        # Restore CLI default values
        cls.single_file_display_line = cls.DEFAULTS["CLI"]["single_file_display_line"]
        cls.compare_file_display_line = cls.DEFAULTS["CLI"]["compare_file_display_line"]
        # Restore GUI default values
        cls.window_size = cls.DEFAULTS["GUI"]["window_size"]
        cls.graph_max_words = cls.DEFAULTS["GUI"]["graph_max_words"]
        cls.graph_figsize = cls.DEFAULTS["GUI"]["graph_figsize"]
        cls.analyze_max_words = cls.DEFAULTS["GUI"]["analyze_max_words"]
        cls.graph_bar_color_single = cls.DEFAULTS["GUI"]["graph_bar_color_single"]
        cls.graph_bar_color_compare1 = cls.DEFAULTS["GUI"]["graph_bar_color_compare1"]
        cls.graph_bar_color_compare2 = cls.DEFAULTS["GUI"]["graph_bar_color_compare2"]
        cls.graph_title_fontsize = cls.DEFAULTS["GUI"]["graph_title_fontsize"]
        cls.graph_label_fontsize = cls.DEFAULTS["GUI"]["graph_label_fontsize"]
        cls.dark_mode = cls.DEFAULTS["GUI"]["dark_mode"]
        cls.text_font_size = cls.DEFAULTS["GUI"]["text_font_size"]

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
                    f"{cls.graph_title_fontsize};{cls.graph_label_fontsize};{int(cls.dark_mode)};"
                    f"{cls.text_font_size}")



def read_file(file_path:str) -> str|None:
    """
    Read a text file and return its content as a string.

    Args:
        file_path (str): Path to the file to be read

    Returns:
        str or None: The content of the file as a string, or None if an error occurred.

    This function handles file reading with error checking for file not found
    and other exceptions. It also warns if the file is empty.
    """
    # Get list of text files in current directory for suggestions if file not found
    txt_files = [file for file in os.listdir() if os.path.isfile(file) and file.endswith(".txt")]
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f'\x1b[31mError: File "{file_path}" not found.\x1b[m')
        # Suggest similar filename if available
        if file_path+".txt" in txt_files:
            print(f'\x1b[33mDid you mean "{file_path}.txt"?\x1b[m')
        return None
        
    # Check if path is a file (not a directory)
    if not os.path.isfile(file_path):
        print(f'\x1b[31mError: "{file_path}" is not a file.\x1b[m')
        return None
        
    try:
        # Attempt to read the file
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()  # Read the entire file content
        
        # Check if file is empty
        if not content.strip():  # Check if the file is empty
            print(f'\x1b[33mWarning: File "{file_path}" is empty.\x1b[m')
        return content  # Return file content
    except Exception as e:  # Handle other exceptions
        print(f'\x1b[31mError reading file "{file_path}": {str(e)}\x1b[m')
        return None  # Return None for error


def clean_text(text:str|None) -> str:
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

    # Replace any character that isn"t a letter, digit, or space with a space
    # This preserves word boundaries while removing punctuation
    cleaned_text = "".join((char if "a" <= char <= "z" or "0" <= char <= "9"
                            or char == " " else " ") for char in text.lower())

    # Remove extra spaces (replace double spaces with single until no doubles remain)
    while "  " in cleaned_text:
        cleaned_text = cleaned_text.replace("  ", " ")

    return cleaned_text.strip()  # Return cleaned and stripped text


def count_words(text:str) -> tuple[list, list]:
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

    # Initialize result structure as a tuple of two lists as an alternative to dictionary
    word_count = ([], [])  # ([words], [frequencies])
    words = text.split(" ")  # Split text into individual words

    # Count frequency of each word using a for loop
    for n in range(len(words)): #will use enumerate later on, which is faster than range(len()) and then thing[idx]
        word = words[n] #because enumerate is O(N), range(len()) O(N) + O(N) = O(2N) > O(N)
        word_index = helpers.linear_search(word_count[0], word)
        if word_index != -1:  # Check if word already exists in our list
            # If word already exists, increment its count
            word_count[1][word_index] += 1
        else:
            # Otherwise, add it to our list with a count of 1
            word_count[0].append(word)
            word_count[1].append(1)

    return word_count  # Return the word counts



def search_word_position(text:str, target_word:str, regex:bool = False) -> list[tuple,]:
    """
    Search for a target word or pattern in the text and return its positions.
    
    Args:
        text (str): The text to search within (original text with punctuation)
        target_word (str): The word or pattern to search for
        regex (bool): Whether to treat target_word as a regular expression
        
    Returns:
        list: A list of tuples (position, matched_text) where the target appears
              (empty list if word not found or inputs are invalid)
              
    This function finds all occurrences of the target word or pattern in the original text,
    ignoring case but preserving the original formatting in the results.
    """
    # Check for empty inputs
    if not text or not target_word:
        return []
    
    results = []  # Initialize list to store results
    
    if regex:
        try:
            # Use regex pattern to find matches
            pattern = re.compile(target_word, re.IGNORECASE)
            words = text.split()
            
            # Find all matches with their positions
            for idx in range(len(words)):
                word = words[idx]
                if pattern.search(word):
                    results.append((idx, word))
        except re.error:
            # Handle invalid regex pattern
            return []
    else:
        # Standard word search (case-insensitive)
        words = text.split()
        target_word = target_word.lower()
        
        # Find all exact matches with their positions
        for idx, word in enumerate(words):
            # Remove punctuation for comparison but keep original word
            clean_word = "".join(c.lower() for c in word if c.isalnum())
            if clean_word == target_word:
                results.append((idx, word))
    
    return results  # Return all found positions with matched text


def sort_alphabetically(word_count:tuple[list, list]) -> list[tuple[str, int],]:
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
    for n in range(len(sorted_words)): #will use enumerate later on (actually used already), which is faster than range(len()) and then thing[idx]
        word = words[n] #because enumerate is O(N), range(len()) O(N) + O(N) = O(2N) > O(N)
        # Find the index of the word in the original list to get its frequency
        result.append(
            (word, word_count[1][helpers.linear_search(word_count[0], word)]))
    return result  # Return sorted word frequency pairs


def sort_by_frequency(word_count:tuple[list, list]) -> list[tuple[str, int],]:
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
        items_to_sort.append(((item[1], item[0]), i))  # Sort by count first, then word

    # Sort the indices
    sorted_indices = helpers.quick_sort(items_to_sort)  # Sort in descending order

    # Reconstruct the result using the sorted indices
    result = []
    for _, idx in sorted_indices:
        result.append(word_items[idx])

    return result  # Return sorted pairs by frequency


def calculate_similarity(word_count1:tuple[list, list], word_count2:tuple[list, list]) -> tuple[float, float]:
    """
    Calculate the similarity percentage between two texts based on word frequencies.

    Args:
        word_count1 (tuple): Word count data for the first text
        word_count2 (tuple): Word count data for the second text

    Returns:
        tuple of 2 floats: Similarity percentage (0-100) of text1 and text2 respectively

    This function calculates the jaccard(?) similarity of both texts by equation given by teacher
    """
    # Initialize counters
    common_freq = 0  # Frequency of common words (minimum of both texts)
    count1_freq = 0  # Total frequency of text 1
    count2_freq = 0  # Total frequency of text 2

    # Calculate total frequency and find common words
    for idx1, word1 in enumerate(word_count1[0]):
        freq1 = word_count1[1][idx1]
        count1_freq += freq1
        # Check if word exists in second text
        idx2 = helpers.linear_search(word_count2[0], word1)
        if idx2 != -1:
            # Add minimum frequency to common count
            common_freq += helpers.min(freq1, word_count2[1][idx2])

    for freq2 in word_count2[1]:
        count2_freq += freq2

    # Calculate similarity percentage
    # Formula: (total common frequency) / (total frequency) * 100%
    return ((common_freq / count1_freq) * 100 if count1_freq > 0 else 0, 
            (common_freq / count2_freq) * 100 if count2_freq > 0 else 0,)


class WordAnalysisApp:
    """
    GUI application for WAPDS.

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

    # Define theme colors
    LIGHT_THEME = [
        "#f0f0f0",  # bg - light gray background
        "#000000",  # fg - black text
        "#ffffff",  # text_bg - white text background
        "#000000",  # text_fg - black text
        "#e0e0e0",  # button_bg - light gray button background
        "#4a6984",  # highlight_bg - blue highlight background
        "#ffffff",  # highlight_fg - white highlight text
        "#ffffff",  # canvas_bg - white canvas background
        "#f0f0f0",  # frame_bg - light gray frame background
        "#f0f0f0",  # labelframe_bg - light gray labelframe background
        "#f0f0f0"   # tab_bg - light gray tab background
    ]

    DARK_THEME = [
        "#1e1e1e",  # bg - darker background
        "#ffffff",  # fg - white text
        "#2d2d2d",  # text_bg - slightly lighter than bg for text areas
        "#ffffff",  # text_fg - white text
        "#3d3d3d",  # button_bg - medium gray for buttons
        "#0078d7",  # highlight_bg - blue highlight
        "#ffffff",  # highlight_fg - white text on highlight
        "#2d2d2d",  # canvas_bg - same as text_bg for consistency
        "#1e1e1e",  # frame_bg - same as bg
        "#1e1e1e",  # labelframe_bg - same as bg
        "#2d2d2d"   # tab_bg - slightly lighter for tabs
    ]



    def __init__(self, root:tk.Tk, size:str):
        """
        Initialize the application with the tkinter root window.

        Args:
            root: Tkinter root window
            size (str): Window size in format "{width}x{height}"

        This constructor sets up the main window, creates the tabbed interface,
        and initializes all UI components and variables.
        """
        
        def save_window_size(event):
            """Save the current window size when the window is resized."""
            self.window_size = f"{event.width}x{event.height}"
        
        def exit_GUI():
            """
            Exit the GUI application with a confirmation dialog.

            This function prompts the user with a message box asking for confirmation
            before quitting the application and thanking them for using it.
            """
            # Ask user for confirmation to quit
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                # Save window size before exiting
                if self.window_size is not None:
                    config.window_size = self.window_size
                    config.save()
                root.bind("<Configure>", lambda:None)
                messagebox.showwarning("Thank you, app closing...", message="Thank you for using WAPDS")  # Thank you message :)
                root.destroy()  # Destroy the root window to close the application
                exit()  # Close the terminal / exit the program too
        
    
        self.root = root  # Set root window
        self.root.title("Word Analysis and Plagiarism Detection")  # Set window title
        self.window_size = None  # Initialize window size tracking variable
        self.root.geometry(size)  # Set window size defined by the user
        # Configure window close behavior to confirm exit
        root.protocol("WM_DELETE_WINDOW", exit_GUI)  # Set exit protocol to use custom exit function
        root.bind("<Configure>", save_window_size)  # Bind window resize event to save size
        
        # Create theme toggle button (created before notebook so the theme toggle is always visible when window size is too small)
        self.theme_frame = ttk.Frame(root)
        self.theme_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 5))
        
        # Create dark mode toggle checkbox
        self.theme_var = tk.BooleanVar(value=config.dark_mode)
        self.theme_toggle = ttk.Checkbutton(
            self.theme_frame, 
            text="Dark Mode", 
            variable=self.theme_var,
            command=self.toggle_theme
        )
        self.theme_toggle.pack(side=tk.RIGHT)

        # Create the main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Variables to store file paths and analysis results
        self.file_path1 = ""
        self.file_path2 = ""
        self.word_count1 = None
        self.word_count2 = None
        self.clean_content1 = ""
        self.clean_content2 = ""

        # Create style for the application
        self.style = ttk.Style()
        
        # Create tabs for various functionalities
        self.create_analyze_tab()  # Tab for analyzing single file
        self.create_compare_tab()  # Tab for comparing two files
        self.create_search_tab()   # Tab for searching words in a file
        self.create_replace_tab()  # Tab for replacing words in a file
        self.create_config_tab()   # Tab for configuring settings
        
        # Apply the current theme
        self.apply_theme()

    def apply_theme(self):
        """
        Apply the current theme to all UI elements.
        
        This method configures all widgets with the appropriate colors and styles
        based on whether dark mode is enabled or not.
        """
        theme = self.DARK_THEME if config.dark_mode else self.LIGHT_THEME
        
        # Configure the ttk styles properly
        self.style.theme_use("default")  # Reset to default theme first
        
        # Configure styles for ttk widgets
        self.style.configure("TFrame", background=theme[8])
        self.style.configure("TLabelframe", background=theme[9])
        self.style.configure("TLabelframe.Label", background=theme[9], foreground=theme[1],
                             font=("Arial", config.text_font_size))
        
        # Configure Notebook and Tab styles
        self.style.configure("TNotebook", background=theme[0])
        self.style.map("TNotebook.Tab", 
                    background=[("selected", theme[5]), ("!selected", theme[10])],
                    foreground=[("selected", theme[6]), ("!selected", theme[1])])
        
        # Configure Button style
        self.style.configure("TButton", 
                            background=theme[4], 
                            foreground=theme[1],
                            font=("Arial", config.text_font_size))
        self.style.map("TButton",
                    background=[("active", theme[5])],
                    foreground=[("active", theme[6])])
        
        # Configure Entry style
        self.style.configure("TEntry", 
                            fieldbackground=theme[2], 
                            foreground=theme[3],
                            insertcolor=theme[1],
                            font=("Arial", config.text_font_size))  # Cursor color
        
        # Configure Checkbutton style
        self.style.configure("TCheckbutton", 
                            background=theme[8], 
                    foreground=theme[1],
                    selectcolor=theme[2])
        self.style.map("TCheckbutton",
                    background=[("active", theme[8])],
                    foreground=[("active", theme[1])])
        
        # Configure Label style
        self.style.configure("TLabel", 
                            background=theme[8], 
                            foreground=theme[1],
                            font=("Arial", config.text_font_size))
        
        # Configure root and main frames
        self.root.configure(background=theme[0])
        
        # Update all widgets recursively
        self._update_widget_colors(self.root, theme)
        
        # If matplotlib is available, update the graph style
        if plt is not None:
            plt.style.use("dark_background" if config.dark_mode else "default")
            
            # Redraw graphs if they exist
            if hasattr(self, "word_count1") and self.word_count1:
                self.create_frequency_graph(self.word_count1, self.analyze_graph_frame, self.analyze_canvas)
                
            if hasattr(self, "word_count1") and hasattr(self, "word_count2") and self.word_count1 and self.word_count2:
                self.create_comparison_graph(self.word_count1, self.word_count2, self.compare_graph_frame, self.compare_canvas)

    def _update_widget_colors(self, widget, theme):
        """
        Recursively update colors for all widgets.
        
        Args:
            widget: The widget to update
            theme: The theme colors to apply
            
        This helper method traverses the widget hierarchy and applies
        appropriate theme colors to each widget based on its type.
        """
        widget_class = widget.__class__.__name__
        
        # Handle standard tkinter widgets (not ttk)
        if widget_class == "Text":
            widget.configure(
                background=theme[2],
                foreground=theme[3],
                insertbackground=theme[1],  # Cursor color
                selectbackground=theme[5],
                selectforeground=theme[6],
                font=("Arial", config.text_font_size)
            )
        elif widget_class == "Listbox":
            widget.configure(
                background=theme[2],
                foreground=theme[3],
                selectbackground=theme[5],
                selectforeground=theme[6],
                font=("Arial", config.text_font_size)
            )
        elif widget_class == "Canvas":
            widget.configure(background=theme[7])
        elif widget_class == "Label":
            widget.configure(background=theme[8], foreground=theme[1], font=("Arial", config.text_font_size))
        elif widget_class == "LabelFrame":
            widget.configure(background=theme[9], foreground=theme[1], font=("Arial", config.text_font_size))
        
        # Recursively update all children
        for child in widget.winfo_children():
            self._update_widget_colors(child, theme)

    def toggle_theme(self):
        """
        Toggle between light and dark themes.
        
        This method updates the config setting, saves it, and applies
        the new theme to all UI elements.
        """
        config.dark_mode = self.theme_var.get()
        config.save()
        self.apply_theme()
        
        # If matplotlib is available, update the graph style
        if plt is not None:
            plt.style.use("dark_background" if config.dark_mode else "default")
            
            # Redraw graphs if they exist
            if hasattr(self, "word_count1") and self.word_count1:
                self.create_frequency_graph(self.word_count1, self.analyze_graph_frame, self.analyze_canvas)
                
            if hasattr(self, "word_count1") and hasattr(self, "word_count2") and self.word_count1 and self.word_count2:
                self.create_comparison_graph(self.word_count1, self.word_count2, self.compare_graph_frame, self.compare_canvas)

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

        self.analyze_graph_frame = ttk.LabelFrame(right_frame, text="Word Frequency Graph")
        self.analyze_graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Canvas to draw the frequency graph
        self.analyze_canvas = tk.Canvas(self.analyze_graph_frame)
        self.analyze_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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
        
        def update_file_labels():
            """
            Update file labels based on whether NLTK is enabled.
            
            When NLTK is enabled:
            - File 1 becomes "File"
            - File 2 becomes "Reference Files"
            Otherwise, they remain as "File 1" and "File 2"
            """
            if self.compare_nltk.get():
                self.file1_label.config(text="File:")
                self.file2_label.config(text="Reference Files:")
                self.file1_stats_frame.config(text="File Statistics")
                self.file2_stats_frame.config(text="Reference Files Statistics")
                # Change browse behavior for file 2 to allow multiple files
                browse_btn2.config(command=self.browse_compare_file2_nltk)
            else:
                self.file1_label.config(text="File 1:")
                self.file2_label.config(text="File 2:")
                self.file1_stats_frame.config(text="File 1 Statistics")
                self.file2_stats_frame.config(text="File 2 Statistics")
                # Change browse behavior back to single file
                browse_btn2.config(command=self.browse_compare_file2)
            
        
        compare_tab = ttk.Frame(self.notebook)  # Create compare tab frame
        self.notebook.add(compare_tab, text="Compare Files")  # Add to notebook

        # File selection frame
        files_frame = ttk.Frame(compare_tab)
        files_frame.pack(fill=tk.X, pady=10)

        # File 1 selection
        file1_frame = ttk.Frame(files_frame)
        file1_frame.pack(fill=tk.X, pady=5)

        self.file1_label = ttk.Label(file1_frame, text="File 1:")
        self.file1_label.pack(side=tk.LEFT, padx=5)  # Label for File 1 selection
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

        self.file2_label = ttk.Label(file2_frame, text="File 2:")
        self.file2_label.pack(side=tk.LEFT, padx=5)  # Label for File 2 selection
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
        
        # More buttons
        buttons_frame = ttk.Frame(files_frame)
        buttons_frame.pack(fill=tk.X, pady=5)

        # Button to perform comparison
        compare_btn = ttk.Button(buttons_frame,
                                text="Compare Files",
                                command=self.compare_files)
        compare_btn.pack(side=tk.TOP, pady=10)
        # Add NLTK checkbox
        self.compare_nltk = tk.BooleanVar(value=False)
        use_nltk = ttk.Checkbutton(buttons_frame, 
                                    text="Use cosine similarity", 
                                    variable=self.compare_nltk,
                                    command=update_file_labels)
        use_nltk.pack(side=tk.RIGHT, padx=5)

        # Results section for displaying statistics and comparison results
        results_frame = ttk.Frame(compare_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Left side - stats and comparison display
        left_frame = ttk.Frame(results_frame)   
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        lists_frame = ttk.Frame(left_frame)  # Frame for statistics lists
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # File 1 stats display
        self.file1_stats_frame = ttk.LabelFrame(lists_frame, text="File 1 Statistics")
        self.file1_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Text area for displaying statistics of File 1
        self.file1_stats_text = tk.Text(self.file1_stats_frame,
                                        height=5,
                                        width=40,
                                        wrap=tk.WORD)  
        self.file1_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # File 2 stats display
        self.file2_stats_frame = ttk.LabelFrame(lists_frame, text="File 2 Statistics")
        self.file2_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Text area for displaying statistics of File 2
        self.file2_stats_text = tk.Text(self.file2_stats_frame,
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
        self.compare_graph_frame = ttk.LabelFrame(right_frame, text="Word Frequency Comparison")
        self.compare_graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Canvas to draw the comparison graph
        self.compare_canvas = tk.Canvas(self.compare_graph_frame)
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
        self.search_file_entry.pack(side=tk.LEFT,
                                    padx=5,
                                    fill=tk.X,
                                    expand=True)

        browse_btn = ttk.Button(file_frame,
                                text="Browse",
                                command=self.browse_search_file)
        browse_btn.pack(side=tk.LEFT, padx=5)

        # Search frame
        search_frame = ttk.Frame(search_tab)
        search_frame.pack(fill=tk.X, pady=10)

        ttk.Label(search_frame, text="Search for:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Add regex checkbox
        self.regex_var = tk.BooleanVar(value=False)
        regex_check = ttk.Checkbutton(search_frame, 
                                    text="Use Regex", 
                                    variable=self.regex_var)
        regex_check.pack(side=tk.LEFT, padx=5)

        search_btn = ttk.Button(search_frame,
                                text="Search",
                                command=self.search_word)
        search_btn.pack(side=tk.LEFT, padx=5)

        # Results frame
        results_frame = ttk.LabelFrame(search_tab, text="Search Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        self.search_results = tk.Text(results_frame, wrap=tk.WORD)
        self.search_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.search_results.config(state=tk.DISABLED)  # Make the text read-only

    def create_replace_tab(self):
        """Create the Replace tab for word replacement."""
        replace_tab = ttk.Frame(self.notebook)
        self.notebook.add(replace_tab, text="Replace Word")

        # File selection
        file_frame = ttk.Frame(replace_tab)
        file_frame.pack(fill=tk.X, pady=10)

        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.replace_file_entry = ttk.Entry(file_frame, width=50)
        self.replace_file_entry.pack(side=tk.LEFT,
                                    padx=5,
                                    fill=tk.X,
                                    expand=True)

        browse_btn = ttk.Button(file_frame,
                                text="Browse",
                                command=self.browse_replace_file)
        browse_btn.pack(side=tk.LEFT, padx=5)

        # Replace frame
        replace_frame = ttk.Frame(replace_tab)
        replace_frame.pack(fill=tk.X, pady=10)

        # Word to replace
        word_frame = ttk.Frame(replace_frame)
        word_frame.pack(fill=tk.X, pady=5)

        ttk.Label(word_frame, text="Text to replace:").pack(side=tk.LEFT, padx=5)
        self.word_entry = ttk.Entry(word_frame, width=30)
        self.word_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Add regex checkbox
        self.replace_regex_var = tk.BooleanVar(value=False)
        regex_check = ttk.Checkbutton(word_frame, 
                                    text="Use Regex", 
                                    variable=self.replace_regex_var)
        regex_check.pack(side=tk.LEFT, padx=5)

        # Replacement word
        replacement_frame = ttk.Frame(replace_frame)
        replacement_frame.pack(fill=tk.X, pady=5)

        ttk.Label(replacement_frame,
                text="Replacement text:").pack(side=tk.LEFT, padx=5)
        self.replacement_entry = ttk.Entry(replacement_frame, width=30)
        self.replacement_entry.pack(side=tk.LEFT,
                                    padx=5,
                                    fill=tk.X,
                                    expand=True)

        replace_btn = ttk.Button(replace_frame,
                                text="Replace",
                                command=self.replace_word)
        replace_btn.pack(pady=5)

        # Text display frames
        text_frame = ttk.Frame(replace_tab)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Original text
        original_frame = ttk.LabelFrame(text_frame, text="Original Text")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.original_text = tk.Text(original_frame, wrap=tk.WORD)
        self.original_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.original_text.config(state=tk.DISABLED)  # Make the text read-only

        # Modified text
        modified_frame = ttk.LabelFrame(text_frame, text="Modified Text")
        modified_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.modified_text = tk.Text(modified_frame, wrap=tk.WORD)
        self.modified_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Save button
        save_frame = ttk.Frame(replace_tab)
        save_frame.pack(fill=tk.X, pady=10)

        save_btn = ttk.Button(save_frame,
                            text="Save Modified Text",
                            command=self.save_modified_text)
        save_btn.pack()


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

        # Label and entry for text font size
        ttk.Label(font_frame, text="Text font size:").pack(side=tk.LEFT, padx=5)
        self.text_font_size_var = tk.StringVar(value=str(config.text_font_size))  # Bind entry with current value
        self.text_font_entry = ttk.Entry(font_frame, width=5, textvariable=self.text_font_size_var)
        self.text_font_entry.pack(side=tk.LEFT, padx=5)

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
    
    def browse_compare_file2_nltk(self):
        """
        Open a file dialog to browse for the a set of reference files to compare.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilenames(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):  # Open dialog for file selection
            self.compare_file_entry2.delete(0, tk.END)  # Clear entry
            for file in file_path[:-1]:
                self.compare_file_entry2.insert(tk.END, file.replace(",", ",\\")+", ")  # Insert selected path
            self.compare_file_entry2.insert(tk.END, file_path[-1].replace(",", ",\\"))
            
    def browse_search_file(self):
        """Browse for a file to search."""
        if file_path := filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):
            self.search_file_entry.delete(0, tk.END)
            self.search_file_entry.insert(0, file_path)

    def browse_replace_file(self):
        """Browse for a file to perform word replacement."""
        if file_path := filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]):
            self.replace_file_entry.delete(0, tk.END)
            self.replace_file_entry.insert(0, file_path)


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
            self.freq_list.insert(tk.END, f'{i + 1}. "{word}": {count} times')  # Insert words and counts

        self.alpha_list.delete(0, tk.END)  # Clear previous alphabetical list
        alpha_sorted = sort_alphabetically(word_count)[:config.analyze_max_words]  # Get sorted alphabetical list
        for i, (word, count) in enumerate(alpha_sorted):  # Iterate through sorted list
            self.alpha_list.insert(tk.END, f'{i + 1}. "{word}": {count} times')  # Insert words and counts

        # Create and display the frequency graph
        self.create_frequency_graph(word_count, self.analyze_canvas, self.analyze_canvas)  # Draw graph for the current file

        # Store data for later use
        self.word_count1 = word_count  # Store word count data
        self.clean_content1 = clean_content  # Store cleaned content

    def create_frequency_graph(self, word_count, canvas_frame_widget, canvas_widget, max_words=config.graph_max_words):
        """
        Create a bar graph of word frequencies.

        Args:
            word_count (tuple): Word count data
            canvas_frame_widget: Tkinter frame that holds the canvas
            canvas_widget: Tkinter canvas to display the graph
            max_words (int): Maximum number of words to display in the graph
        """
        if plt is None:
            return
        
        # Clear previous graph
        for widget in canvas_widget.winfo_children():
            widget.destroy()
        plt.close()
            
        for widget in canvas_frame_widget.winfo_children():
            if widget.winfo_id() != canvas_widget.winfo_id():
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
        ax.set_xlabel("Frequency", fontsize=config.graph_label_fontsize)  # X-axis label
        ax.set_title("Top Word Frequencies", fontsize=config.graph_title_fontsize)  # Graph title
        ax.tick_params(labelsize=config.graph_label_fontsize)  # Set tick params for labels

        # Add count labels on bars
        for bar in bars:
            width = bar.get_width()  # Get bar width
            ax.text(width + 0.5,
                    bar.get_y() + bar.get_height() / 2,
                    f"{width}",
                    ha="left",
                    va="center")  # Display count on bar

        plt.tight_layout()  # Adjust layout
        # Embed the graph in the canvas
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)  # Create canvas for matplotlib figure
        canvas.draw()  # Draw the figure
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Pack canvas into the Tkinter widget
        
        # Add navigation toolbar for panning, zooming, etc.
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame_widget)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add vertical scrollbar if needed
        if len(words) > 10:  # Only add scrollbar if there are many words
            scrollbar = ttk.Scrollbar(canvas_widget, orient=tk.VERTICAL, command=canvas_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas_widget.configure(yscrollcommand=scrollbar.set)


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

        # Read and process the first file
        content1 = read_file(file_path1)  # Read first file content
        if content1 is None:  # Check if reading was successful
            messagebox.showerror("Error", f"Could not read file: {file_path1}")  # Show error message
            return  # Exit method on error
        if self.compare_nltk.get() and get_similarity_score is None:
            self.compare_nltk.set(False)
            print("\x1b[33mWarning: some required modules in nltk_plagiarism module is missing, or is corrupted. Please (re)install the necesserary modules by running `python -m pip install nltk scikit-learn` in the terminal\x1b[m")  #Show error message
            messagebox.showerror("Error", "there are some errors trying to use cosine similarity (nltk), jaccard(?) similarity is used instead. Please refer to the error message in the terminal")  # Show more error message

        # Process differently based on whether NLTK is enabled
        if self.compare_nltk.get():
            # Handle NLTK-based comparison with multiple reference files
            file_paths = []
            for file in file_path2.split(", "):
                if file:
                    file_paths.append(file.replace(",\\", ","))
            
            # Read all reference files
            reference_contents = []
            reference_file_names = []
            for path in file_paths:
                content = read_file(path)
                if content is None:
                    messagebox.showerror("Error", f"Could not read file: {path}")
                    return
                reference_contents.append(content)
                reference_file_names.append(os.path.basename(path))
            
            # Display statistics for file 1
            clean_content1 = clean_text(content1)
            word_count1 = count_words(clean_content1)
            total_words1 = len(clean_content1.split(" "))
            unique_words1 = len(word_count1[0])
            
            self.file1_stats_text.delete(1.0, tk.END)
            self.file1_stats_text.insert(tk.END, f"File: {os.path.basename(file_path1)}\n")
            self.file1_stats_text.insert(tk.END, f"Total words: {total_words1}\n")
            self.file1_stats_text.insert(tk.END, f"Unique words: {unique_words1}\n")
            
            # Display statistics for reference files
            self.file2_stats_text.delete(1.0, tk.END)
            self.file2_stats_text.insert(tk.END, f"Reference Files: {len(file_paths)}\n")
            
            total_words2 = 0
            unique_words = []
            
            # Process each reference file
            reference_word_counts = []
            for i, content in enumerate(reference_contents):
                clean_content = clean_text(content)
                word_count = count_words(clean_content)
                reference_word_counts.append(word_count)
                
                words = clean_content.split(" ")
                total_words2 += len(words)
                for word in word_count[0]:
                    if word not in unique_words:
                        unique_words.append(word)
                
                self.file2_stats_text.insert(tk.END, f"File {i+1}: {reference_file_names[i]}\n")
            
            self.file2_stats_text.insert(tk.END, f"Total words across all files: {total_words2}\n")
            self.file2_stats_text.insert(tk.END, f"Unique words across all files: {len(unique_words)}\n")
            
            # Use NLTK for plagiarism detection
            plagiarism_results = get_similarity_score(content1, reference_contents)
            
            # Display results
            self.comparison_text.delete(1.0, tk.END)
            
            # Prepare similarity scores for all reference files
            similarity_scores = [0] * len(reference_contents)
            
            if plagiarism_results:
                # Found plagiarism
                max_similarity = helpers.max(result[1] for result in plagiarism_results)
                similarity = max_similarity * 100  # Convert to percentage
                
                self.comparison_text.insert(tk.END, f"Similarity percentage: {similarity:.2f}%\n\n")
                
                # List all matches
                self.comparison_text.insert(tk.END, "Matches found in:\n")
                for i, result in enumerate(plagiarism_results):
                    score = result[1] * 100
                    # Find which reference file this match corresponds to
                    match_index = helpers.linear_search(reference_contents, result[0])
                    file_name = reference_file_names[match_index]
                    similarity_scores[match_index] = score  # Store score for this reference file
                    
                    self.comparison_text.insert(tk.END, f"Match {i+1}: {file_name} - {score:.2f}% similarity\n")
            else:
                # No plagiarism detected
                similarity = 0
                self.comparison_text.insert(tk.END, "No significant similarity detected\n\n")
                self.comparison_text.insert(tk.END, "Similarity percentage: 0.00%\n")
            
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

            self.comparison_text.insert(tk.END, f"\nPlagiarism Level: {level}", "color")
            
            # Create a specialized NLTK-based comparison graph for all reference files
            if reference_word_counts:
                self.create_nltk_comparison_graph(
                    word_count1, 
                    reference_word_counts,
                    os.path.basename(file_path1), 
                    reference_file_names,
                    similarity_scores, 
                    self.compare_graph_frame, 
                    self.compare_canvas
                )
            
        else:
            # Standard comparison between two files
            content2 = read_file(file_path2)  # Read second file content
            if content2 is None:  # Check if reading was successful
                messagebox.showerror("Error", f"Could not read file: {file_path2}")  # Show error message
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

            # Calculate similarity using standard method
            similarity = calculate_similarity(word_count1, word_count2)  # Calculate similarity percentage

            self.comparison_text.delete(1.0, tk.END)  # Clear previous comparison results
            self.comparison_text.insert(tk.END, f"Similarity percentage of\ntext 1: {similarity[0]:.2f}%\ntext 2: {similarity[1]:.2f}%\n\n")  # Display similarity percentage

            # Determine plagiarism level based on similarity percentage
            similarity = helpers.max(similarity)
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

            self.comparison_text.insert(tk.END, f"Plagiarism Level: {level}", "color")  # Display plagiarism level
            
            # Create comparison graph
            self.create_comparison_graph(word_count1, word_count2, self.compare_graph_frame, self.compare_canvas)  # Draw graph for comparisons




    def create_comparison_graph(self, word_count1, word_count2, canvas_frame_widget, canvas_widget, max_words=config.graph_max_words):
        """
        Create a comparison graph of word frequencies between two files.

        Args:
            word_count1 (tuple): Word count data for the first file
            word_count2 (tuple): Word count data for the second file
            canvas_frame_widget: Tkinter frame that holds the canvas
            canvas_widget: Tkinter canvas to display the graph
            max_words (int): Maximum number of words to display from each file
        """
        if plt is None:
            return
        
        # Clear previous graph
        for widget in canvas_widget.winfo_children():
            widget.destroy()
        plt.close()
            
        for widget in canvas_frame_widget.winfo_children():
            if widget.winfo_id() != canvas_widget.winfo_id():
                widget.destroy()
            
        # Get top words from both files
        freq_sorted1 = sort_by_frequency(word_count1)  # Sort word counts from first file
        freq_sorted2 = sort_by_frequency(word_count2)  # Sort word counts from second file

        # Create sets of top words for both files
        combined_top_words = []
        top_words1 = []
        for word, _ in freq_sorted1[:max_words]: # Extract top words for first file
            if word not in top_words1:
                top_words1.append(word)
        for word, _ in freq_sorted2[:max_words]: # Extract top words for second file
            if word in top_words1 and word not in combined_top_words:
                combined_top_words.append(word)


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
        ax.bar([i - width / 2 for i in x], counts1, width, label="File 1", color=config.graph_bar_color_compare1)  # Bars for first file
        ax.bar([i + width / 2 for i in x], counts2, width, label="File 2", color=config.graph_bar_color_compare2)  # Bars for second file

        # Add labels and legend
        ax.set_ylabel("Frequency")  # Y-axis label
        ax.set_title("Word Frequency Comparison")  # Graph title
        ax.set_xticks(x)  # Set positions for x-ticks
        ax.set_xticklabels(combined_top_words, rotation=45, ha="right")  # Set labels for x-ticks
        ax.legend()  # Display legend

        plt.tight_layout()  # Adjust layout for better spacing
        # Embed the graph in the canvas
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)  # Create canvas for matplotlib figure
        canvas.draw()  # Draw the figure
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Pack canvas into the Tkinter widget
        
        # Add navigation toolbar for panning, zooming, etc.
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame_widget)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add vertical scrollbar if needed
        if len(combined_top_words) > 10:  # Only add scrollbar if there are many words
            scrollbar = ttk.Scrollbar(canvas_widget, orient=tk.VERTICAL, command=canvas_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas_widget.configure(yscrollcommand=scrollbar.set)

        
        
    def create_nltk_comparison_graph(self, word_count1, reference_word_counts, file1_name, reference_file_names, 
                                    similarity_scores, canvas_frame_widget, canvas_widget, max_words=config.graph_max_words):
        """
        Create a specialized comparison graph for NLTK-based plagiarism detection showing all reference files.

        Args:
            word_count1 (tuple): Word count data for the first file
            reference_word_counts (list): List of word count data for all reference files
            file1_name (str): Name of the first file
            reference_file_names (list): Names of all reference files
            similarity_scores (list): List of similarity scores for each reference file
            canvas_frame_widget: Tkinter frame that holds the canvas
            canvas_widget: Tkinter canvas to display the graph
            max_words (int): Maximum number of words to display from each file
        """
        if plt is None:
            return


        # Clear previous graph
        for widget in canvas_widget.winfo_children():
            widget.destroy()
        plt.close()
            
        for widget in canvas_frame_widget.winfo_children():
            if widget.winfo_id() != canvas_widget.winfo_id():
                widget.destroy()
        
        # Get top words from the query file
        freq_sorted1 = sort_by_frequency(word_count1)
        top_words1 = []
        for word, _ in freq_sorted1[:max_words]:
            if word not in top_words1:
                top_words1.append(word)

        # Find common words across all files
        all_common_words = []
        for word_count2 in reference_word_counts:
            freq_sorted2 = sort_by_frequency(word_count2)
            for word, _ in freq_sorted2[:max_words]:
                if word in top_words1 and word not in all_common_words:
                    all_common_words.append(word)
        
        # If no common words found across any files
        if not all_common_words:
            fig = plt.figure(figsize=config.graph_figsize)
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, "No common words found in top frequency lists", 
                    ha="center", va="center", fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.tight_layout()
            
            # Create a frame to hold the canvas
            frame = ttk.Frame(canvas_widget)
            frame.pack(fill=tk.BOTH, expand=True)
            
            # Embed the graph in the canvas
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            return
        
        # Sort common words by frequency in the first file
        all_common_words_sorted = helpers.quick_sort(all_common_words, 
                                        key=lambda word: word_count1[1][helpers.linear_search(word_count1[0], word)] 
                                        if word in word_count1[0] else 0,
                                        reverse=True)
        
        # Limit to a reasonable number of words to keep the graph readable
        # For multiple reference files, we need to be more selective
        display_words = all_common_words_sorted[:max_words]
        
        # Create a figure with enough height for all reference files
        fig_height = helpers.max(config.graph_figsize[1], 2 + len(reference_word_counts) * 0.5)
        fig = plt.figure(figsize=(config.graph_figsize[0], fig_height))
        
        # Create a grid of subplots - one for each reference file
        num_plots = len(reference_word_counts)
        
        # If there are too many reference files, limit the display
        if num_plots > 10:
            # Sort reference files by similarity score and take top 10
            indices = helpers.quick_sort(range(len(similarity_scores)), key=lambda i: similarity_scores[i], reverse=True)[:10]
            reference_word_counts = [reference_word_counts[i] for i in indices]
            reference_file_names = [reference_file_names[i] for i in indices]
            similarity_scores = [similarity_scores[i] for i in indices]
            num_plots = 10
        
        # Create subplots
        for i in range(num_plots):
            ax = fig.add_subplot(num_plots, 1, i+1)
            
            # Get counts for the query file and this reference file
            counts1 = []
            counts2 = []
            
            for word in display_words:
                # Get count in the query file
                if word in word_count1[0]:
                    idx = helpers.linear_search(word_count1[0], word)
                    counts1.append(word_count1[1][idx])
                else:
                    counts1.append(0)
                    
                # Get count in this reference file
                word_count2 = reference_word_counts[i]
                if word in word_count2[0]:
                    idx = helpers.linear_search(word_count2[0], word)
                    counts2.append(word_count2[1][idx])
                else:
                    counts2.append(0)
            
            # Create bar chart for common words
            x = range(len(display_words))
            width = 0.35
            
            ax.bar([j - width/2 for j in x], counts1, width, label=file1_name, color=config.graph_bar_color_compare1)
            ax.bar([j + width/2 for j in x], counts2, width, 
                label=f"{reference_file_names[i]} ({similarity_scores[i]:.1f}%)", 
                color=config.graph_bar_color_compare2)
            
            # Add labels and legend
            if i == 0:  # Only add title to the first subplot
                ax.set_title("Word Frequency Comparison with Reference Files")
            
            # Add y-label only to the middle subplot to save space
            if i == num_plots // 2:
                ax.set_ylabel("Frequency")
            
            # Add x-labels only to the last subplot
            if i == num_plots - 1:
                ax.set_xticks(x)
                ax.set_xticklabels(display_words, rotation=45, ha="right")
            else:
                ax.set_xticks(x)
                ax.set_xticklabels([])
            
            ax.legend(loc="upper right", fontsize="small")
        
        plt.tight_layout()
        # Embed the graph in the canvas
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)  # Create canvas for matplotlib figure
        canvas.draw()  # Draw the figure
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Pack canvas into the Tkinter widget
        
        # Add navigation toolbar for panning, zooming, etc.
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame_widget)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add vertical scrollbar for multiple plots
        scrollbar = ttk.Scrollbar(canvas_widget, orient=tk.VERTICAL, command=canvas_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_widget.configure(yscrollcommand=scrollbar.set)
        
        # Add horizontal scrollbar if needed
        if len(display_words) > 10:
            h_scrollbar = ttk.Scrollbar(canvas_widget, orient=tk.HORIZONTAL, command=canvas_widget.xview)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            canvas_widget.configure(xscrollcommand=h_scrollbar.set)


        
    def search_word(self):
        """
        Search for a word or pattern in the selected file and highlight occurrences.
        
        This method:
        1. Gets the file path and target word from input fields
        2. Reads the file content (preserving original formatting)
        3. Finds all occurrences of the target word or pattern
        4. Displays the results with highlighted context
        
        The search supports both exact word matching and regular expressions,
        with results showing the original text with punctuation preserved.
        """
        file_path = self.search_file_entry.get()  # Get file path from entry
        target_word = self.search_entry.get()  # Get search word/pattern from entry
        
        # Check if regex checkbox is selected
        regex = self.regex_var.get()

        # Validate inputs - ensure both file path and search term are provided
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        if not target_word:
            messagebox.showerror("Error", "Please enter a word or pattern to search for.")
            return

        # Read file content
        content = read_file(file_path)
        if content is None:
            messagebox.showerror("Error", f"Could not read file: {file_path}")
            return

        # Find word positions in original text using the search helper function
        positions = search_word_position(content, target_word, regex)

        # Clear previous results and prepare text widget for new content
        self.search_results.config(state=tk.NORMAL)  # Make the text updatable
        self.search_results.delete(1.0, tk.END)

        if positions:
            # Display summary of occurrences at the top of results
            match_text = "pattern" if regex else "word"
            self.search_results.insert(
                tk.END,
                f'The {match_text} "{target_word}" appears {len(positions)} times\n\n'
            )

            # Configure tag for highlighting the target word with yellow background
            self.search_results.tag_configure("highlight", background="yellow", foreground="black")

            # Show each occurrence in context with surrounding words
            words = content.split()
            for pos, matched_word in positions:
                # Get a window of words around the occurrence (3 words before, 3 words after)
                start = helpers.max(0, pos - 3)  # Ensure we don"t go below index 0
                end = helpers.min(len(words), pos + 4)  # Ensure we don"t exceed array bounds

                # Create context with ellipses if needed to show this is a snippet
                prefix = "... " if pos > 3 else ""  # Add ellipsis if we"re not at the beginning
                suffix = " ..." if pos + 4 < len(words) else ""  # Add ellipsis if we"re not at the end

                # Insert position number and prefix
                self.search_results.insert(tk.END, f"Position {pos}: {prefix}")

                # Insert words before target with normal formatting
                if start < pos:
                    self.search_results.insert(tk.END, " ".join(words[start:pos]) + " ")

                # Insert target word with highlighting (yellow background)
                self.search_results.insert(tk.END, matched_word, "highlight")

                # Insert words after target with normal formatting
                if pos + 1 < end:
                    self.search_results.insert(tk.END, " " + " ".join(words[pos+1:end]))

                # Add suffix and newline for readability
                self.search_results.insert(tk.END, f"{suffix}\n")
        else:
            # No matches found - inform the user
            match_text = "pattern" if regex else "word"
            self.search_results.insert(tk.END, f'The {match_text} "{target_word}" was not found in the file.')
        
        # Make the text read-only again to prevent user edits
        self.search_results.config(state=tk.DISABLED)

    def replace_word(self):
        """
        Replace occurrences of a word or pattern in the selected file.

        This method:
        1. Gets the file path, target word/pattern, and replacement word
        2. Reads the file content (preserving original formatting)
        3. Replaces all occurrences of the target
        4. Displays both original and modified text with highlighting

        The replacement preserves the original text formatting including
        newlines, punctuation and capitalization where appropriate, and 
        highlights the modified parts in the result.
        """
        # Get input values from UI fields
        file_path = self.replace_file_entry.get()  # Path to the file
        target_word = self.word_entry.get()  # Word/pattern to replace
        replacement_word = self.replacement_entry.get()  # Replacement text

        # Check if regex checkbox is selected for pattern matching
        regex = self.replace_regex_var.get()

        # Validate inputs - ensure file path and target word are provided
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        if not target_word:
            messagebox.showerror("Error", "Please enter a word or pattern to replace.")
            return

        # Read file content using the helper function
        content = read_file(file_path)
        if content is None:
            messagebox.showerror("Error", f"Could not read file: {file_path}")
            return

        # Prepare text widgets for displaying content
        self.original_text.config(state=tk.NORMAL)  # Make the original text updatable
        
        # Configure tags for highlighting the replacements in both text widgets
        self.modified_text.tag_configure("highlight", background="yellow", foreground="black")
        self.original_text.tag_configure("highlight", background="yellow", foreground="black")
        
        # Clear both text widgets
        self.modified_text.delete(1.0, tk.END)
        self.original_text.delete(1.0, tk.END)

        # Perform replacement based on whether regex is enabled
        if regex:
            try:
                # For regex pattern matching, use re.finditer to find all matches
                matches = list(re.finditer(target_word, content, flags=re.IGNORECASE))
                
                if matches:
                    # Track position of last match to continue from
                    last_end = 0
                    for match in matches:
                        # Insert text before the match (unchanged)
                        self.original_text.insert(tk.END, content[last_end:match.start()])
                        self.modified_text.insert(tk.END, content[last_end:match.start()])
                        
                        # Insert original text with highlighting in original view
                        self.original_text.insert(tk.END, content[match.start():match.end()], "highlight")
                        # Insert replacement with highlighting in modified view
                        self.modified_text.insert(tk.END, replacement_word, "highlight")
                        
                        # Update position tracker
                        last_end = match.end()
                    
                    # Insert remaining text after the last match
                    self.original_text.insert(tk.END, content[last_end:])
                    self.modified_text.insert(tk.END, content[last_end:])
                else:
                    # No matches found, just display the original content in both views
                    self.original_text.insert(tk.END, content)
                    self.modified_text.insert(tk.END, content)
            except re.error:
                # Handle invalid regex pattern error
                messagebox.showerror("Error", "Invalid regular expression pattern.")
                return
        else:
            # For exact word matching, process line by line to preserve formatting
            # Split content by lines to preserve newlines
            lines = content.split("\n")
            
            # Process each line separately
            for i, line in enumerate(lines):
                # Handle empty lines
                if not line.strip():  # Preserve empty lines
                    if i > 0:  # Don"t add newline before the first line
                        self.original_text.insert(tk.END, "\n")
                        self.modified_text.insert(tk.END, "\n")
                    continue
                    
                # Split line into words for processing
                words = line.split()
                
                # Handle lines with only whitespace
                if not words:  # Empty line with whitespace
                    if i > 0:
                        self.original_text.insert(tk.END, "\n")
                        self.modified_text.insert(tk.END, "\n")
                    continue
                    
                # Find all occurrences of the target word in this line
                positions = []
                for idx, word in enumerate(words):
                    # Check if this word matches our target (ignoring case and punctuation)
                    clean_word = "".join(c.lower() for c in word if c.isalnum())
                    if clean_word == target_word.lower():
                        positions.append(idx)
                
                # Add a newline before this line if it's not the first line
                if i > 0:
                    self.original_text.insert(tk.END, "\n")
                    self.modified_text.insert(tk.END, "\n")
                    
                if positions:
                    # Process the line with replacements
                    current_pos = 0
                    for pos in positions:
                        # Add text up to this position (unchanged)
                        if pos > current_pos:
                            self.original_text.insert(tk.END, " ".join(words[current_pos:pos]) + " ")
                            self.modified_text.insert(tk.END, " ".join(words[current_pos:pos]) + " ")
                        
                        # Get the original word
                        original_word = words[pos]
                        
                        # Extract leading and trailing punctuation to preserve in replacement
                        leading_punct = ""
                        trailing_punct = ""
                        
                        # Extract leading punctuation (characters at start that aren"t alphanumeric)
                        i = 0
                        while i < len(original_word) and not original_word[i].isalnum():
                            leading_punct += original_word[i]
                            i += 1
                        
                        # Extract trailing punctuation (characters at end that aren"t alphanumeric)
                        i = len(original_word) - 1
                        while i >= 0 and not original_word[i].isalnum():
                            trailing_punct = original_word[i] + trailing_punct
                            i -= 1
                        
                        # Insert the original and replacement with highlighting
                        self.original_text.insert(tk.END, original_word, "highlight")
                        # Preserve punctuation in the replacement
                        self.modified_text.insert(tk.END, leading_punct + replacement_word + trailing_punct, "highlight")
                        
                        # Add a space if this isn"t the last word
                        if pos < len(words) - 1:
                            self.original_text.insert(tk.END, " ")
                            self.modified_text.insert(tk.END, " ")
                        
                        # Update position tracker
                        current_pos = pos + 1
                    
                    # Add any remaining text in the line
                    if current_pos < len(words):
                        self.original_text.insert(tk.END, " ".join(words[current_pos:]))
                        self.modified_text.insert(tk.END, " ".join(words[current_pos:]))
                else:
                    # No replacements in this line, keep it as is
                    self.original_text.insert(tk.END, line)
                    self.modified_text.insert(tk.END, line)
        
        # Make the original text read-only to prevent user edits
        self.original_text.config(state=tk.DISABLED)

    def save_modified_text(self):
        """
        Save the modified text to a new file.
        
        This method:
        1. Checks if there is modified text to save
        2. Opens a file dialog for the user to choose save location
        3. Writes the modified text to the selected file
        4. Provides feedback on success or failure
        
        The method handles potential errors during the save operation
        and notifies the user accordingly.
        """
        # Check if there is any modified text to save
        if not self.modified_text.get(1.0, tk.END).strip():
            messagebox.showerror("Error", "No modified text to save.")
            return

        # Open file dialog to get save location
        if file_path := filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        ):
            try:
                # Write the modified text to the selected file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.modified_text.get(1.0, tk.END))
                # Show success message with the saved file path
                messagebox.showinfo("Success",
                                    f'Modified text saved to "{file_path}"')
            except Exception as e:
                # Handle any errors during file saving
                messagebox.showerror("Error", f"Error saving file: {str(e)}")


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
            text_font_size = int(self.text_font_size_var.get())  # Get label font size

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
            config.graph_figsize = [graph_width, graph_height]  # Update figure size
            config.graph_title_fontsize = title_fontsize
            config.graph_label_fontsize = label_fontsize
            config.graph_bar_color_single = self.bar_color_single_var.get()  # Update single color
            config.graph_bar_color_compare1 = self.bar_color_compare1_var.get()  # Update compare file 1 color
            config.graph_bar_color_compare2 = self.bar_color_compare2_var.get()  # Update compare file 2 color
            config.text_font_size = text_font_size
            self.apply_theme()
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
        self.text_font_size_var.set(str(config.text_font_size))  # Restore color for second compare file
        self.apply_theme()

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
        if type is int:
            temp_unsaved = int(temp_unsaved)
            if temp_unsaved > 0:  # Validate that input is a positive integer
                return temp_unsaved
            else:
                raise ValueError  # Trigger exception for invalid input
        elif type is float:
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
        elif type is int:
            print("Please enter a positive integer.", end="")
        elif type is float:
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
    unsaved_text_font_size = None

    while True:
        # Display the current configurable settings and menu options
        unsaved = False
        for unsaved_var in list(locals()):
            if unsaved_var in ("config_option", "unsaved", "unsaved_var"):
                continue
            if eval(unsaved_var) is not None:
                unsaved = True
        print(
            [[],
            [*f"Change settings{'(unsaved)' if unsaved else ''}:"],
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
            [*"Graph bar: set color of s", "\x1b[1;4;97mI\x1b[m", *f"ngle bar (analyse file) to {config.graph_bar_color_single if unsaved_graph_bar_color_single is None else f'{unsaved_graph_bar_color_single} (was {config.graph_bar_color_single})'}"],
            [*"Graph bar: set color of File", "\x1b[1;4;97m1\x1b[m", *f"'s bar (compare file) to {config.graph_bar_color_compare1 if unsaved_graph_bar_color_compare1 is None else f'{unsaved_graph_bar_color_compare1} (was {config.graph_bar_color_compare1})'}"],
            [*"Graph bar: set color of File", "\x1b[1;4;97m2\x1b[m", *f"'s bar (compare file) to {config.graph_bar_color_compare2 if unsaved_graph_bar_color_compare2 is None else f'{unsaved_graph_bar_color_compare2} (was {config.graph_bar_color_compare2})'}"],
            [*"Graph ", "\x1b[1;4;97mT\x1b[m", *f"itle: set font size to {config.graph_title_fontsize if unsaved_graph_title_fontsize is None else f'{unsaved_graph_title_fontsize} (was {config.graph_title_fontsize})'}"],
            [*"Graph ", "\x1b[1;4;97mL\x1b[m", *f"abel: set font size to {config.graph_label_fontsize if unsaved_graph_label_fontsize is None else f'{unsaved_graph_label_fontsize} (was {config.graph_label_fontsize})'}"],
            [*"Text: set ", "\x1b[1;4;97mF\x1b[m", *f"ont size to {config.text_font_size if unsaved_text_font_size is None else f'{unsaved_text_font_size} (was {config.text_font_size})'}"],
            ["\x1b[1;4mS\x1b[m", *"ave and exit"],
            ["\x1b[1;4;97mE\x1b[m", *"xit without saving"]], _override=True, wrap_override=True)  # Formatting the options menu
        
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
        elif config_option == "I":
            unsaved_graph_bar_color_single = configure_test_input("Enter color of the bar in Analyze File mode", str, str(config.graph_bar_color_single))
        elif config_option == "1":
            unsaved_graph_bar_color_compare1 = configure_test_input("Enter color of File1's bar in Compare Files mode", str, str(config.graph_bar_color_compare1))
        elif config_option == "2":
            unsaved_graph_bar_color_compare2 = configure_test_input("Enter color of File2's bar in Compare Files mode", str, str(config.graph_bar_color_compare2))
        elif config_option == "T":
            unsaved_graph_title_fontsize = configure_test_input("Enter font size of the figure's title", float, str(config.graph_title_fontsize))
        elif config_option == "L":
            unsaved_graph_label_fontsize = configure_test_input("Enter font size of the figure's labels", float, str(config.graph_label_fontsize))
        elif config_option == "F":
            unsaved_text_font_size = configure_test_input("Enter font size of the text labels", int, str(config.graph_label_fontsize))
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
        if unsaved_text_font_size is not None:
            config.text_font_size = unsaved_text_font_size

        # Save updated configuration to persistent storage
        config.save()
        print("Saved!")
    
    
def search_word(file_path:str, target_word:str):
    """
    Search for a word in a file and display its positions.
    
    Args:
        file_path (str): Path to the file to search
        target_word (str): Word to search for
        
    This function:
    1. Reads and cleans the file content
    2. Finds all occurrences of the target word
    3. Displays the results with highlighted context
    
    The function handles file reading errors and provides feedback
    about the search operation.
    """
    content = read_file(file_path)

    if content is not None:
        positions = search_word_position(clean_text(content), target_word)
        if positions:
            print(f'The word "{target_word}" appears {len(positions)} times at positions: {", ".join(str(pos[0]) for pos in positions)}')
            return
    print(f'The word "{target_word}" was not found in the file.')


def replace_word(file_path:str, target_word:str, replacement_word:str):
    """
    Replace occurrences of a target word with a replacement word in a file.
    
    Args:
        file_path (str): Path to the file to modify
        target_word (str): Word to be replaced
        replacement_word (str): Word to replace the target word with
        
    This function:
    1. Reads the file content preserving original formatting
    2. Replaces all occurrences of the target word
    3. Displays a preview of the original and modified text
    4. Offers to save the modified text to a new file
    
    The function handles file reading errors and provides feedback
    about the replacement operation.
    """
    content = read_file(file_path)

    if content is not None:
        # Split by words while preserving newlines and spacing
        lines = content.split("\n")
        modified_lines = []
        
        for line in lines:
            if not line.strip():  # Preserve empty lines
                modified_lines.append("")
                continue
                
            words = line.split()
            modified_line = ""
            current_pos = 0
            
            # Find all occurrences of the target word in this line
            positions = []
            for idx, word in enumerate(words):
                # Check if this word matches our target (ignoring case and punctuation)
                clean_word = "".join(c.lower() for c in word if c.isalnum())
                if clean_word == target_word.lower():
                    positions.append(idx)
            
            if positions:
                # Process the line with replacements
                current_pos = 0
                for pos in positions:
                    # Add text up to this position
                    modified_line += " ".join(words[current_pos:pos]) + (" " if current_pos < pos else "")
                    
                    # Get the original word
                    original_word = words[pos]
                    
                    # Extract leading and trailing punctuation
                    leading_punct = ""
                    trailing_punct = ""
                    
                    # Extract leading punctuation
                    i = 0
                    while i < len(original_word) and not original_word[i].isalnum():
                        leading_punct += original_word[i]
                        i += 1
                    
                    # Extract trailing punctuation
                    i = len(original_word) - 1
                    while i >= 0 and not original_word[i].isalnum():
                        trailing_punct = original_word[i] + trailing_punct
                        i -= 1
                    
                    # Insert the replacement with punctuation preserved
                    modified_line += leading_punct + replacement_word + trailing_punct
                    
                    # Add a space if this isn"t the last word
                    if pos < len(words) - 1:
                        modified_line += " "
                    
                    current_pos = pos + 1
                
                # Add any remaining text in the line
                if current_pos < len(words):
                    modified_line += " ".join(words[current_pos:])
            else:
                # No replacements in this line, keep it as is
                modified_line = line
                
            modified_lines.append(modified_line)
        
        # Join all lines back together with newlines preserved
        modified_content = "\n".join(modified_lines)

        print(f"\n\
Original text:\n\
{(content[:100])+"..." if len(content) > 100 else content}\n\
\n\
Modified text:\n\
{modified_content[:100]+"..." if len(modified_content) > 100 else modified_content}"
              )

        save_option = input("\n\nDo you want to save the modified text to a new file? (y/n): ", single_letter=True).strip().lower()
        if save_option == "y":
            new_file_path = input(
                "Enter the path for the new file: ").strip()
            try:
                with open(new_file_path, "w", encoding="utf-8") as file:
                    file.write(modified_content)
                print(f'Modified text saved to "{new_file_path}"')
            except Exception as e:
                print(f"Error saving file: {str(e)}")




def display_results(file_path:str, word_count:tuple[list, list], total_words:int, unique_words:int, show_nums:int = 10, wrap:int = os.get_terminal_size().columns):
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
        wrap (int): The terminal width to wrap text (default is the current terminal size)
    """
    # Limit number of words to display to available words
    show_nums = helpers.min(show_nums, len(word_count[0]))  # Maximum words to show is the smaller of user request or available data
    hyphen_wrap = helpers.min(wrap, len(str(show_nums)) + 30)  # Text wrapping limit

    # Print header and statistics
    print(f'\
\n\
{"=" * helpers.min(wrap, len(file_path) + 15)}\n\
Analysis of "{file_path}":\n\
{"=" * helpers.min(wrap, len(file_path) + 15)}\n\
Total words: {total_words}\n\
Unique words: {unique_words}\n\
\n\
\n\
Top {show_nums} Most Frequent Words:\n\
{"-" * hyphen_wrap}')

    # Print frequency-sorted words
    frequency_sorted = sort_by_frequency(word_count)  # Get list of words sorted by frequency
    txt = "".join(f'{i + 1}. "{word}": {count} times\n' for i, (word, count) in enumerate(frequency_sorted[:show_nums]))  # Format output
    print(txt)  # Display formatted word frequency information

    # Print alphabetically-sorted words
    txt = f"\nFirst {show_nums} Words (Alphabetically):\n{"-" * hyphen_wrap}\n"  # Setup string for display
    alpha_sorted = sort_alphabetically(word_count)  # Get list of words sorted alphabetically
    for i, (word, count) in enumerate(alpha_sorted[:show_nums]):  # Iterate and format
        txt += f'{i + 1}. "{word}": {count} times\n'  # Append formatted string
    print(txt)  # Display the final formatted alphabetical listings

def compare_files(file_path1:str, file_path2:str):
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
        f'\n{"=" * helpers.min(columns, len(file_path1) + len(file_path2) + 30)}\n\
Comparison between "{file_path1}" and "{file_path2}":\n\
{"=" * helpers.min(columns, len(file_path1) + len(file_path2) + 30)}\n\n\
Similarity percentage of\n\
text 1: {similarity[0]:.2f}%\n\
text 2: {similarity[1]:.2f}%'
    )

    # Determine and display the plagiarism level using the similarity percentage
    similarity = helpers.max(similarity)
    if similarity > 80:
        print("\x1b[31mPlagiarism Level: HIGH - These texts are very similar\x1b[m")  # High similarity
    elif similarity > 50:
        print("\x1b[33mPlagiarism Level: MEDIUM - These texts have significant overlap\x1b[m")  # Medium similarity
    elif similarity > 20:
        print("\x1b[92mPlagiarism Level: LOW - These texts have some common elements\x1b[m")  # Low similarity
    else:
        print("\x1b[32mPlagiarism Level: MINIMAL - These texts are mostly different\x1b[m")  # Minimal similarity

def analyze_file(file_path:str):
    """
    Analyze a single text file for CLI mode.
    
    This function reads the specified file, cleans its content,
    counts words, determines total and unique word counts,
    and then displays results using display_results().

    Args:
        file_path (str): The path to the file to analyze
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
    

def mainGUI():
    """
    Start the GUI version of the Word Analysis and Plagiarism Detection System.

    This function initializes the tkinter window, creates an instance of the application,
    and sets up a dialog confirmation when the user attempts to close the window.
    """
    root = tk.Tk()  # Create main tkinter window
    app = WordAnalysisApp(root, config.window_size)  # Instantiate GUI
    #app is unused because tkinter take care of all the stuff
    
    # Begin the main event loop
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
3. Search for a word in a file\n\
4. Replace a word in a file\n\
5. Configure settings\n\
6. Exit\n")

        # Prompt user for choice and capture input
        choice = input("\nEnter your choice (1-6): ", single_letter=True).strip()

        # Handle each choice
        if choice in "1234":
            txt_files = [file for file in os.listdir() if os.path.isfile(file) and file.endswith(".txt")]
            print("Text files in current directory:\n" + "\n".join(txt_files))
            if choice == "1":
                file_path = input("Enter the path to the text file: ").strip()  # Path for file
                analyze_file(file_path)  # Call the analyze function for the selected file

            elif choice == "2":
                file_path1 = input("Enter the path to the first text file: ").strip()  # Path for first file
                file_path2 = input("Enter the path to the second text file: ").strip()  # Path for second file
                compare_files(file_path1, file_path2)  # Call compare function on selected files

            elif choice == "3":
                file_path = input("Enter the path to the text file: ").strip()
                target_word = input("Enter the word to search for: ").strip()
                search_word(file_path, target_word)

            elif choice == "4":
                file_path = input("Enter the path to the text file: ").strip()
                target_word = input("Enter the word to replace: ").strip()
                replacement_word = input("Enter the replacement word: ").strip()
                replace_word(file_path, target_word, replacement_word)
        
        elif choice == "5":
            configure()  # Call configuration function

        elif choice == "6":
            print("Thank you for using WAPDS!")
            break  # Exit the loop

        else:
            print(f"Invalid choice {repr(choice)}. Please enter a number between 1 and 6.")  # Input error handling

if __name__ == "__main__":
    # Parse command line arguments to determine whether to run GUI or CLI version of the application
    some_text = "{width}x{height}"  # Still dont know how to put curly brackets in f string
    parser = argparse.ArgumentParser(description="Word Analysis and Plagiarism Detection System (WAPDS)")  # Setup argument parser
    parser.add_argument(
        "run_type",
        help='Enter "GUI" or "CLI" to determine which version should run, defaults to GUI',
        nargs="?",  # Optional argument with default
        default="GUI")  # Default to GUI if not provided
    parser.add_argument(
        "GUI_window_size",
        help=f"Enter in format of {some_text}, set the GUI window size and will be saved, defaults to last window size (currently {repr(config.window_size)})",
        nargs="?",  # Optional argument for GUI window size configuration
        default=config.window_size)  # Default size of the window
    args = parser.parse_args()  # Parse the command-line arguments

    # Start the appropriate interface based on the argument provided
    if args.run_type == "GUI":
        if plt is None:  # if matplotlib is missing
            print("\x1b[33mWarning: matplotlib is not found, or is corrupted. Please (re)install matplotlib by running `python -m pip install matplotlib` in the terminal\x1b[m")
        # Set GUI window size
        GUI_window_size = args.GUI_window_size.strip()
        GUI_window_size_check = GUI_window_size.split("x")  # Split input into width and height
        try:
            GUI_window_size_check = [int(dimension) for dimension in GUI_window_size_check]  # Convert dimensions into integers
            if len(GUI_window_size_check) != 2:  # Check for two dimensions
                raise ValueError  # Raise an error if not valid
            for n in GUI_window_size_check:  # Validate each dimension
                if n <= 0:  # Ensure dimensions are positive
                    raise ValueError
        except ValueError:
            # If parsing fails, inform the user of the formatting error
            if GUI_window_size == config.window_size:
                config.reset_to_defaults() #corrupted config
            else:
                parser.error(f"Please enter GUI window size in the format of {some_text}, not {repr(args.GUI_window_size)}")
        config.window_size = GUI_window_size  # Set the new window size in the config
        config.save()  # Save the new configurations
        mainGUI()  # Launch GUI application
    elif args.run_type == "CLI":
        # make print and input animated, looks fancy, yet creates inconvenience lol
        from helpers import animated_print as print, animated_input as input
        mainCLI()  # Launch CLI application
    else:
        # If an invalid run type is provided, inform the user
        parser.error(f'Please enter either "GUI" or "CLI" for run type, not {repr(args.run_type)}')
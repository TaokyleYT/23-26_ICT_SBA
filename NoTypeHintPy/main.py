import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import helpers

try:
    from nltk_plagiarism import get_similarity_score
except:
    get_similarity_score = None
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends._backend_tk import NavigationToolbar2Tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except:
    plt = None
import argparse


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
        graph_title_fontsize (float): Font size for graph titles
        graph_label_fontsize (float): Font size for graph labels
        dark_mode (bool): Whether dark mode is enabled
        text_font_size (int): Font size for text labels
    """

    DEFAULTS = {
        "CLI": {"single_file_display_line": 10, "compare_file_display_line": 5},
        "GUI": {
            "window_size": "1000x700",
            "graph_max_words": 10,
            "graph_figsize": [5.0, 4.0],
            "analyze_max_words": 5,
            "graph_bar_color_single": "skyblue",
            "graph_bar_color_compare1": "skyblue",
            "graph_bar_color_compare2": "lightgreen",
            "graph_title_fontsize": 12.0,
            "graph_label_fontsize": 10.0,
            "dark_mode": False,
            "text_font_size": 10,
        },
    }
    try:
        with open("WAPDS.config", "r") as f:
            config_data = f.readline().split(";")
            single_file_display_line = int(config_data[0])
            compare_file_display_line = int(config_data[1])
            window_size = str(config_data[2])
            graph_max_words = int(config_data[3])
            graph_figsize = [float(config_data[4]), float(config_data[5])]
            analyze_max_words = int(config_data[6])
            graph_bar_color_single = str(config_data[7])
            graph_bar_color_compare1 = str(config_data[8])
            graph_bar_color_compare2 = str(config_data[9])
            graph_title_fontsize = float(config_data[10])
            graph_label_fontsize = float(config_data[11])
            dark_mode = bool(int(config_data[12]))
            text_font_size = int(config_data[13])
    except:
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
    with open("WAPDS.config", "w") as f:
        f.write(
            f"{single_file_display_line};{compare_file_display_line};{window_size};{graph_max_words};{graph_figsize[0]};{graph_figsize[1]};{analyze_max_words};{graph_bar_color_single};{graph_bar_color_compare1};{graph_bar_color_compare2};{graph_title_fontsize};{graph_label_fontsize};{int(dark_mode)};{text_font_size}"
        )

    @classmethod
    def reset_to_defaults(cls):
        """
        Reset all settings to their default values.

        This method restores all configuration parameters to the predefined default values
        but does not save them to the configuration file.
        """
        cls.single_file_display_line = cls.DEFAULTS["CLI"]["single_file_display_line"]
        cls.compare_file_display_line = cls.DEFAULTS["CLI"]["compare_file_display_line"]
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
            f.write(
                f"{cls.single_file_display_line};{cls.compare_file_display_line};{cls.window_size};{cls.graph_max_words};{cls.graph_figsize[0]};{cls.graph_figsize[1]};{cls.analyze_max_words};{cls.graph_bar_color_single};{cls.graph_bar_color_compare1};{cls.graph_bar_color_compare2};{cls.graph_title_fontsize};{cls.graph_label_fontsize};{int(cls.dark_mode)};{cls.text_font_size}"
            )


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
    txt_files = [
        file for file in os.listdir() if os.path.isfile(file) and file.endswith(".txt")
    ]
    if not os.path.exists(file_path):
        print(f'\x1b[31mError: File "{file_path}" not found.\x1b[m')
        if file_path + ".txt" in txt_files:
            print(f'\x1b[33mDid you mean "{file_path}.txt"?\x1b[m')
        return None
    if not os.path.isfile(file_path):
        print(f'\x1b[31mError: "{file_path}" is not a file.\x1b[m')
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        if not content.strip():
            print(f'\x1b[33mWarning: File "{file_path}" is empty.\x1b[m')
        return content
    except Exception as e:
        print(f'\x1b[31mError reading file "{file_path}": {str(e)}\x1b[m')
        return None


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
    2. Replacing all non-alphanumeric characters (except hyphens) with spaces
    3. Removing extra spaces
    """
    if text is None:
        return ""
    cleaned_text = "".join(
        (
            (
                char
                if "a" <= char <= "z"
                or "0" <= char <= "9"
                or char == " "
                or (char == "-")
                else " "
            )
            for char in text.lower()
        )
    )
    while "  " in cleaned_text:
        cleaned_text = cleaned_text.replace("  ", " ")
    return cleaned_text.strip()


def alphanumerical(text):
    """
    Finds out if the text is alphanumerical. (basically str.isalnum())

    Args:
        text (str): The text to check

    Returns:
        bool: True if the text is alphanumerical, False otherwise.

    This function checks if the input text contains only alphanumeric characters
    """
    return helpers.all(
        ("a" <= char <= "z" or "0" <= char <= "9" for char in text.lower())
    )


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
    word_count = ([], [])
    words = text.split(" ")
    for n in range(len(words)):
        word = words[n]
        word_index = helpers.linear_search(word_count[0], word)
        if word_index != -1:
            word_count[1][word_index] += 1
        else:
            word_count[0].append(word)
            word_count[1].append(1)
    return word_count


def search_word_position(text, target_word, regex=False):
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
    if not text or not target_word:
        return []
    results = []
    if regex:
        try:
            pattern = re.compile(target_word, re.IGNORECASE)
            words = text.split()
            for idx in range(len(words)):
                word = words[idx]
                if pattern.search(word):
                    results.append((idx, word))
        except re.error:
            return []
    else:
        words = text.lower().split()
        target_word = target_word.lower()
        for idx, word in enumerate(words):
            clean_word = "".join(
                (c.lower() for c in word if alphanumerical(c) or c == "'" or c == "-")
            )
            if clean_word == target_word:
                results.append((idx, word))
    return results


def sort_alphabetically(word_count):
    """
    Sort words alphabetically using quick sort from helpers.

    Args:
        word_count (tuple): A tuple of (words, frequencies) as returned by count_words()

    Returns:
        list: List of (word, frequency) tuples sorted alphabetically

    This function sorts the words in alphabetical order and returns a list of
    (word, frequency) pairs maintaining the original frequency information.
    """
    word_items = []
    for idx in range(len(word_count[0])):
        word_items.append((word_count[0][idx], word_count[1][idx]))
    items_to_sort = []
    for i, item in enumerate(word_items):
        items_to_sort.append((item, i))
    sorted_indices = helpers.quick_sort(items_to_sort)
    result = []
    for _, idx in sorted_indices:
        result.append(word_items[idx])
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
    word_items = []
    for idx in range(len(word_count[0])):
        word_items.append((word_count[0][idx], word_count[1][idx]))
    items_to_sort = []
    for i, item in enumerate(word_items):
        items_to_sort.append(((item[1], item[0]), i))
    sorted_indices = helpers.quick_sort(items_to_sort, reverse=True)
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
        tuple of 2 floats: Similarity percentage (0-100) of text1 and text2 respectively

    This function calculates the jaccard(?) similarity of both texts by equation given by teacher
    """
    common_freq = 0
    count1_freq = 0
    count2_freq = 0
    for idx1, word1 in enumerate(word_count1[0]):
        freq1 = word_count1[1][idx1]
        count1_freq += freq1
        idx2 = helpers.linear_search(word_count2[0], word1)
        if idx2 != -1:
            common_freq += helpers.min(freq1, word_count2[1][idx2])
    for freq2 in word_count2[1]:
        count2_freq += freq2
    return (
        common_freq / count1_freq * 100 if count1_freq > 0 else 0,
        common_freq / count2_freq * 100 if count2_freq > 0 else 0,
    )


class GUI_APP:
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

    LIGHT_THEME = [
        "#f0f0f0",
        "#000000",
        "#ffffff",
        "#000000",
        "#e0e0e0",
        "#4a6984",
        "#ffffff",
        "#ffffff",
        "#f0f0f0",
        "#f0f0f0",
        "#f0f0f0",
    ]
    DARK_THEME = [
        "#1e1e1e",
        "#ffffff",
        "#2d2d2d",
        "#ffffff",
        "#3d3d3d",
        "#0078d7",
        "#ffffff",
        "#2d2d2d",
        "#1e1e1e",
        "#1e1e1e",
        "#2d2d2d",
    ]

    def __init__(self, root, size):
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
            if (
                self.root.state() == "normal"
                and event.width > 150
                and (event.height > 150)
            ):
                self.window_size = f"{event.width}x{event.height}"

        def exit_GUI():
            """
            Exit the GUI application with a confirmation dialog.

            This function prompts the user with a message box asking for confirmation
            before quitting the application and thanking them for using it.
            """
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                if self.window_size is not None:
                    config.window_size = self.window_size
                    config.save()
                root.bind("<Configure>", lambda: None)
                messagebox.showwarning(
                    "Thank you, app closing...", message="Thank you for using WAPDS"
                )
                root.destroy()
                exit()

        self.root = root
        self.root.title("Word Analysis and Plagiarism Detection")
        self.window_size = None
        self.root.geometry(size)
        root.protocol("WM_DELETE_WINDOW", exit_GUI)
        root.bind("<Configure>", save_window_size)
        self.theme_frame = ttk.Frame(root)
        self.theme_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 5))
        self.theme_var = tk.BooleanVar(value=config.dark_mode)
        self.theme_toggle = ttk.Checkbutton(
            self.theme_frame,
            text="Dark Mode",
            variable=self.theme_var,
            command=self.toggle_theme,
        )
        self.theme_toggle.pack(side=tk.RIGHT)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.style = ttk.Style()
        self.create_analyze_tab()
        self.create_compare_tab()
        self.create_search_tab()
        self.create_replace_tab()
        self.create_config_tab()
        self.apply_theme()

    def apply_theme(self):
        """
        Apply the current theme to all UI elements.

        This method configures all widgets with the appropriate colors and styles
        based on whether dark mode is enabled or not.
        """

        def _update_widget_colors(widget, theme):
            """
            Recursively update colors for all widgets.

            Args:
                widget: The widget to update
                theme: The theme colors to apply

            This helper method traverses the widget hierarchy and applies
            appropriate theme colors to each widget based on its type.
            """
            widget_class = widget.__class__.__name__
            if widget_class == "Text":
                widget.configure(
                    background=theme[2],
                    foreground=theme[3],
                    insertbackground=theme[1],
                    selectbackground=theme[5],
                    selectforeground=theme[6],
                    font=("Arial", config.text_font_size),
                )
            elif widget_class == "Listbox":
                widget.configure(
                    background=theme[2],
                    foreground=theme[3],
                    selectbackground=theme[5],
                    selectforeground=theme[6],
                    font=("Arial", config.text_font_size),
                )
            elif widget_class == "Canvas":
                widget.configure(background=theme[7])
            elif widget_class == "Label":
                widget.configure(
                    background=theme[8],
                    foreground=theme[1],
                    font=("Arial", config.text_font_size),
                )
            elif widget_class == "LabelFrame":
                widget.configure(
                    background=theme[9],
                    foreground=theme[1],
                    font=("Arial", config.text_font_size),
                )
            for child in widget.winfo_children():
                _update_widget_colors(child, theme)

        theme = self.DARK_THEME if config.dark_mode else self.LIGHT_THEME
        self.style.theme_use("default")
        self.style.configure("TFrame", background=theme[8])
        self.style.configure("TLabelframe", background=theme[9])
        self.style.configure(
            "TLabelframe.Label",
            background=theme[9],
            foreground=theme[1],
            font=("Arial", config.text_font_size),
        )
        self.style.configure("TNotebook", background=theme[0])
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", theme[5]), ("!selected", theme[10])],
            foreground=[("selected", theme[6]), ("!selected", theme[1])],
        )
        self.style.configure(
            "TButton",
            background=theme[4],
            foreground=theme[1],
            font=("Arial", config.text_font_size),
        )
        self.style.map(
            "TButton",
            background=[("active", theme[5])],
            foreground=[("active", theme[6])],
        )
        self.style.configure(
            "TEntry",
            fieldbackground=theme[2],
            foreground=theme[3],
            insertcolor=theme[1],
            font=("Arial", config.text_font_size),
        )
        self.style.configure(
            "TCheckbutton",
            background=theme[8],
            foreground=theme[1],
            selectcolor=theme[2],
        )
        self.style.map(
            "TCheckbutton",
            background=[("active", theme[8])],
            foreground=[("active", theme[1])],
        )
        self.style.configure(
            "TLabel",
            background=theme[8],
            foreground=theme[1],
            font=("Arial", config.text_font_size),
        )
        self.root.configure(background=theme[0])
        _update_widget_colors(self.root, theme)
        if plt is not None:
            plt.style.use("dark_background" if config.dark_mode else "default")
            if hasattr(self, "analyze_graph_cmd"):
                eval(self.analyze_graph_cmd)
            if hasattr(self, "compare_graph_cmd"):
                eval(self.compare_graph_cmd)

    def toggle_theme(self):
        """
        Toggle between light and dark themes.

        This method updates the config setting, saves it, and applies
        the new theme to all UI elements.
        """
        config.dark_mode = self.theme_var.get()
        config.save()
        self.apply_theme()

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
        file_frame = ttk.Frame(analyze_tab)
        file_frame.pack(fill=tk.X, pady=10)
        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.file_entry1 = ttk.Entry(file_frame, width=50)
        self.file_entry1.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file1)
        browse_btn.pack(side=tk.LEFT, padx=5)
        analyze_btn = ttk.Button(file_frame, text="Analyze", command=self.analyze_file)
        analyze_btn.pack(side=tk.LEFT, padx=5)
        results_frame = ttk.Frame(analyze_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        stats_frame = ttk.LabelFrame(left_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, pady=5)
        self.stats_text = tk.Text(stats_frame, height=5, width=40, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        lists_frame = ttk.Frame(left_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        freq_frame = ttk.LabelFrame(lists_frame, text="Most Frequent Words")
        freq_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.freq_list = tk.Listbox(freq_frame, height=15)
        self.freq_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        alpha_frame = ttk.LabelFrame(lists_frame, text="Alphabetical Words")
        alpha_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.alpha_list = tk.Listbox(alpha_frame, height=15)
        self.alpha_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        right_frame = ttk.Frame(results_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        self.analyze_graph_frame = ttk.LabelFrame(
            right_frame, text="Word Frequency Graph"
        )
        self.analyze_graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
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
            Update file labels based on whether cosine similarity is enabled.

            When cosine similarity is enabled:
            - File 1 becomes "File"
            - File 2 becomes "Reference Files"
            Otherwise, they remain as "File 1" and "File 2"
            """
            if self.compare_nltk.get():
                self.file1_label.config(text="File:")
                self.file2_label.config(text="Reference Files:")
                self.file1_stats_frame.config(text="File Statistics")
                self.file2_stats_frame.config(text="Reference Files Statistics")
                browse_btn2.config(command=self.browse_compare_file2_nltk)
            else:
                self.file1_label.config(text="File 1:")
                self.file2_label.config(text="File 2:")
                self.file1_stats_frame.config(text="File 1 Statistics")
                self.file2_stats_frame.config(text="File 2 Statistics")
                browse_btn2.config(command=self.browse_compare_file2)

        compare_tab = ttk.Frame(self.notebook)
        self.notebook.add(compare_tab, text="Compare Files")
        files_frame = ttk.Frame(compare_tab)
        files_frame.pack(fill=tk.X, pady=10)
        file1_frame = ttk.Frame(files_frame)
        file1_frame.pack(fill=tk.X, pady=5)
        self.file1_label = ttk.Label(file1_frame, text="File 1:")
        self.file1_label.pack(side=tk.LEFT, padx=5)
        self.compare_file_entry1 = ttk.Entry(file1_frame, width=50)
        self.compare_file_entry1.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        browse_btn1 = ttk.Button(
            file1_frame, text="Browse", command=self.browse_compare_file1
        )
        browse_btn1.pack(side=tk.LEFT, padx=5)
        file2_frame = ttk.Frame(files_frame)
        file2_frame.pack(fill=tk.X, pady=5)
        self.file2_label = ttk.Label(file2_frame, text="File 2:")
        self.file2_label.pack(side=tk.LEFT, padx=5)
        self.compare_file_entry2 = ttk.Entry(file2_frame, width=50)
        self.compare_file_entry2.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        browse_btn2 = ttk.Button(
            file2_frame, text="Browse", command=self.browse_compare_file2
        )
        browse_btn2.pack(side=tk.LEFT, padx=5)
        buttons_frame = ttk.Frame(files_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        compare_btn = ttk.Button(
            buttons_frame, text="Compare Files", command=self.compare_files
        )
        compare_btn.pack(side=tk.TOP, pady=10)
        self.compare_nltk = tk.BooleanVar(value=False)
        use_nltk = ttk.Checkbutton(
            buttons_frame,
            text="Use cosine similarity",
            variable=self.compare_nltk,
            command=update_file_labels,
        )
        use_nltk.pack(side=tk.RIGHT, padx=5)
        results_frame = ttk.Frame(compare_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        lists_frame = ttk.Frame(left_frame)
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.file1_stats_frame = ttk.LabelFrame(lists_frame, text="File 1 Statistics")
        self.file1_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.file1_stats_text = tk.Text(
            self.file1_stats_frame, height=5, width=40, wrap=tk.WORD
        )
        self.file1_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file2_stats_frame = ttk.LabelFrame(lists_frame, text="File 2 Statistics")
        self.file2_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.file2_stats_text = tk.Text(
            self.file2_stats_frame, height=5, width=40, wrap=tk.WORD
        )
        self.file2_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        comparison_frame = ttk.LabelFrame(left_frame, text="Comparison Results")
        comparison_frame.pack(fill=tk.X, pady=10)
        self.comparison_text = tk.Text(comparison_frame, height=6, wrap=tk.WORD)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        right_frame = ttk.Frame(results_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        self.compare_graph_frame = ttk.LabelFrame(
            right_frame, text="Word Frequency Comparison"
        )
        self.compare_graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.compare_canvas = tk.Canvas(self.compare_graph_frame)
        self.compare_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_search_tab(self):
        """Create the Search tab for word searching."""
        search_tab = ttk.Frame(self.notebook)
        self.notebook.add(search_tab, text="Search Word")
        file_frame = ttk.Frame(search_tab)
        file_frame.pack(fill=tk.X, pady=10)
        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.search_file_entry = ttk.Entry(file_frame, width=50)
        self.search_file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        browse_btn = ttk.Button(
            file_frame, text="Browse", command=self.browse_search_file
        )
        browse_btn.pack(side=tk.LEFT, padx=5)
        search_frame = ttk.Frame(search_tab)
        search_frame.pack(fill=tk.X, pady=10)
        ttk.Label(search_frame, text="Search for:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.regex_var = tk.BooleanVar(value=False)
        regex_check = ttk.Checkbutton(
            search_frame, text="Use Regex", variable=self.regex_var
        )
        regex_check.pack(side=tk.LEFT, padx=5)
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_word)
        search_btn.pack(side=tk.LEFT, padx=5)
        results_frame = ttk.LabelFrame(search_tab, text="Search Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        self.search_results = tk.Text(results_frame, wrap=tk.WORD)
        self.search_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.search_results.config(state=tk.DISABLED)

    def create_replace_tab(self):
        """Create the Replace tab for word replacement."""
        replace_tab = ttk.Frame(self.notebook)
        self.notebook.add(replace_tab, text="Replace Word")
        file_frame = ttk.Frame(replace_tab)
        file_frame.pack(fill=tk.X, pady=10)
        ttk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.replace_file_entry = ttk.Entry(file_frame, width=50)
        self.replace_file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        browse_btn = ttk.Button(
            file_frame, text="Browse", command=self.browse_replace_file
        )
        browse_btn.pack(side=tk.LEFT, padx=5)
        replace_frame = ttk.Frame(replace_tab)
        replace_frame.pack(fill=tk.X, pady=10)
        word_frame = ttk.Frame(replace_frame)
        word_frame.pack(fill=tk.X, pady=5)
        ttk.Label(word_frame, text="Text to replace:").pack(side=tk.LEFT, padx=5)
        self.word_entry = ttk.Entry(word_frame, width=30)
        self.word_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.replace_regex_var = tk.BooleanVar(value=False)
        regex_check = ttk.Checkbutton(
            word_frame, text="Use Regex", variable=self.replace_regex_var
        )
        regex_check.pack(side=tk.LEFT, padx=5)
        replacement_frame = ttk.Frame(replace_frame)
        replacement_frame.pack(fill=tk.X, pady=5)
        ttk.Label(replacement_frame, text="Replacement text:").pack(
            side=tk.LEFT, padx=5
        )
        self.replacement_entry = ttk.Entry(replacement_frame, width=30)
        self.replacement_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        replace_btn = ttk.Button(
            replace_frame, text="Replace", command=self.replace_word
        )
        replace_btn.pack(pady=5)
        text_frame = ttk.Frame(replace_tab)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        original_frame = ttk.LabelFrame(text_frame, text="Original Text")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.original_text = tk.Text(original_frame, wrap=tk.WORD)
        self.original_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.original_text.config(state=tk.DISABLED)
        modified_frame = ttk.LabelFrame(text_frame, text="Modified Text")
        modified_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.modified_text = tk.Text(modified_frame, wrap=tk.WORD)
        self.modified_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        save_frame = ttk.Frame(replace_tab)
        save_frame.pack(fill=tk.X, pady=10)
        save_btn = ttk.Button(
            save_frame, text="Save Modified Text", command=self.save_modified_text
        )
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
        config_tab = ttk.Frame(self.notebook)
        self.notebook.add(config_tab, text="Configuration")
        CLI_settings_frame = ttk.LabelFrame(config_tab, text="CLI Settings")
        CLI_settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        GUI_settings_frame = ttk.LabelFrame(config_tab, text="GUI Settings")
        GUI_settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        single_file_frame = ttk.Frame(CLI_settings_frame)
        single_file_frame.pack(fill=tk.X, pady=10)
        ttk.Label(
            single_file_frame, text="Number of words to display in Analyze File tab:"
        ).pack(side=tk.LEFT, padx=5)
        self.single_file_display_var = tk.StringVar(
            value=str(config.single_file_display_line)
        )
        self.single_file_display_entry = ttk.Entry(
            single_file_frame, width=10, textvariable=self.single_file_display_var
        )
        self.single_file_display_entry.pack(side=tk.LEFT, padx=5)
        compare_file_frame = ttk.Frame(CLI_settings_frame)
        compare_file_frame.pack(fill=tk.X, pady=10)
        ttk.Label(
            compare_file_frame, text="Number of words to display in Compare Files tab:"
        ).pack(side=tk.LEFT, padx=5)
        self.compare_file_display_var = tk.StringVar(
            value=str(config.compare_file_display_line)
        )
        self.compare_file_display_entry = ttk.Entry(
            compare_file_frame, width=10, textvariable=self.compare_file_display_var
        )
        self.compare_file_display_entry.pack(side=tk.LEFT, padx=5)
        graph_settings_frame = ttk.LabelFrame(GUI_settings_frame, text="Graph Settings")
        graph_settings_frame.pack(fill=tk.X, pady=10, padx=5)
        words_frame = ttk.Frame(graph_settings_frame)
        words_frame.pack(fill=tk.X, pady=5)
        ttk.Label(words_frame, text="Max words in graph:").pack(side=tk.LEFT, padx=5)
        self.graph_max_words_var = tk.StringVar(value=str(config.graph_max_words))
        self.graph_max_words_entry = ttk.Entry(
            words_frame, width=10, textvariable=self.graph_max_words_var
        )
        self.graph_max_words_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(words_frame, text="Max words to show in text:").pack(
            side=tk.LEFT, padx=5
        )
        self.analyze_max_words_var = tk.StringVar(value=str(config.analyze_max_words))
        self.analyze_max_words_entry = ttk.Entry(
            words_frame, width=10, textvariable=self.analyze_max_words_var
        )
        self.analyze_max_words_entry.pack(side=tk.LEFT, padx=5)
        size_frame = ttk.Frame(graph_settings_frame)
        size_frame.pack(fill=tk.X, pady=5)
        ttk.Label(size_frame, text="Graph size (width, height):").pack(
            side=tk.LEFT, padx=5
        )
        self.graph_width_var = tk.StringVar(value=str(config.graph_figsize[0]))
        self.graph_width_entry = ttk.Entry(
            size_frame, width=5, textvariable=self.graph_width_var
        )
        self.graph_width_entry.pack(side=tk.LEFT, padx=2)
        self.graph_height_var = tk.StringVar(value=str(config.graph_figsize[1]))
        self.graph_height_entry = ttk.Entry(
            size_frame, width=5, textvariable=self.graph_height_var
        )
        self.graph_height_entry.pack(side=tk.LEFT, padx=2)
        font_frame = ttk.Frame(graph_settings_frame)
        font_frame.pack(fill=tk.X, pady=5)
        ttk.Label(font_frame, text="Title font size:").pack(side=tk.LEFT, padx=5)
        self.title_font_var = tk.StringVar(value=str(config.graph_title_fontsize))
        self.title_font_entry = ttk.Entry(
            font_frame, width=5, textvariable=self.title_font_var
        )
        self.title_font_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(font_frame, text="Label font size:").pack(side=tk.LEFT, padx=5)
        self.label_font_var = tk.StringVar(value=str(config.graph_label_fontsize))
        self.label_font_entry = ttk.Entry(
            font_frame, width=5, textvariable=self.label_font_var
        )
        self.label_font_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(font_frame, text="Text font size:").pack(side=tk.LEFT, padx=5)
        self.text_font_size_var = tk.StringVar(value=str(config.text_font_size))
        self.text_font_entry = ttk.Entry(
            font_frame, width=5, textvariable=self.text_font_size_var
        )
        self.text_font_entry.pack(side=tk.LEFT, padx=5)
        colors_frame = ttk.Frame(graph_settings_frame)
        colors_frame.pack(fill=tk.X, pady=5)
        ttk.Label(colors_frame, text="Bar colors:").pack(side=tk.LEFT, padx=5)
        self.bar_color_single_var = tk.StringVar(
            value=str(config.graph_bar_color_single)
        )
        ttk.Entry(colors_frame, width=10, textvariable=self.bar_color_single_var).pack(
            side=tk.LEFT, padx=2
        )
        self.bar_color_compare1_var = tk.StringVar(
            value=str(config.graph_bar_color_compare1)
        )
        ttk.Entry(
            colors_frame, width=10, textvariable=self.bar_color_compare1_var
        ).pack(side=tk.LEFT, padx=2)
        self.bar_color_compare2_var = tk.StringVar(
            value=str(config.graph_bar_color_compare2)
        )
        ttk.Entry(
            colors_frame, width=10, textvariable=self.bar_color_compare2_var
        ).pack(side=tk.LEFT, padx=2)
        buttons_frame = ttk.Frame(config_tab)
        buttons_frame.pack(fill=tk.X, pady=20)
        save_btn = ttk.Button(
            buttons_frame, text="Save settings", command=self.save_config
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        cancel_btn = ttk.Button(
            buttons_frame, text="Cancel changes", command=self.reset_last_save_config
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        reset_btn = ttk.Button(
            buttons_frame,
            text="Reset values to default",
            command=self.reset_default_config,
        )
        reset_btn.pack(side=tk.RIGHT, padx=5)
        info_frame = ttk.Frame(config_tab)
        info_frame.pack(fill=tk.X, pady=10)
        info_text = tk.Text(info_frame, height=5, wrap=tk.WORD)
        info_text.pack(fill=tk.X, padx=10)
        info_text.insert(
            tk.END,
            "These settings control how many words are displayed in the word lists and graphs. Changes will be saved to the configuration file and applied immediately once the save button is pressed.",
        )
        info_text.config(state=tk.DISABLED)

    def browse_file1(self):
        """
        Open a file dialog to browse for a file to analyze.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        ):
            self.file_entry1.delete(0, tk.END)
            self.file_entry1.insert(0, file_path)
            self.file_path1 = file_path

    def browse_compare_file1(self):
        """
        Open a file dialog to browse for the first file to compare.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        ):
            self.compare_file_entry1.delete(0, tk.END)
            self.compare_file_entry1.insert(0, file_path)

    def browse_compare_file2(self):
        """
        Open a file dialog to browse for the second file to compare.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        ):
            self.compare_file_entry2.delete(0, tk.END)
            self.compare_file_entry2.insert(0, file_path)

    def browse_compare_file2_nltk(self):
        """
        Open a file dialog to browse for the a set of reference files to compare.
        Updates the file path entry field with the selected path.
        """
        if file_path := filedialog.askopenfilenames(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        ):
            self.compare_file_entry2.delete(0, tk.END)
            for file in file_path[:-1]:
                self.compare_file_entry2.insert(tk.END, file.replace(",", ",\\") + ", ")
            self.compare_file_entry2.insert(tk.END, file_path[-1].replace(",", ",\\"))

    def browse_search_file(self):
        """Browse for a file to search."""
        if file_path := filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        ):
            self.search_file_entry.delete(0, tk.END)
            self.search_file_entry.insert(0, file_path)

    def browse_replace_file(self):
        """Browse for a file to perform word replacement."""
        if file_path := filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        ):
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
        total_words = len(clean_content.split(" "))
        unique_words = len(word_count[0])
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
        self.stats_text.insert(tk.END, f"Total words: {total_words}\n")
        self.stats_text.insert(tk.END, f"Unique words: {unique_words}\n")
        self.freq_list.delete(0, tk.END)
        freq_sorted = sort_by_frequency(word_count)[: config.analyze_max_words]
        for i, (word, count) in enumerate(freq_sorted):
            self.freq_list.insert(tk.END, f'{i + 1}. "{word}": {count} times')
        self.alpha_list.delete(0, tk.END)
        alpha_sorted = sort_alphabetically(word_count)[: config.analyze_max_words]
        for i, (word, count) in enumerate(alpha_sorted):
            self.alpha_list.insert(tk.END, f'{i + 1}. "{word}": {count} times')
        self.analyze_graph_cmd = f"self.create_frequency_graph({word_count}, self.analyze_canvas, self.analyze_canvas)"
        eval(self.analyze_graph_cmd)

    def create_frequency_graph(
        self,
        word_count,
        canvas_frame_widget,
        canvas_widget,
        max_words=config.graph_max_words,
    ):
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
        for widget in canvas_widget.winfo_children():
            widget.destroy()
        plt.close()
        for widget in canvas_frame_widget.winfo_children():
            if widget.winfo_id() != canvas_widget.winfo_id():
                widget.destroy()
        freq_sorted = sort_by_frequency(word_count)
        top_words = freq_sorted[:max_words]
        if not top_words:
            return
        fig, ax = plt.subplots(figsize=config.graph_figsize)
        words = [word for word, _ in top_words][::-1]
        counts = [count for _, count in top_words][::-1]
        bars = ax.barh(words, counts, color=config.graph_bar_color_single)
        ax.set_xlabel("Frequency", fontsize=config.graph_label_fontsize)
        ax.set_title("Top Word Frequencies", fontsize=config.graph_title_fontsize)
        ax.tick_params(labelsize=config.graph_label_fontsize)
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 0.1,
                bar.get_y() + bar.get_height() / 2,
                f"{width}",
                ha="left",
                va="center",
            )
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame_widget)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

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
        content1 = read_file(file_path1)
        if content1 is None:
            messagebox.showerror("Error", f"Could not read file: {file_path1}")
            return
        if self.compare_nltk.get() and get_similarity_score is None:
            self.compare_nltk.set(False)
            file_path2 = file_path2.split(", ")[0].replace(",\\", ",")
            print(
                "\x1b[33mWarning: some required modules in nltk_plagiarism module is missing, or is corrupted. Please (re)install the necesserary modules by running `python -m pip install nltk scikit-learn` in the terminal\x1b[m"
            )
            messagebox.showerror(
                "Error",
                "there are some errors trying to use cosine similarity (nltk), jaccard(?) similarity is used instead. Please refer to the error message in the terminal",
            )
        if self.compare_nltk.get():
            file_paths = []
            for file in file_path2.split(", "):
                if file:
                    file_paths.append(file.replace(",\\", ","))
            reference_contents = []
            reference_file_names = []
            for path in file_paths:
                content = read_file(path)
                if content is None:
                    messagebox.showerror("Error", f"Could not read file: {path}")
                    return
                reference_contents.append(content)
                reference_file_names.append(os.path.basename(path))
            clean_content1 = clean_text(content1)
            word_count1 = count_words(clean_content1)
            total_words1 = len(clean_content1.split(" "))
            unique_words1 = len(word_count1[0])
            self.file1_stats_text.delete(1.0, tk.END)
            self.file1_stats_text.insert(
                tk.END, f"File: {os.path.basename(file_path1)}\n"
            )
            self.file1_stats_text.insert(tk.END, f"Total words: {total_words1}\n")
            self.file1_stats_text.insert(tk.END, f"Unique words: {unique_words1}\n")
            self.file2_stats_text.delete(1.0, tk.END)
            self.file2_stats_text.insert(
                tk.END, f"Reference Files: {len(file_paths)}\n"
            )
            total_words2 = 0
            unique_words = []
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
                self.file2_stats_text.insert(
                    tk.END, f"File {i + 1}: {reference_file_names[i]}\n"
                )
            self.file2_stats_text.insert(
                tk.END, f"Total words across all files: {total_words2}\n"
            )
            self.file2_stats_text.insert(
                tk.END, f"Unique words across all files: {len(unique_words)}\n"
            )
            plagiarism_results = get_similarity_score(content1, reference_contents)
            self.comparison_text.delete(1.0, tk.END)
            similarity_scores = [0] * len(reference_contents)
            if plagiarism_results:
                max_similarity = helpers.max(
                    (result[1] for result in plagiarism_results)
                )
                similarity = max_similarity * 100
                self.comparison_text.insert(
                    tk.END, f"Similarity percentage: {similarity:.2f}%\n"
                )
                self.comparison_text.insert(tk.END, "Matches found in:\n")
                for i, result in enumerate(plagiarism_results):
                    score = result[1] * 100
                    match_index = helpers.linear_search(reference_contents, result[0])
                    file_name = reference_file_names[match_index]
                    similarity_scores[match_index] = score
                    self.comparison_text.insert(
                        tk.END,
                        f"Match {i + 1}: {file_name} - {score:.2f}% similarity\n",
                    )
            else:
                similarity = 0
                self.comparison_text.insert(
                    tk.END, "No significant similarity detected\n"
                )
                self.comparison_text.insert(tk.END, "Similarity percentage: 0.00%\n")
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
            if reference_word_counts:
                self.compare_graph_cmd = f"self.create_nltk_comparison_graph({word_count1}, {reference_word_counts}, '{os.path.basename(file_path1)}', {reference_file_names}, {similarity_scores}, self.compare_graph_frame, self.compare_canvas)"
                eval(self.compare_graph_cmd)
        else:
            content2 = read_file(file_path2)
            if content2 is None:
                messagebox.showerror("Error", f"Could not read file: {file_path2}")
                return
            clean_content1 = clean_text(content1)
            clean_content2 = clean_text(content2)
            word_count1 = count_words(clean_content1)
            word_count2 = count_words(clean_content2)
            total_words1 = len(clean_content1.split(" "))
            total_words2 = len(clean_content2.split(" "))
            unique_words1 = len(word_count1[0])
            unique_words2 = len(word_count2[0])
            self.file1_stats_text.delete(1.0, tk.END)
            self.file1_stats_text.insert(
                tk.END, f"File: {os.path.basename(file_path1)}\n"
            )
            self.file1_stats_text.insert(tk.END, f"Total words: {total_words1}\n")
            self.file1_stats_text.insert(tk.END, f"Unique words: {unique_words1}\n")
            self.file2_stats_text.delete(1.0, tk.END)
            self.file2_stats_text.insert(
                tk.END, f"File: {os.path.basename(file_path2)}\n"
            )
            self.file2_stats_text.insert(tk.END, f"Total words: {total_words2}\n")
            self.file2_stats_text.insert(tk.END, f"Unique words: {unique_words2}\n")
            similarity = calculate_similarity(word_count1, word_count2)
            self.comparison_text.delete(1.0, tk.END)
            self.comparison_text.insert(
                tk.END,
                f"Similarity percentage of\ntext 1: {similarity[0]:.2f}%\ntext 2: {similarity[1]:.2f}%\n",
            )
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
            self.comparison_text.insert(tk.END, f"Plagiarism Level: {level}", "color")
            self.compare_graph_cmd = f"self.create_comparison_graph({word_count1}, {word_count2}, self.compare_graph_frame, self.compare_canvas)"
            eval(self.compare_graph_cmd)

    def create_comparison_graph(
        self,
        word_count1,
        word_count2,
        canvas_frame_widget,
        canvas_widget,
        max_words=config.graph_max_words,
    ):
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
        for widget in canvas_widget.winfo_children():
            widget.destroy()
        plt.close()
        for widget in canvas_frame_widget.winfo_children():
            if widget.winfo_id() != canvas_widget.winfo_id():
                widget.destroy()
        freq_sorted1 = sort_by_frequency(word_count1)
        freq_sorted2 = sort_by_frequency(word_count2)
        combined_top_words = []
        top_words1 = []
        for word, _ in freq_sorted1[:max_words]:
            if word not in top_words1:
                top_words1.append(word)
        for word, _ in freq_sorted2[:max_words]:
            if word in top_words1 and word not in combined_top_words:
                combined_top_words.append(word)
        if not combined_top_words:
            return
        counts1 = []
        counts2 = []
        for word in combined_top_words:
            idx = helpers.linear_search(word_count1[0], word)
            if idx != -1:
                counts1.append(word_count1[1][idx])
            else:
                counts1.append(0)
            idx = helpers.linear_search(word_count2[0], word)
            if idx != -1:
                counts2.append(word_count2[1][idx])
            else:
                counts2.append(0)
        fig, ax = plt.subplots(figsize=config.graph_figsize)
        x = range(len(combined_top_words))
        width = 0.35
        ax.bar(
            [i - width / 2 for i in x],
            counts1,
            width,
            label="File 1",
            color=config.graph_bar_color_compare1,
        )
        ax.bar(
            [i + width / 2 for i in x],
            counts2,
            width,
            label="File 2",
            color=config.graph_bar_color_compare2,
        )
        ax.set_ylabel("Frequency")
        ax.set_title("Word Frequency Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels(combined_top_words, rotation=45, ha="right")
        ax.legend()
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame_widget)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_nltk_comparison_graph(
        self,
        word_count1,
        reference_word_counts,
        file1_name,
        reference_file_names,
        similarity_scores,
        canvas_frame_widget,
        canvas_widget,
        max_words=config.graph_max_words,
    ):
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
        for widget in canvas_widget.winfo_children():
            widget.destroy()
        plt.close()
        for widget in canvas_frame_widget.winfo_children():
            if widget.winfo_id() != canvas_widget.winfo_id():
                widget.destroy()
        freq_sorted1 = sort_by_frequency(word_count1)
        top_words1 = []
        for word, _ in freq_sorted1[:max_words]:
            if word not in top_words1:
                top_words1.append(word)
        all_common_words = []
        for word_count2 in reference_word_counts:
            freq_sorted2 = sort_by_frequency(word_count2)
            for word, _ in freq_sorted2[:max_words]:
                if word in top_words1 and word not in all_common_words:
                    all_common_words.append(word)
        if not all_common_words:
            fig = plt.figure(figsize=config.graph_figsize)
            ax = fig.add_subplot(111)
            ax.text(
                0.5,
                0.5,
                "No common words found in top frequency lists",
                ha="center",
                va="center",
                fontsize=12,
            )
            ax.set_xticks([])
            ax.set_yticks([])
            plt.tight_layout()
            frame = ttk.Frame(canvas_widget)
            frame.pack(fill=tk.BOTH, expand=True)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            return
        all_common_words_sorted = helpers.quick_sort(
            all_common_words,
            key=lambda word: (
                word_count1[1][helpers.linear_search(word_count1[0], word)]
                if word in word_count1[0]
                else 0
            ),
            reverse=True,
        )
        display_words = all_common_words_sorted[:max_words]
        fig_height = helpers.max(
            config.graph_figsize[1], 2 + len(reference_word_counts) * 0.5
        )
        fig = plt.figure(figsize=(config.graph_figsize[0], fig_height))
        num_plots = len(reference_word_counts)
        if num_plots > 10:
            indices = helpers.quick_sort(
                range(len(similarity_scores)),
                key=lambda i: similarity_scores[i],
                reverse=True,
            )[:10]
            reference_word_counts = [reference_word_counts[i] for i in indices]
            reference_file_names = [reference_file_names[i] for i in indices]
            similarity_scores = [similarity_scores[i] for i in indices]
            num_plots = 10
        for i in range(num_plots):
            ax = fig.add_subplot(num_plots, 1, i + 1)
            counts1 = []
            counts2 = []
            for word in display_words:
                if word in word_count1[0]:
                    idx = helpers.linear_search(word_count1[0], word)
                    counts1.append(word_count1[1][idx])
                else:
                    counts1.append(0)
                word_count2 = reference_word_counts[i]
                if word in word_count2[0]:
                    idx = helpers.linear_search(word_count2[0], word)
                    counts2.append(word_count2[1][idx])
                else:
                    counts2.append(0)
            x = range(len(display_words))
            width = 0.35
            ax.bar(
                [j - width / 2 for j in x],
                counts1,
                width,
                label=file1_name,
                color=config.graph_bar_color_compare1,
            )
            ax.bar(
                [j + width / 2 for j in x],
                counts2,
                width,
                label=f"{reference_file_names[i]} ({similarity_scores[i]:.1f}%)",
                color=config.graph_bar_color_compare2,
            )
            if i == 0:
                ax.set_title("Word Frequency Comparison with Reference Files")
            if i == num_plots // 2:
                ax.set_ylabel("Frequency")
            if i == num_plots - 1:
                ax.set_xticks(x)
                ax.set_xticklabels(display_words, rotation=45, ha="right")
            else:
                ax.set_xticks(x)
                ax.set_xticklabels([])
            ax.legend(loc="upper right", fontsize="small")
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame_widget)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

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
        file_path = self.search_file_entry.get()
        target_word = self.search_entry.get()
        regex = self.regex_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return
        if not target_word:
            messagebox.showerror(
                "Error", "Please enter a word or pattern to search for."
            )
            return
        content = read_file(file_path)
        if content is None:
            messagebox.showerror("Error", f"Could not read file: {file_path}")
            return
        positions = search_word_position(content, target_word, regex)
        self.search_results.config(state=tk.NORMAL)
        self.search_results.delete(1.0, tk.END)
        if positions:
            match_text = "pattern" if regex else "word"
            self.search_results.insert(
                tk.END,
                f'The {match_text} "{target_word}" appears {len(positions)} times\n',
            )
            self.search_results.tag_configure(
                "highlight", background="yellow", foreground="black"
            )
            words = content.split()
            for pos, matched_word in positions:
                start = helpers.max(0, pos - 3)
                end = helpers.min(len(words), pos + 4)
                prefix = "... " if pos > 3 else ""
                suffix = " ..." if pos + 4 < len(words) else ""
                self.search_results.insert(tk.END, f"Position {pos}: {prefix}")
                if start < pos:
                    self.search_results.insert(tk.END, " ".join(words[start:pos]) + " ")
                self.search_results.insert(tk.END, matched_word, "highlight")
                if pos + 1 < end:
                    self.search_results.insert(
                        tk.END, " " + " ".join(words[pos + 1 : end])
                    )
                self.search_results.insert(tk.END, f"{suffix}\n")
        else:
            match_text = "pattern" if regex else "word"
            self.search_results.insert(
                tk.END, f'The {match_text} "{target_word}" was not found in the file.'
            )
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
        file_path = self.replace_file_entry.get()
        target_word = self.word_entry.get()
        replacement_word = self.replacement_entry.get()
        regex = self.replace_regex_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return
        if not target_word:
            messagebox.showerror("Error", "Please enter a word or pattern to replace.")
            return
        content = read_file(file_path)
        if content is None:
            messagebox.showerror("Error", f"Could not read file: {file_path}")
            return
        self.original_text.config(state=tk.NORMAL)
        self.modified_text.tag_configure(
            "highlight", background="yellow", foreground="black"
        )
        self.original_text.tag_configure(
            "highlight", background="yellow", foreground="black"
        )
        self.modified_text.delete(1.0, tk.END)
        self.original_text.delete(1.0, tk.END)
        if regex:
            try:
                matches = list(re.finditer(target_word, content, flags=re.IGNORECASE))
                if matches:
                    last_end = 0
                    for match in matches:
                        self.original_text.insert(
                            tk.END, content[last_end : match.start()]
                        )
                        self.modified_text.insert(
                            tk.END, content[last_end : match.start()]
                        )
                        self.original_text.insert(
                            tk.END, content[match.start() : match.end()], "highlight"
                        )
                        self.modified_text.insert(tk.END, replacement_word, "highlight")
                        last_end = match.end()
                    self.original_text.insert(tk.END, content[last_end:])
                    self.modified_text.insert(tk.END, content[last_end:])
                else:
                    self.original_text.insert(tk.END, content)
                    self.modified_text.insert(tk.END, content)
            except re.error:
                messagebox.showerror("Error", "Invalid regular expression pattern.")
                return
        else:
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if not line.strip():
                    if i > 0:
                        self.original_text.insert(tk.END, "\n")
                        self.modified_text.insert(tk.END, "\n")
                    continue
                words = line.split()
                if not words:
                    if i > 0:
                        self.original_text.insert(tk.END, "\n")
                        self.modified_text.insert(tk.END, "\n")
                    continue
                positions = []
                for idx, word in enumerate(words):
                    clean_word = "".join(
                        (
                            c.lower()
                            for c in word
                            if alphanumerical(c) or c == "'" or c == "-"
                        )
                    )
                    if clean_word == target_word.lower():
                        positions.append(idx)
                if i > 0:
                    self.original_text.insert(tk.END, "\n")
                    self.modified_text.insert(tk.END, "\n")
                if positions:
                    current_pos = 0
                    for pos in positions:
                        if pos > current_pos:
                            self.original_text.insert(
                                tk.END, " ".join(words[current_pos:pos]) + " "
                            )
                            self.modified_text.insert(
                                tk.END, " ".join(words[current_pos:pos]) + " "
                            )
                        original_word = words[pos]
                        leading_punct = ""
                        trailing_punct = ""
                        i = 0
                        while i < len(original_word) and (
                            not alphanumerical(original_word[i])
                        ):
                            leading_punct += original_word[i]
                            i += 1
                        i = len(original_word) - 1
                        while i >= 0 and (not alphanumerical(original_word[i])):
                            trailing_punct = original_word[i] + trailing_punct
                            i -= 1
                        self.original_text.insert(tk.END, original_word, "highlight")
                        self.modified_text.insert(
                            tk.END,
                            leading_punct + replacement_word + trailing_punct,
                            "highlight",
                        )
                        if pos < len(words) - 1:
                            self.original_text.insert(tk.END, " ")
                            self.modified_text.insert(tk.END, " ")
                        current_pos = pos + 1
                    if current_pos < len(words):
                        self.original_text.insert(tk.END, " ".join(words[current_pos:]))
                        self.modified_text.insert(tk.END, " ".join(words[current_pos:]))
                else:
                    self.original_text.insert(tk.END, line)
                    self.modified_text.insert(tk.END, line)
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
        if not self.modified_text.get(1.0, tk.END).strip():
            messagebox.showerror("Error", "No modified text to save.")
            return
        if file_path := filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        ):
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.modified_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f'Modified text saved to "{file_path}"')
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def save_config(self):
        """
        Save the configuration settings to the config file.

        This method retrieves current user settings from the input fields,
        validates them, and updates the config accordingly. All changes are
        saved in the WAPDS.config file.
        """
        try:
            single_file_display = int(self.single_file_display_var.get())
            compare_file_display = int(self.compare_file_display_var.get())
            graph_max_words = int(self.graph_max_words_var.get())
            analyze_max_words = int(self.analyze_max_words_var.get())
            graph_width = float(self.graph_width_var.get())
            graph_height = float(self.graph_height_var.get())
            title_fontsize = float(self.title_font_var.get())
            label_fontsize = float(self.label_font_var.get())
            text_font_size = int(self.text_font_size_var.get())
            if helpers.any(
                (
                    x <= 0
                    for x in [
                        single_file_display,
                        compare_file_display,
                        graph_max_words,
                        analyze_max_words,
                        graph_width,
                        graph_height,
                        title_fontsize,
                        label_fontsize,
                    ]
                )
            ):
                messagebox.showerror(
                    "Error", "All numeric settings must be positive numbers."
                )
                return
            config.single_file_display_line = single_file_display
            config.compare_file_display_line = compare_file_display
            config.graph_max_words = graph_max_words
            config.analyze_max_words = analyze_max_words
            config.graph_figsize = [graph_width, graph_height]
            config.graph_title_fontsize = title_fontsize
            config.graph_label_fontsize = label_fontsize
            config.graph_bar_color_single = self.bar_color_single_var.get()
            config.graph_bar_color_compare1 = self.bar_color_compare1_var.get()
            config.graph_bar_color_compare2 = self.bar_color_compare2_var.get()
            config.text_font_size = text_font_size
            self.apply_theme()
            config.save()
            messagebox.showinfo("Configuration", "Settings saved successfully!")
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter valid numbers for both settings."
            )

    def reset_last_save_config(self):
        """
        Reset the configuration fields to their current values.

        This method resets the input fields to the last saved values
        from the configuration.
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
        self.text_font_size_var.set(str(config.text_font_size))
        self.apply_theme()

    def reset_default_config(self):
        """
        Reset the configuration fields to their default values.

        This method resets all fields in the configuration tab to their preset
        default values defined in the config class.
        """
        config.reset_to_defaults()
        self.theme_var.set(config.dark_mode)
        self.reset_last_save_config()
        messagebox.showinfo("Configuration", "Settings reset to default values.")


def configure_test_input(prompt, type, was, error=""):
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
        temp_unsaved = input(f"{prompt} (was {was}): ")
        if type is int:
            temp_unsaved = int(temp_unsaved)
            if temp_unsaved > 0:
                return temp_unsaved
            else:
                raise ValueError
        elif type is float:
            temp_unsaved = float(temp_unsaved)
            if temp_unsaved > 0:
                return temp_unsaved
            else:
                raise ValueError
        else:
            return type(temp_unsaved)
    except ValueError:
        print("\x1b[31mInvalid input. ", end="")
        if error:
            print(error, end="")
        elif type is int:
            print("Please enter a positive integer.", end="")
        elif type is float:
            print("Please enter a positive float.", end="")
        else:
            print("Please enter a valid string.", end="")
        print("\x1b[m")


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
    - Font sizes for titles, labels, and text
    """
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
        unsaved = False
        for unsaved_var in list(locals()):
            if unsaved_var in ("config_option", "unsaved", "unsaved_var"):
                continue
            if eval(unsaved_var) is not None:
                unsaved = True
        print(
            [
                [],
                [*f'Change settings{("(unsaved)" if unsaved else "")}:'],
                [],
                [*"CLI settings:"],
                [
                    "\x1b[1;4;97mA\x1b[m",
                    *f'nalyse file: show first {(config.single_file_display_line if unsaved_single_file_display_line is None else f"{unsaved_single_file_display_line} (was {config.single_file_display_line})")} sorted words appeared',
                ],
                [
                    "\x1b[1;4;97mC\x1b[m",
                    *f'ompare files: show first {(config.compare_file_display_line if unsaved_compare_file_display_line is None else f"{unsaved_compare_file_display_line} (was {config.compare_file_display_line})")} sorted words appeared',
                ],
                [],
                [*"GUI settings:"],
                [
                    "a",
                    "\x1b[1;4;97mN\x1b[m",
                    *f'alyse file: show first {(config.analyze_max_words if unsaved_analyze_max_words is None else f"{unsaved_analyze_max_words} (was {config.analyze_max_words})")} sorted words appeared',
                ],
                [
                    *"Graph: ",
                    "\x1b[1;4;97mM\x1b[m",
                    *f'ax word: show first {(config.graph_max_words if unsaved_graph_max_words is None else f"{unsaved_graph_max_words} (was {config.graph_max_words})")} sorted words appeared',
                ],
                [
                    *"Graph figure size: set the figure ",
                    "\x1b[1;4;97mH\x1b[m",
                    *f'eight to {(config.graph_figsize[1] if unsaved_graph_figsize_h is None else f"{unsaved_graph_figsize_h} (was {config.graph_figsize[1]})")}',
                ],
                [
                    *"Graph figure size: set the figure ",
                    "\x1b[1;4;97mW\x1b[m",
                    *f'idth to {(config.graph_figsize[0] if unsaved_graph_figsize_w is None else f"{unsaved_graph_figsize_w} (was {config.graph_figsize[0]})")}',
                ],
                [
                    *"Graph bar: set color of s",
                    "\x1b[1;4;97mI\x1b[m",
                    *f'ngle bar (analyse file) to {(config.graph_bar_color_single if unsaved_graph_bar_color_single is None else f"{unsaved_graph_bar_color_single} (was {config.graph_bar_color_single})")}',
                ],
                [
                    *"Graph bar: set color of File",
                    "\x1b[1;4;97m1\x1b[m",
                    *f"'s bar (compare file) to {(config.graph_bar_color_compare1 if unsaved_graph_bar_color_compare1 is None else f'{unsaved_graph_bar_color_compare1} (was {config.graph_bar_color_compare1})')}",
                ],
                [
                    *"Graph bar: set color of File",
                    "\x1b[1;4;97m2\x1b[m",
                    *f"'s bar (compare file) to {(config.graph_bar_color_compare2 if unsaved_graph_bar_color_compare2 is None else f'{unsaved_graph_bar_color_compare2} (was {config.graph_bar_color_compare2})')}",
                ],
                [
                    *"Graph ",
                    "\x1b[1;4;97mT\x1b[m",
                    *f'itle: set font size to {(config.graph_title_fontsize if unsaved_graph_title_fontsize is None else f"{unsaved_graph_title_fontsize} (was {config.graph_title_fontsize})")}',
                ],
                [
                    *"Graph ",
                    "\x1b[1;4;97mL\x1b[m",
                    *f'abel: set font size to {(config.graph_label_fontsize if unsaved_graph_label_fontsize is None else f"{unsaved_graph_label_fontsize} (was {config.graph_label_fontsize})")}',
                ],
                [
                    *"Text: set ",
                    "\x1b[1;4;97mF\x1b[m",
                    *f'ont size to {(config.text_font_size if unsaved_text_font_size is None else f"{unsaved_text_font_size} (was {config.text_font_size})")}',
                ],
                ["\x1b[1;4mS\x1b[m", *"ave and exit"],
                ["\x1b[1;4;97mE\x1b[m", *"xit without saving"],
            ],
            _override=True,
            wrap_override=True,
        )
        config_option = input("Enter option: ", single_letter=True).upper().strip()
        if config_option == "A":
            unsaved_single_file_display_line = configure_test_input(
                "Enter number of sorted words to display in Analyze File mode",
                int,
                str(config.single_file_display_line),
            )
        elif config_option == "C":
            unsaved_compare_file_display_line = configure_test_input(
                "Enter number of sorted words to display in Compare Files mode",
                int,
                str(config.compare_file_display_line),
            )
        elif config_option == "N":
            unsaved_analyze_max_words = configure_test_input(
                "Enter number of sorted words to display in Analyze File mode",
                int,
                str(config.analyze_max_words),
            )
        elif config_option == "M":
            unsaved_graph_max_words = configure_test_input(
                "Enter number of sorted words to display in the result figure",
                int,
                str(config.graph_max_words),
            )
        elif config_option == "H":
            unsaved_graph_figsize_h = configure_test_input(
                "Enter height of the figure", float, str(config.graph_figsize[1])
            )
        elif config_option == "W":
            unsaved_graph_figsize_w = configure_test_input(
                "Enter width of the figure", float, str(config.graph_figsize[0])
            )
        elif config_option == "I":
            unsaved_graph_bar_color_single = configure_test_input(
                "Enter color of the bar in Analyze File mode",
                str,
                str(config.graph_bar_color_single),
            )
        elif config_option == "1":
            unsaved_graph_bar_color_compare1 = configure_test_input(
                "Enter color of File1's bar in Compare Files mode",
                str,
                str(config.graph_bar_color_compare1),
            )
        elif config_option == "2":
            unsaved_graph_bar_color_compare2 = configure_test_input(
                "Enter color of File2's bar in Compare Files mode",
                str,
                str(config.graph_bar_color_compare2),
            )
        elif config_option == "T":
            unsaved_graph_title_fontsize = configure_test_input(
                "Enter font size of the figure's title",
                float,
                str(config.graph_title_fontsize),
            )
        elif config_option == "L":
            unsaved_graph_label_fontsize = configure_test_input(
                "Enter font size of the figure's labels",
                float,
                str(config.graph_label_fontsize),
            )
        elif config_option == "F":
            unsaved_text_font_size = configure_test_input(
                "Enter font size of the text labels", int, str(config.text_font_size)
            )
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
        if unsaved_text_font_size is not None:
            config.text_font_size = unsaved_text_font_size
        config.save()
        print("Saved!")


def search_word(file_path, target_word):
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
            print(
                f'The word "{target_word}" appears {len(positions)} times at positions: {", ".join((str(pos[0]) for pos in positions))}'
            )
            return
    print(f'The word "{target_word}" was not found in the file.')


def replace_word(file_path, target_word, replacement_word):
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
        lines = content.split("\n")
        modified_lines = []
        for line in lines:
            if not line.strip():
                modified_lines.append("")
                continue
            words = line.split()
            modified_line = ""
            current_pos = 0
            positions = []
            for idx, word in enumerate(words):
                clean_word = "".join(
                    (
                        c.lower()
                        for c in word
                        if alphanumerical(c) or c == "'" or c == "-"
                    )
                )
                if clean_word == target_word.lower():
                    positions.append(idx)
            if positions:
                current_pos = 0
                for pos in positions:
                    modified_line += " ".join(words[current_pos:pos]) + (
                        " " if current_pos < pos else ""
                    )
                    original_word = words[pos]
                    leading_punct = ""
                    trailing_punct = ""
                    i = 0
                    while i < len(original_word) and (
                        not alphanumerical(original_word[i])
                    ):
                        leading_punct += original_word[i]
                        i += 1
                    i = len(original_word) - 1
                    while i >= 0 and (not alphanumerical(original_word[i])):
                        trailing_punct = original_word[i] + trailing_punct
                        i -= 1
                    modified_line += leading_punct + replacement_word + trailing_punct
                    if pos < len(words) - 1:
                        modified_line += " "
                    current_pos = pos + 1
                if current_pos < len(words):
                    modified_line += " ".join(words[current_pos:])
            else:
                modified_line = line
            modified_lines.append(modified_line)
        modified_content = "\n".join(modified_lines)
        print(
            f"\nOriginal text:\n{(content[:100] + '...' if len(content) > 100 else content)}\n\nModified text:\n{(modified_content[:100] + '...' if len(modified_content) > 100 else modified_content)}"
        )
        save_option = input(
            "\nDo you want to save the modified text to a new file? (y/n): ",
            single_letter=True,
        ).lower()
        if save_option == "y":
            new_file_path = input("Enter the path for the new file: ").strip()
            try:
                with open(new_file_path, "w", encoding="utf-8") as file:
                    file.write(modified_content)
                print(f'Modified text saved to "{new_file_path}"')
            except Exception as e:
                print(f"Error saving file: {str(e)}")


def display_results(
    file_path, word_count, total_words, unique_words, show_nums=10, wrap=None
):
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
        wrap (int | None): The terminal width to wrap text (default is the current terminal size)
    """
    show_nums = helpers.min(show_nums, len(word_count[0]))
    if wrap is None:
        wrap = os.get_terminal_size().columns
    hyphen_wrap = helpers.min(wrap, len(str(show_nums)) + 30)
    print(
        f"""\n{'=' * helpers.min(wrap, len(file_path) + 15)}\nAnalysis of "{file_path}":\n{'=' * helpers.min(wrap, len(file_path) + 15)}\nTotal words: {total_words}\nUnique words: {unique_words}\n\n\nTop {show_nums} Most Frequent Words:\n{'-' * hyphen_wrap}"""
    )
    frequency_sorted = sort_by_frequency(word_count)
    txt = "".join(
        (
            f'{i + 1}. "{word}": {count} times\n'
            for i, (word, count) in enumerate(frequency_sorted[:show_nums])
        )
    )
    print(txt)
    txt = f"""\nFirst {show_nums} Words (Alphabetically):\n{'-' * hyphen_wrap}\n"""
    alpha_sorted = sort_alphabetically(word_count)
    for i, (word, count) in enumerate(alpha_sorted[:show_nums]):
        txt += f'{i + 1}. "{word}": {count} times\n'
    print(txt)


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
    columns = os.get_terminal_size().columns
    content1 = read_file(file_path1)
    content2 = read_file(file_path2)
    if content1 is None or content2 is None:
        print("\x1b[31mError: Cannot compare files due to reading errors.\x1b[m")
        return
    clean_content1 = clean_text(content1)
    clean_content2 = clean_text(content2)
    word_count1 = count_words(clean_content1)
    word_count2 = count_words(clean_content2)
    total_words1 = len(clean_content1.split(" "))
    total_words2 = len(clean_content2.split(" "))
    unique_words1 = len(word_count1[0])
    unique_words2 = len(word_count2[0])
    display_results(
        file_path1,
        word_count1,
        total_words1,
        unique_words1,
        config.compare_file_display_line,
    )
    display_results(
        file_path2,
        word_count2,
        total_words2,
        unique_words2,
        config.compare_file_display_line,
    )
    similarity = calculate_similarity(word_count1, word_count2)
    print(
        f"""\n{'=' * helpers.min(columns, len(file_path1) + len(file_path2) + 30)}\nComparison between "{file_path1}" and "{file_path2}":\n{'=' * helpers.min(columns, len(file_path1) + len(file_path2) + 30)}\n\nSimilarity percentage of\ntext 1: {similarity[0]:.2f}%\ntext 2: {similarity[1]:.2f}%"""
    )
    similarity = helpers.max(similarity)
    if similarity > 80:
        print("\x1b[31mPlagiarism Level: HIGH - These texts are very similar\x1b[m")
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

    This function reads the specified file, cleans its content,
    counts words, determines total and unique word counts,
    and then displays results using display_results().

    Args:
        file_path (str): The path to the file to analyze
    """
    content = read_file(file_path)
    if content is None:
        return
    clean_content = clean_text(content)
    word_count = count_words(clean_content)
    total_words = len(clean_content.split(" "))
    unique_words = len(word_count[0])
    display_results(
        file_path,
        word_count,
        total_words,
        unique_words,
        config.single_file_display_line,
    )


def mainGUI():
    """
    Start the GUI version of the Word Analysis and Plagiarism Detection System.

    This function initializes the tkinter window, creates an instance of the application,
    and sets up a dialog confirmation when the user attempts to close the window.
    """
    root = tk.Tk()
    app = GUI_APP(root, config.window_size)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        if app.window_size is not None:
            config.window_size = app.window_size
            config.save()
        root.bind("<Configure>", lambda: None)
        root.destroy()
        raise KeyboardInterrupt from None


def mainCLI():
    """
    Start the CLI version of the Word Analysis and Plagiarism Detection System.

    This function presents a text-based menu interface for users to choose
    file analysis, comparison, configuration, and exit options.
    """
    columns = os.get_terminal_size().columns
    file_path = ""
    file_path2 = ""
    print(
        "Word Analysis and Plagiarism Detection System\n"
        + "-" * helpers.min(columns, 45)
    )
    while True:
        print(
            "\n\nMenu:\n1. Analyze a single file\n2. Compare two files for plagiarism\n3. Search for a word in a file\n4. Replace a word in a file\n5. Configure settings\n6. Exit\n"
        )
        choice = input("\nEnter your choice (1-6): ", single_letter=True)
        if choice in "1234":
            txt_files = [
                file
                for file in os.listdir()
                if os.path.isfile(file) and file.endswith(".txt")
            ]
            print(
                "Text files in current directory"
                + (
                    " (enter nothing to use the last chosen file)"
                    if file_path or file_path2
                    else ""
                )
                + ":\n"
                + "\n".join(txt_files)
            )
            if choice == "1":
                new_file_path = input(
                    "Enter the path to the text file"
                    + (f" (last chosen file: {file_path})" if file_path else "")
                    + ": "
                ).strip()
                if new_file_path != "":
                    file_path = new_file_path
                analyze_file(file_path)
            elif choice == "2":
                new_file_path = input(
                    "Enter the path to the first text file"
                    + (f" (last chosen: {file_path})" if file_path else "")
                    + ": "
                ).strip()
                new_file_path2 = input(
                    "Enter the path to the second text file"
                    + (f" (last chosen: {file_path2})" if file_path2 else "")
                    + ": "
                ).strip()
                if new_file_path != "":
                    file_path = new_file_path
                if new_file_path2 != "":
                    file_path2 = new_file_path2
                compare_files(file_path, file_path2)
            elif choice == "3":
                new_file_path = input(
                    "Enter the path to the text file"
                    + (f" (last chosen: {file_path})" if file_path else "")
                    + ": "
                ).strip()
                target_word = input("Enter the word to search for: ").strip()
                if new_file_path != "":
                    file_path = new_file_path
                search_word(file_path, target_word)
            elif choice == "4":
                new_file_path = input(
                    "Enter the path to the text file"
                    + (f" (last chosen: {file_path})" if file_path else "")
                    + ": "
                ).strip()
                target_word = input("Enter the word to replace: ").strip()
                replacement_word = input("Enter the replacement word: ").strip()
                if new_file_path != "":
                    file_path = new_file_path
                replace_word(file_path, target_word, replacement_word)
        elif choice == "5":
            configure()
        elif choice == "6":
            print("Thank you for using WAPDS!")
            break
        else:
            print(
                f"Invalid choice {repr(choice)}. Please enter a number between 1 and 6."
            )


if __name__ == "__main__":
    some_text = "{width}x{height}"
    parser = argparse.ArgumentParser(
        description="Word Analysis and Plagiarism Detection System (WAPDS)"
    )
    parser.add_argument(
        "run_type",
        help='Enter "GUI" or "CLI" to determine which version should run, defaults to GUI',
        nargs="?",
        default="GUI",
    )
    parser.add_argument(
        "GUI_window_size",
        help=f"Enter in format of {some_text}, set the GUI window size and will be saved, defaults to last window size (currently {repr(config.window_size)})",
        nargs="?",
        default=config.window_size,
    )
    args = parser.parse_args()
    if args.run_type == "GUI":
        if plt is None:
            print(
                "\x1b[33mWarning: matplotlib is not found, or is corrupted. Please (re)install matplotlib by running `python -m pip install matplotlib` in the terminal\x1b[m"
            )
        GUI_window_size = args.GUI_window_size.strip()
        GUI_window_size_check = GUI_window_size.split("x")
        try:
            GUI_window_size_check = list(map(int, GUI_window_size_check))
            if len(GUI_window_size_check) != 2:
                raise ValueError
            for n in GUI_window_size_check:
                if n <= 0:
                    raise ValueError
                elif n < 150:
                    raise TypeError
        except ValueError:
            if GUI_window_size == config.window_size:
                config.reset_to_defaults()
            else:
                parser.error(
                    f"Please enter GUI window size in the format of {some_text}, not {repr(GUI_window_size)}"
                )
        except TypeError:
            if GUI_window_size == config.window_size:
                config.reset_to_defaults()
            else:
                parser.error(
                    f"GUI is too small ({GUI_window_size}), please keep the window size larger than 150x150"
                )
        config.window_size = GUI_window_size
        config.save()
        mainGUI()
    elif args.run_type == "CLI":
        from helpers import animated_input as input
        from helpers import animated_print as print

        mainCLI()
    else:
        parser.error(
            f'Please enter either "GUI" or "CLI" for run type, not {repr(args.run_type)}'
        )

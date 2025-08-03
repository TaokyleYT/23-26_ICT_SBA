# Word Analysis and Plagiarism Detection System

> ⚠️ Before using this program, please make sure that your local environment is\
> at least Python 3.9+ (Recommended 3.10+) for normal version or\
> at least Python 3.5+ (Recommended 3.8+)for LowVerPy version\
> (Theoretically, LowVerPy versions can be run with Python 3.3+, but code stability is not guaranteed, and errors will occur)

<div align="center">
<h1 size="300%">
WAPDS<br>
Word Analysis and Plagiarism Detection System
</h1>
<img alt="" src="https://img.shields.io/badge/python-3.3_%7C_3.4-EF0000" />
<img alt="" src="https://img.shields.io/badge/3.5_%7C_3.6_%7C_3.7_%7C_3.8-FFCC22" />
<img alt="" src="https://img.shields.io/badge/3.9-yellow" />
<img alt="" src="https://img.shields.io/badge/3.10_%7C_3.11_%7C_3.12_%7C_3.13_%7C_3.14-green" />
<img alt="" src="https://img.shields.io/github/commit-activity/y/TaokyleYT/WAPDS" />
<img alt="" src="https://img.shields.io/github/last-commit/TaokyleYT/WAPDS" />
<img alt="" src="https://img.shields.io/github/contributors-anon/TaokyleYT/WAPDS" />
<img alt="" src="https://img.shields.io/github/issues/TaokyleYT/WAPDS">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/TaokyleYT/WAPDS">
<img alt="GitHub repo file or directory count" src="https://img.shields.io/github/directory-file-count/TaokyleYT/WAPDS">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/TaokyleYT/WAPDS">
<p>WAPDS is a system that analyzes texts and detects plagiarism across different texts. </p>

</div>

## How to use

1. First use git to clone this project `git clone https://github.com/TaokyleYT/WAPDS`
2. Switch directory `cd ./WAPDS/`
3. Run the main script `python main.py`

Running `main.py` defaults to GUI mode. To run in CLI mode, use `python main.py CLI`.\
More details about command line options can be found from `python main.py -h`.

## Functions

### CLI & GUI

- [x] Text count
- [x] Unique word count
- [x] Word frequency
- [x] Overlap coefficient based plagiarism detection
- [x] Word finder
- [x] Word replacer
- [x] Persistent configuration
- [x] Remembering previously selected text files

### GUI

- [x] Graphs on word frequency
- [x] Cosine similarity based plagiarism detection
- [x] Multiple reference texts supported for cosine similarity based plagiarism detection
- [x] Highlighted word finder
- [x] Interactive word replacer
- [ ] Text difference

## TODO

- [ ] Make the result from CLI word finder more readable
- [ ] Find the optimal speed for CLI print animation
- [ ] Make the GUI graphs more useful
- [ ] Make the GUI more beautiful
- [ ] Integrate GUI exclusive functions to CLI

## Known issues

- [ ] CLI: on windows, input requires user to press enter twice
- [ ] GUI: graphs are not quite readable

## Technology stack

### main.py

| Module | Purpose | Reference |
| ---- | ---- | ---- |
| os | terminal size detection and file operations | <https://docs.python.org/3/library/os.html> |
| re | regex matching features | <https://docs.python.org/3/library/re.html> |
| tkinter | GUI | <https://docs.python.org/3/library/tkinter.html> |
| numpy (**EXTERN LIB**) | For matching values from graphs with results from nltk_tools<br>(included in scikit-learn installation, this import batches with importing nltk_tools) | <https://scikit-learn.org> |
| matplotlib (**EXTERN LIB**) | plotting graphs on GUI | <https://matplotlib.org> |
| argparse | For parsing command line arguments | <https://docs.python.org/3/library/argparse.html> |

### helpers.py

| Module | Purpose | Reference |
| ---- | ---- | ---- |
| os | temporarily overriding the terminal's settings used by animated print/input | <https://docs.python.org/3/library/os.html> |
| re | Extracting data from ANSI commands used by animated print/input | <https://docs.python.org/3/library/re.html> |
| string | For grabbing printable characters | <https://docs.python.org/3/library/string.html> |
| sys | For checking OS type and providing raw stdin&stdout ports | <https://docs.python.org/3/library/sys.html> |
| time | For implementing delays for animated print/input | <https://docs.python.org/3/library/time.html> |
| ctypes | For controlling console in Windows | <https://docs.python.org/3/library/ctypes.html> |
| termios | For controlling terminal settings on Unix/Linux | <https://docs.python.org/3/library/termios.html> |
| tty | For setting terminal to character-by-character input mode on Unix/Linux | <https://docs.python.org/3/library/tty.html> |

### nltk_tools.py

| Module | Purpose | Reference |
| ---- | ---- | ---- |
| os | Checking nltk data cache | <https://docs.python.org/3/library/os.html> |
| nltk (**EXTERN LIB**) | For tokenizing texts and creating word vectors | <https://www.nltk.org> |
| scikit-learn (**EXTERN LIB**) | For calculating cosine similarity between word vectors | <https://scikit-learn.org> |

## Disclaimer

Copyright © 2025 Taokyle. All rights reserved.

WAPDS is an application for submission of 2026 Hong Kong Diploma of Secondary Education Examination *[HKDSE](https://en.wikipedia.org/wiki/Hong_Kong_Diploma_of_Secondary_Education)* and Information and Communications Technology *
[ICT](https://www.hkeaa.edu.hk/en/hkdse/hkdse_subj.html?A2&2&16)* School-Based Assessment *
[SBA](https://www.hkeaa.edu.hk/en/sba/introduction)*. For more details on this application, please refer to the report.

Copyright 2025 Taokyle. license under *
[GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)*

This file is part of WAPDS.\
WAPDS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\
WAPDS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. \
See the GNU General Public License for more details.\
You should not have received a copy of the GNU General Public License along with WAPDS because Im too lazy to add it.\
Therefore to get that copy urself, see <https://www.gnu.org/licenses/>.

## Below are the marking schemes I copied directly from my teacher

### Task 1 (Design & Implementation)

Write a Python program to analyze articles from text files. The program should:

- Count the number of words in a text file.
- Sort the vocabulary alphabetically and by frequency.
- Check for potential plagiarism by comparing two articles and calculating their percentage of similarity based on word frequencies.

**Complete the following tasks:**\
(a) Select suitable data types and data structures.

- Justify your choices (e.g. dictionaries for word frequencies, lists for sorting).

(b) Count word frequencies in the text.

- Ignore case differences (e.g. "Hello" and "hello" are treated as the same word).
- Exclude punctuation marks and spaces during counting.

(c) Sort the vocabulary.

- Alphabetically (e.g. A-Z).
- By frequency (e.g. most to least frequent).

(d) Compare two articles and calculate similarity percentage.

- Design an algorithm to compare word frequencies between two text files.
- Calculate the percentage of similarity using a formula (e.g. (common_words / total_unique_words) \* 100).

(e) Use stepwise refinement to describe the algorithm.

- Break down the process into modular steps (e.g. file input, data cleaning, counting, sorting, comparison).

\
*You may want to consider some of the following key factors when designing the program:*\
\
*Use functions to ensure a modular approach (e.g. read_file(), count_words(), calculate_similarity()).*\
*Validate input files (e.g. check if files exist and are non-empty).*\
*Handle errors gracefully (e.g. invalid file paths, empty files).*\
*Ensure clear output (e.g. display word counts, sorted lists, similarity percentage).*\
*Search for a target word, and/or replace it with another word.*

\
**Deliverables:**

- Python program code.
- Documentation explaining your design choices and algorithms.

*Notes:*\
*Ensure your program handles edge cases (e.g. empty files, non-text formats).*\
*Focus on readability and reusability (e.g. add comments, avoid hard-coded paths).*

### Task 2 (Testing & Evaluation)

**Test your program and evaluate its performance.**\
(a) Conduct a test using the following test cases:

- Test Case 1: Two identical articles (similarity percentage should be 100%).
- Test Case 2: Two completely different articles (similarity percentage should be <15%).
- Test Case 3: Articles with partial overlaps (e.g. ~50% shared vocabulary).

(b) Record feedback and results.

- Document the accuracy of word counts, sorting, and similarity calculations.
- Identify limitations (e.g. case sensitivity, handling hyphenated words).

(c) Improve the program.

- Option 1: make one major change in the program and illustrate the corresponding improvement.
- Option 2: describe how the scope of the program could be extended.

**Create a document to illustrate the development of the program. You may want to consider some of the following:**

- Compare pros and cons of your initial design.
- Discuss algorithm optimization (e.g. improving efficiency for large files).
- Include screenshots of test results and code snippets in your report.

**Deliverables:**

- Report detailing test results, improvements, and reflections on the program’s design.

## Marking Scheme

### Task 1: Design & Implementation (25 marks)

#### 1. Program Functionality (15 marks)

**Word Counting**\
Fully functional.\
Handles edge cases and is efficient for large files.\
Demonstrates effective and comprehensive data processing.\
Output is clear and well-formatted.\
Efficient and optimized.

**Vocabulary Sorting**\
Efficient sorting with clear output.\
Handles both alphabetical and frequency sorting flawlessly.\
Works well even for large datasets.\
Demonstrates appropriate ICT skills coherently and effectively.\
Output is easy to interpret and use.

**Plagiarism Detection**\
Advanced plagiarism detection.\
Handles edge cases and calculates similarity efficiently.\
Creates an appropriate output format that can easily be tested.\
Demonstrates innovative use of algorithms or techniques.\
Output is comprehensive and accurate.

#### 2. Code Quality (5 marks)

Code is well-structured and modular.\
Functions are reusable and follow the DRY (Don’t Repeat Yourself) principle.\
Code is thoroughly commented with clear explanations.\
Variable and function names are meaningful and follow naming conventions.\
Error handling is comprehensive and user-friendly.

#### 3. Design (5 marks)

Algorithm is well-designed and efficient.\
Demonstrates a clear understanding of the problem and provides an optimal solution.\
Uses appropriate data structures and techniques (e.g., dictionaries, sets, sorting algorithms).\
Handles edge cases gracefully (e.g., empty inputs, large datasets).\
Algorithms are clearly documented with step-by-step explanations or flowcharts.

### Task 2: Testing & Evaluation (15 marks)

#### 1. Test Plan Design (3 marks)

Test plan is comprehensive and well-structured.\
Clearly defines objectives, scope, and methodology for testing.\
Includes detailed steps for executing test cases.\
Identifies all relevant test scenarios (e.g., edge cases, normal cases).\
Demonstrates a clear understanding of the program’s functionality and potential issues.

#### 2. Test Cases, Records of test results & Evaluation (8 marks)

Test cases cover all relevant scenarios (e.g., edge cases, normal cases).\
Records of test results are detailed and well-organized.\
Evaluation of results is thorough and identifies all issues.\
Demonstrates a clear understanding of expected vs. actual outcomes.\
Includes suggestions for improvement based on test results.

#### 3. Program Improvement (4 marks)

Implements a major enhancement with a clear impact on functionality.\
Demonstrates innovative use of algorithms or techniques.\
Clearly explains the improvement and its benefits.\
Includes detailed documentation of the changes made.\
Shows a significant improvement in program performance or usability.

## WOO HERES WHAT I WILL DO

```none
command line & GUI (?)
CAN USE PYGAME WOOOO
(use tkinter instead bc hav matplotlib)
COLORED TEXT WITH ANSI ESCAPE WHY NOT
test case would be hard but okay maybe try try
count word: no special
sort: QUICK SORT ALL THE WAY
plagiarism: different test types, like word frequency, sentence matching, shows top matching results and stuff idk
plagiarism: might use the same concept of autocorrect system to detect

note: can use matplotlib or ascii graph to show result instead of numbers
(matplotlib implemented into GUI, ascii graph prob rejected)

should I train a big ahh neural network for plagiarism? idk it seemed a bit overkill lol
```

## WOOO SOME BUGS I AINT FIXIN FOR NOTHIN

```none
So far so good
```

## WOOO SOME FIXED BUGS MS LUO AINT FINDIN FOR NOTHIN

```none
CLI:
font size setting in CLI shows graph label instead :/
GUI:
multiple file selected to compare, nltk die die, file dont select first only
```

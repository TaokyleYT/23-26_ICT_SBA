# 23-26_ICT_SBA
wooooo my SBA for absolutely no reason (I mean I have reason, which is DSE, well idk aaaaaaaa)

# Word Analysis and Plagiarism Detection System
## Task 1 (Design & Implementation)
- Write a Python program to analyze articles from text files. The program should:
- Count the number of words in a text file.
- Sort the vocabulary alphabetically and by frequency.
- Check for potential plagiarism by comparing two articles and calculating their percentage of similarity based on word frequencies.

**Complete the following tasks:**<br>
<br>(a) Select suitable data types and data structures.<br>
* Justify your choices (e.g. dictionaries for word frequencies, lists for sorting).

<br>(b) Count word frequencies in the text.<br>
* Ignore case differences (e.g. "Hello" and "hello" are treated as the same word).
* Exclude punctuation marks and spaces during counting.

<br>(c) Sort the vocabulary.<br>
* Alphabetically (e.g. A-Z).
* By frequency (e.g. most to least frequent).

<br>(d) Compare two articles and calculate similarity percentage.<br>
* Design an algorithm to compare word frequencies between two text files.
* Calculate the percentage of similarity using a formula (e.g. (common_words / total_unique_words) * 100).

<br>(e) Use stepwise refinement to describe the algorithm.<br>
* Break down the process into modular steps (e.g. file input, data cleaning, counting, sorting, comparison).

<br><br><br>
*You may want to consider some of the following key factors when designing the program:*<br><br>
<i>
Use functions to ensure a modular approach (e.g. read_file(), count_words(), calculate_similarity()).<br>
Validate input files (e.g. check if files exist and are non-empty).<br>
Handle errors gracefully (e.g. invalid file paths, empty files).<br>
Ensure clear output (e.g. display word counts, sorted lists, similarity percentage).<br>
Search for a target word, and/or replace it with another word.<br>
</i>
<br><br>
**Deliverables:**<br>
- Python program code.
- Documentation explaining your design choices and algorithms.


<i>
Notes:<br>
Ensure your program handles edge cases (e.g. empty files, non-text formats).<br>
Focus on readability and reusability (e.g. add comments, avoid hard-coded paths).<br>
</i>


## Task 2 (Testing & Evaluation)
**Test your program and evaluate its performance.**<br>
<br>(a) Conduct a test using the following test cases:<br>
- Test Case 1: Two identical articles (similarity percentage should be 100%).<br>
- Test Case 2: Two completely different articles (similarity percentage should be <15%).<br>
- Test Case 3: Articles with partial overlaps (e.g. ~50% shared vocabulary).<br>

<br>(b) Record feedback and results.<br>
- Document the accuracy of word counts, sorting, and similarity calculations.<br>
- Identify limitations (e.g. case sensitivity, handling hyphenated words).<br>

<br>(c) Improve the program.<br>
- Option 1: make one major change in the program and illustrate the corresponding improvement.<br>
- Option 2: describe how the scope of the program could be extended.<br>

**Create a document to illustrate the development of the program. You may want to consider some of the following:**<br>
- Compare pros and cons of your initial design.<br>
- Discuss algorithm optimization (e.g. improving efficiency for large files).<br>
- Include screenshots of test results and code snippets in your report.<br>

**Deliverables:**
- Report detailing test results, improvements, and reflections on the program’s design.<br>


# Marking Scheme

## Task 1: Design & Implementation (25 marks)

### 1. Program Functionality (15 marks)

**Word Counting**<br>
Fully functional.<br>
Handles edge cases and is efficient for large files.<br>
Demonstrates effective and comprehensive data processing.<br>
Output is clear and well-formatted.<br>
Efficient and optimized.<br>


**Vocabulary Sorting**<br>
Efficient sorting with clear output.<br>
Handles both alphabetical and frequency sorting flawlessly.<br>
Works well even for large datasets.<br>
Demonstrates appropriate ICT skills coherently and effectively.<br>
Output is easy to interpret and use.<br>


**Plagiarism Detection**<br>
Advanced plagiarism detection.<br>
Handles edge cases and calculates similarity efficiently.<br>
Creates an appropriate output format that can easily be tested.<br>
Demonstrates innovative use of algorithms or techniques.<br>
Output is comprehensive and accurate.<br>


### 2. Code Quality (5 marks) 

Code is well-structured and modular.<br>
Functions are reusable and follow the DRY (Don’t Repeat Yourself) principle.<br>
Code is thoroughly commented with clear explanations.<br>
Variable and function names are meaningful and follow naming conventions.<br>
Error handling is comprehensive and user-friendly.<br>


### 3. Design (5 marks)

Algorithm is well-designed and efficient.<br>
Demonstrates a clear understanding of the problem and provides an optimal solution.<br>
Uses appropriate data structures and techniques (e.g., dictionaries, sets, sorting algorithms).<br>
Handles edge cases gracefully (e.g., empty inputs, large datasets).<br>
Algorithms are clearly documented with step-by-step explanations or flowcharts.<br>



## Task 2: Testing & Evaluation (15 marks)

### 1. Test Plan Design (3 marks)

Test plan is comprehensive and well-structured.<br>
Clearly defines objectives, scope, and methodology for testing.<br>
Includes detailed steps for executing test cases.<br>
Identifies all relevant test scenarios (e.g., edge cases, normal cases).<br>
Demonstrates a clear understanding of the program’s functionality and potential issues.<br>


### 2. Test Cases, Records of test results & Evaluation (8 marks)

Test cases cover all relevant scenarios (e.g., edge cases, normal cases).<br>
Records of test results are detailed and well-organized.<br>
Evaluation of results is thorough and identifies all issues.<br>
Demonstrates a clear understanding of expected vs. actual outcomes.<br>
Includes suggestions for improvement based on test results.<br>


### 3. Program Improvement (4 marks)

Implements a major enhancement with a clear impact on functionality.<br>
Demonstrates innovative use of algorithms or techniques.<br>
Clearly explains the improvement and its benefits.<br>
Includes detailed documentation of the changes made.<br>
Shows a significant improvement in program performance or usability.<br>




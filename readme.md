### Author: Ahmad Saadat
# Qontigo Assessment 

# Table of Contents 📝

1. [Foreword](#foreword)
2. [Business requirements](#business-requirements-📋)
3. [Navigating the code base](#navigating-the-code-base-🖱️)
4. [Solution](#solution-🔧) <br>
    a. [High Level](#high-level-🐼) <br>
    b. [Low Level](#low-level-🧪)
5. [Going Forward](#going-forward-⏩)
6. [Setting up locally]()

# Foreword

**To see the output of this program directly, you can navigate to [src/data/output_files/](https://github.com/ahmadsaadat/Work_Python_Assessment_Qontigo/tree/main/src/data/output_files)**

- <sub><sup>For each DAY (DAY1 and DAY2), indicate how many distinct ETFs are present ➡️ [1_number_of_distinct_ETFs_per_day.csv](https://github.com/ahmadsaadat/Work_Python_Assessment_Qontigo/blob/main/src/data/output_files/1_number_of_distinct_ETFs_per_day.csv)</sup></sub>
- <sub><sup> For each DAY, for each ETF provide a breakdown of how many constituents are present in each ETF ➡️ [2_number_of_constituents_per_ETF_per_Day.csv](https://github.com/ahmadsaadat/Work_Python_Assessment_Qontigo/blob/main/src/data/output_files/2_number_of_constituents_per_ETF_per_Day.csv) </sup></sub>
- <sub><sup> Dropped -- Compare DAY1 to DAY2. For a given ETF, indicate which constituent has dropped from DAY1 to DAY2, and which constituent has been added from DAY1 to DAY2 ➡️ [3_0_dropped_constituents_between_Day1_and_Day2.csv](https://github.com/ahmadsaadat/Work_Python_Assessment_Qontigo/blob/main/src/data/output_files/3_0_dropped_constituents_between_Day1_and_Day2.csv) </sup></sub>
- <sub><sup> Added -- Compare DAY1 to DAY2. For a given ETF, indicate which constituent has dropped from DAY1 to DAY2, and which constituent has been added from DAY1 to DAY2 ➡️ [3_1_added_constituents_between_Day1_and_Day2.csv](https://github.com/ahmadsaadat/Work_Python_Assessment_Qontigo/blob/main/src/data/output_files/3_1_added_constituents_between_Day1_and_Day2.csv) </sup></sub>
- <sub><sup> For each ETF, indicate which constituent’s weight has changed the MOST from DAY1 to DAY2 ➡️ [4_max_constituent_percentage_change_per_ETF.csv](https://github.com/ahmadsaadat/Work_Python_Assessment_Qontigo/blob/main/src/data/output_files/4_max_constituent_percentage_change_per_ETF.csv) </sup></sub>


# Business requirements 📋

You can find the original set of business requirements here: [Click Me](https://qontigo-assessment.s3.amazonaws.com/Coding+Exercise.pdf)

# Navigating the code base :computer_mouse:
**src/**: contains the main business logic which aims to solve for the requirements above. <br>
**src/data/input_files/**: contains the actual text files/data source we will be operating on. <br>
**src/data/output_files/**: contains the csv files which are generated after running main.py on the **input_files**. <br>

**test/**: contains test cases which test the functionality of the main.py functions. <br>
**test/data/input_files/**: contains mock text files and mock data to test main.py functionality. <br>
**test/data/output_files/**: contains the csv files which are generated after running test_main.py on the mock input files.<br>


```
src/
├─ data/
│  ├─ input_files/
│  │  ├─ Day1.txt
│  │  ├─ Day2.txt
│  ├─ output_files/
│  │  ├─ 0_build_df.csv
│  │  ├─ 1_number_of_distinct_ETFs_per_day.csv
│  │  ├─ 2_number_of_constituents_per_ETF_per_Day.csv
│  │  ├─ 3_0_dropped_constituents_between_Day1_and_Day2.csv
│  │  ├─ 3_1_added_constituents_between_Day1_and_Day2.csv
│  │  ├─ 4_max_constituent_percentage_change_per_ETF.csv
├─ main.py

test/
├─ data/
│  ├─ input_files/
│  │  ├─ Day1.txt
│  │  ├─ Day2.txt
│  ├─ output_files/
│  │  ├─ 0_build_df.csv
│  │  ├─ 1_number_of_distinct_ETFs_per_day.csv
│  │  ├─ 2_number_of_constituents_per_ETF_per_Day.csv
│  │  ├─ 3_0_dropped_constituents_between_Day1_and_Day2.csv
│  │  ├─ 3_1_added_constituents_between_Day1_and_Day2.csv
│  │  ├─ 4_max_constituent_percentage_change_per_ETF.csv
│  │  ├─ test_main.py
├─ test_main.py


readme.md

```

# Solution 🔧

## High Level 🐼
The reason why I chose the **Pandas library** for Python to solve for these set of requirements is because of Pandas Efficiency and more clear cut Data Representation over other methods. By Efficiency and Data Representation I mean:

Efficiency: Pandas is originally designed to work with large datasets, offering operations which are faster than traditional programming language data structures. It also supports in built IO operations which can be very helpful for loading and unloading text and csv files.

Data Representation: The DataFrame object allows the data to be structured in a tabular format which can be easier to work with as a developer who spends a lot of time debugging.

## Low Level 🧪
I took a TDD approach to solving these set of requirements. By first building a **test** folder, and populating the input text files with **mock data**.

Once I was satisfied with the output results of the mock data, I attempted to extend it to the main files: Day1.txt and Day2.txt


# Going Forward ⏩

In order to make this code more **production grade**, it will need:
- **Higher degree of separation of concern:** As you might see throughout the code, there are instances were hardcoding took place. This is not advisable and must be revised. But in the interest of time, I will leave it this way.
- **More test cases:** We currently have one set of mock data to test our functions. Ideally they should be multiple to cover all edge cases.

# Setting up locally
### Technical Requirements:
- Python3 (version 3.11.4)
- pip3
- virtualenv
- pandas
- pytest

<br>

1. make sure you've installed python3, you can check so by running this command
```
python3 --version
```
2. Create a new virtual environment in the root project directory
```
python3 -m venv .venv
```
3. Activate the virtual environment
```
source .venv/bin/activate
```
4. Install dependencies:
```
pip3 install -r requirements.txt
```
5. navigate to src folder
```
cd src
```
6. run the main method
```
python3 main.py
```
7. navigate to data/output_files/ to see the generated csv files
```
cd data/output_files/
nano 1_number_of_distinct_ETFs_per_day.csv
```
import os
import math

class TestCase:
    def __init__(self, output, alphabetic, frequency, position):
        self.output = output
        self.alphabetic = alphabetic
        self.frequency = frequency
        self.position = position

def is_whitespace_or_empty(line):
    return not line.strip()

def is_max_or_average(str1, str2):
    return (str1.startswith("Maximum") and str2.startswith("Maximum")) or (str1.startswith("Average") and str2.startswith("Average"))

def extract_position_and_frequency(line):
    space_pos = line.find(' ')
    open_paren_pos = line.find('(')
    close_paren_pos = line.find(')')

    if space_pos == -1 or open_paren_pos == -1 or close_paren_pos == -1:
        raise ValueError("String format is incorrect.")

    alphabetic = line[:space_pos]
    freq = line[space_pos + 1:open_paren_pos].strip()
    pos = line[open_paren_pos + 1:close_paren_pos].strip()

    frequency = int(freq)
    position = int(pos)

    return TestCase(line, alphabetic, frequency, position)

def check_max_probes(str1, str2):
    if str1.startswith("Maximum") and str2.startswith("Maximum"):
        max1 = int(str1[26:].strip())
        max2 = int(str2[26:].strip())
        return max1 == max2
    return False

def check_average_probes(str1, str2):
    if str1.startswith("Average") and str2.startswith("Average"):
        max1 = math.ceil(float(str1[26:].strip()) * 10) / 10
        max2 = float(str2[26:].strip())
        return max1 == max2
    return False

def compare_test_cases(file1_path, file2_path):
    if not os.path.isfile(file1_path) or not os.path.isfile(file2_path):
        print("Error: Unable to open one or both files.")
        return

    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        test_cases1 = []
        test_cases2 = []
        current_test_case = []
        identical_frequency = 0
        identical_position = 0
        identical_alphabetic = 0
        identical_max_probes = 0
        identical_average_probes = 0

        for line in file1:
            if is_whitespace_or_empty(line):
                continue
            if line.startswith('-'):
                if current_test_case:
                    test_cases1.append(current_test_case)
                    current_test_case = []
            else:
                current_test_case.append(line.strip())
        if current_test_case:
            test_cases1.append(current_test_case)

        current_test_case = []

        for line in file2:
            if is_whitespace_or_empty(line):
                continue
            if line.startswith('-'):
                if current_test_case:
                    test_cases2.append(current_test_case)
                    current_test_case = []
            else:
                current_test_case.append(line.strip())
        if current_test_case:
            test_cases2.append(current_test_case)

    for i in range(min(len(test_cases1), len(test_cases2))):
        differences_found_frequency = False
        differences_found_position = False
        differences_found_alphabetic = False

        test_case1 = test_cases1[i]
        test_case2 = test_cases2[i]

        if test_case1 != test_case2:
            print(f"\nDifferences found in Test Case {i + 1}:")
            for j in range(min(len(test_case1), len(test_case2))):
                if test_case1[j].startswith("Maximum") or test_case2[j].startswith("Maximum"):
                    if not check_max_probes(test_case1[j], test_case2[j]):
                        print(f"Expected number of max probes is different for test case: {i + 1}")
                    else:
                        identical_max_probes += 1

                if test_case1[j].startswith("Average") or test_case2[j].startswith("Average"):
                    if not check_average_probes(test_case1[j], test_case2[j]):
                        print(f"Expected number of average probes is different for test case: {i + 1}")
                    else:
                        identical_average_probes += 1

                if j < len(test_case1) and j < len(test_case2) and not is_whitespace_or_empty(test_case1[j]) and not is_whitespace_or_empty(test_case2[j]) and not is_max_or_average(test_case1[j], test_case2[j]) and test_case1[j] != test_case2[j]:
                    t1 = extract_position_and_frequency(test_case1[j])
                    t2 = extract_position_and_frequency(test_case2[j])

                    if t1.frequency != t2.frequency:
                        differences_found_frequency = True

                    if t1.position != t2.position:
                        differences_found_position = True

                    if t1.alphabetic != t2.alphabetic:
                        differences_found_alphabetic = True

                    print(f"Expected: {t2.output} || Output: {t1.output}")

            if not differences_found_frequency:
                identical_frequency += 1
            if not differences_found_position:
                identical_position += 1
            if not differences_found_alphabetic:
                identical_alphabetic += 1

        else:
            print(f"Test Case {i + 1} is identical.")
            identical_frequency += 1
            identical_position += 1
            identical_alphabetic += 1
            identical_max_probes += 1
            identical_average_probes += 1

    print("######################################################")
    print(f"Total number of correct max probes: {identical_max_probes}")
    print(f"Total marks for max probes: {identical_max_probes} * 1 pt = {identical_max_probes * 1}")
    print("------------------------------------------------------")
    print(f"Total number of correct average probes: {identical_average_probes}")
    print(f"Total marks for average probes: {identical_average_probes} * 1 pt = {identical_average_probes * 1}")
    print("------------------------------------------------------")
    print(f"Total number of identical Frequency: {identical_frequency}")
    print(f"Total marks for identical Frequency: {identical_frequency} * 2 pt = {identical_frequency * 2}")
    print("------------------------------------------------------")
    print(f"Total number of identical Position: {identical_position}")
    print(f"Total marks for identical Position: {identical_position} * 2 pt = {identical_position * 2}")
    print("------------------------------------------------------")
    print(f"Total number of identical Alphabetic listing: {identical_alphabetic}")
    print(f"Total marks for identical Alphabetic listing: {identical_alphabetic} * 2 pt = {identical_alphabetic * 2}")
    print("------------------------------------------------------")
    print(f"Total marks: {(identical_alphabetic * 2) + (identical_position * 2) + (identical_frequency * 2) + (identical_max_probes * 1) + (identical_average_probes * 1)}")
    print("######################################################")

if __name__ == "__main__":
    print("Project Grades report")
    file1_path = "student_output.txt"
    file2_path = "Correct_output.txt"
    compare_test_cases(file1_path, file2_path)

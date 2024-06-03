import os

def is_whitespace_or_empty(line):
    return not line.strip()

def compare_test_cases(file1_path, file2_path):
    if not os.path.isfile(file1_path) or not os.path.isfile(file2_path):
        print("Error: Unable to open one or both files.")
        return

    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        # Read and discard the first line from file1 to ignore the student ID
        discard_line = file1.readline()
        if not discard_line:
            print("Error: Unable to read the first line from file1.")
            return

        # Read and discard the first line from file2 to ignore the header or any initial info
        discard_line = file2.readline()
        if not discard_line:
            print("Error: Unable to read the first line from file2.")
            return

        test_cases1 = []
        test_cases2 = []
        current_test_case = []

        # Process file1
        for line in file1:
            if is_whitespace_or_empty(line):
                continue
            if line.startswith("*"):
                if current_test_case:
                    test_cases1.append(current_test_case)
                    current_test_case = []
            else:
                current_test_case.append(line.strip())
        if current_test_case:
            test_cases1.append(current_test_case)

        current_test_case = []

        # Process file2
        file2.seek(0)
        discard_line = file2.readline()  # Skip the first line again after resetting the stream position

        for line in file2:
            if is_whitespace_or_empty(line):
                continue
            if line.startswith("*"):
                if current_test_case:
                    test_cases2.append(current_test_case)
                    current_test_case = []
            else:
                current_test_case.append(line.strip())
        if current_test_case:
            test_cases2.append(current_test_case)

    identical_test_cases = 0
    for i in range(min(len(test_cases1), len(test_cases2))):
        test_case1 = test_cases1[i]
        test_case2 = test_cases2[i]

        if test_case1 != test_case2:
            print(f"\nDifferences found in Test Case {i + 1}:")
            for j in range(max(len(test_case1), len(test_case2))):
                if j < len(test_case1) and j < len(test_case2) and \
                        not is_whitespace_or_empty(test_case1[j]) and \
                        not is_whitespace_or_empty(test_case2[j]) and \
                        test_case1[j] != test_case2[j]:
                    print(f"Student output: {test_case1[j]}")
                    print(f"Correct output: {test_case2[j]}\n")
        else:
            print(f"Test Case {i + 1} is identical.")
            identical_test_cases += 1

    print("######################################################")
    print(f"Total number of identical test cases: {identical_test_cases}")
    print(f"Total marks: {identical_test_cases * 5}")
    print("######################################################")

if __name__ == "__main__":
    file1_path = "output.txt"
    file2_path = "Correct_output.txt"
    compare_test_cases(file1_path, file2_path)

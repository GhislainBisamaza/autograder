#include <iostream>
#include <fstream>
#include <string>
#include <vector>

bool isWhiteSpaceOrEmpty(const std::string& str) {
    return str.find_first_not_of(" \t\n\v\f\r") == std::string::npos;
}

void compareTestCases(const std::string& file1_path, const std::string& file2_path) {
    std::ifstream file1(file1_path);
    std::ifstream file2(file2_path);

    if (!file1.is_open() || !file2.is_open()) {
        std::cerr << "Error: Unable to open one or both files." << std::endl;
        return;
    }

    // Read and discard the first line from file1 to ignore the student ID
    std::string discardLine;
    if (!std::getline(file1, discardLine)) {
        std::cerr << "Error: Unable to read the first line from file1." << std::endl;
        return;
    }

    // Read and discard the first line from file2 to ignore the header or any initial info
    if (!std::getline(file2, discardLine)) {
        std::cerr << "Error: Unable to read the first line from file2." << std::endl;
        return;
    }

    std::vector<std::vector<std::string>> testCases1;
    std::vector<std::vector<std::string>> testCases2;

    std::string line;
    std::vector<std::string> currentTestCase;

    while (std::getline(file1, line)) {
        if (isWhiteSpaceOrEmpty(line)) {
            continue;
        }

        if (line.find("*") == 0) {
            if (!currentTestCase.empty()) {
                testCases1.push_back(currentTestCase);
                currentTestCase.clear();
            }
        } else {
            currentTestCase.push_back(line);
        }
    }
    if (!currentTestCase.empty()) {
        testCases1.push_back(currentTestCase);
    }

    currentTestCase.clear();
    file2.clear();
    file2.seekg(0, std::ios::beg);

    // Skip the first line again after clearing flags and resetting the stream position
    std::getline(file2, discardLine);

    while (std::getline(file2, line)) {
        if (isWhiteSpaceOrEmpty(line)) {
            continue;
        }

        if (line.find("*") == 0) {
            if (!currentTestCase.empty()) {
                testCases2.push_back(currentTestCase);
                currentTestCase.clear();
            }
        } else {
            currentTestCase.push_back(line);
        }
    }
    if (!currentTestCase.empty()) {
        testCases2.push_back(currentTestCase);
    }

    size_t identicalTestCases = 0;
    for (size_t i = 0; i < std::min(testCases1.size(), testCases2.size()); ++i) {
        auto& testCase1 = testCases1[i];
        auto& testCase2 = testCases2[i];

        if (testCase1 != testCase2) {
            std::cout << "\n" << "Differences found in Test Case " << (i + 1) << ":" << std::endl;

            for (size_t j = 0; j < std::max(testCase1.size(), testCase2.size()); ++j) {
                if (j < testCase1.size() && j < testCase2.size() &&
                    !isWhiteSpaceOrEmpty(testCase1[j]) && !isWhiteSpaceOrEmpty(testCase2[j]) &&
                    testCase1[j] != testCase2[j]) {
                    std::cout << "Student output: " << testCase1[j] << std::endl;
                    std::cout << "Correct output: " << testCase2[j] << std::endl << "\n";
                }
            }
        } else {
            std::cout << "Test Case " << (i + 1) << " is identical." << std::endl;
            ++identicalTestCases;
        }
    }

    std::cout << "######################################################" << std::endl;
    std::cout << "Total number of identical test cases: " << identicalTestCases << std::endl;
    std::cout << "Total marks: " << identicalTestCases * 5 << std::endl;
    std::cout << "######################################################" << std::endl;

    file1.close();
    file2.close();
}

int main() {
    std::string file1_path = "output.txt";
    std::string file2_path = "Correct_output.txt";
    compareTestCases(file1_path, file2_path);

    return 0;
}





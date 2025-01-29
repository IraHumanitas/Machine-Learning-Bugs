import json
import os
from faker import Faker

fake = Faker()

FOLDER_NAME = "data_testing"
FILE_NAME = "test_cases.json"
FILE_PATH = os.path.join(FOLDER_NAME, FILE_NAME)

os.makedirs(FOLDER_NAME, exist_ok=True)

def get_input(prompt):
    return input(prompt)

def load_existing_data():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, 'r') as f:
                existing_data = json.load(f)
                return existing_data
        except (json.JSONDecodeError, FileNotFoundError):
            print("File kosong atau tidak dapat dibaca. Memulai dari awal.")
            return []
    return []

def save_test_data(data):
    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def generate_test_case(url, test_case, selectors, button_selector, expected_results, actual_data=None):
    test_cases = []

    if actual_data:
        input_action = {selector: actual_data.get(selector, fake.word()) for selector in selectors}
        test_cases.append({
            "test_case": test_case,
            "description": f"{test_case} dengan data yang benar",
            "selector_input": selectors,
            "button_selector": button_selector,
            "expected_result": expected_results["success"],
            "input_action": input_action,
            "actual_data": actual_data
        })

        for selector in selectors:
            wrong_input_action = {s: actual_data.get(s, fake.word()) for s in selectors}
            wrong_input_action[selector] = fake.word()  # Buat salah satu input berbeda
            test_cases.append({
                "test_case": test_case,
                "description": f"Input dengan {selector} yang salah",
                "selector_input": selectors,
                "button_selector": button_selector,
                "expected_result": expected_results["failure"],
                "input_action": wrong_input_action
            })

        all_wrong_input_action = {selector: fake.word() for selector in selectors}
        test_cases.append({
            "test_case": test_case,
            "description": "Input semua data salah",
            "selector_input": selectors,
            "button_selector": button_selector,
            "expected_result": expected_results["failure"],
            "input_action": all_wrong_input_action
        })


    full_input_action = {selector: fake.word() for selector in selectors}
    test_cases.append({
        "test_case": test_case,
        "description": f"Submit {test_case} semua data lengkap",
        "selector_input": selectors,
        "button_selector": button_selector,
        "expected_result": expected_results["success"],
        "input_action": full_input_action
    })

    for selector in selectors:
        partial_input_action = {s: fake.word() for s in selectors}
        partial_input_action[selector] = "" 
        test_cases.append({
            "test_case": test_case,
            "description": f"Submit {test_case} dengan {selector} kosong",
            "selector_input": selectors,
            "button_selector": button_selector,
            "expected_result": expected_results["failure"],
            "input_action": partial_input_action
        })

    empty_input_action = {selector: "" for selector in selectors}
    test_cases.append({
        "test_case": test_case,
        "description": f"Submit {test_case} dengan semua data kosong",
        "selector_input": selectors,
        "button_selector": button_selector,
        "expected_result": expected_results["failure"],
        "input_action": empty_input_action
    })

    return test_cases

def main():
    url = get_input("Enter the URL: ")
    test_case = get_input("Enter the test case (e.g., Login, Registration, Create, Delete): ").lower()

    selectors = {}
    button_selector = {}

    num_selectors = int(get_input("How many selectors to input? "))
    for i in range(num_selectors):
        selector_name = get_input(f"Enter selector {i+1} name (e.g., username, password, etc.): ")
        selector_type = get_input(f"Enter the type of selector {i+1} (id, name, class, etc.): ")
        selectors[selector_name] = selector_type

    button_name = get_input("Enter button name: ")
    button_type = get_input("Enter button type (id, name, class, etc.): ")
    button_selector = {
        "button_name": button_name,
        "button_type": button_type
    }

    success_expected_selector = get_input("Enter expected selector for success (e.g., success_message): ")
    success_expected_value = get_input("Enter expected value for success (e.g., Login Success): ")
    success_url = get_input("Enter the URL for success result: ")

    failure_expected_selector = get_input("Enter expected selector for failure (e.g., error_message): ")
    failure_expected_value = get_input("Enter expected value for failure (e.g., Login Failed): ")
    failure_url = get_input("Enter the URL for failure result: ")

    expected_results = {
        "success": {
            "expected_selector": success_expected_selector,
            "expected_value": success_expected_value,
            "url": success_url
        },
        "failure": {
            "expected_selector": failure_expected_selector,
            "expected_value": failure_expected_value,
            "url": failure_url
        }
    }

    actual_data = {}
    if get_input("Do you want to add actual data for the test case? (yes/no): ").lower() == "yes":
        for selector_name in selectors:
            actual_data[selector_name] = get_input(f"Enter actual value for {selector_name}: ")
    else:
        actual_data = None

    test_case_data = {
        "url": url,
        "test_cases": generate_test_case(url, test_case, selectors, button_selector, expected_results, actual_data)
    }

    existing_data = load_existing_data()
    existing_data.append(test_case_data)
    save_test_data(existing_data)

    print(f"Test cases successfully saved in {FILE_PATH}")

if __name__ == "__main__":
    main()

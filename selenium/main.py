import json
import os
import importlib.util
import sys

def load_test_cases(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def run_test_cases_for_url(selected_url, test_data):
    selected_test_cases = next(item for item in test_data if item['url'] == selected_url)['test_cases']
    
    for case in selected_test_cases:
        test_case_name = case['test_case']
        
        module_name = f"selenium.testcases.{test_case_name}"
        module_path = os.path.join(os.getcwd(), 'selenium', 'testcases', f"{test_case_name}.py")
        
        if module_path not in sys.path:
            sys.path.append(module_path)
        
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        module.run_tests(selected_url, selected_test_cases)

def main():
    data_file = "data-driver-test/test_cases.json"  
    test_data = load_test_cases(data_file)
    
    urls = [item['url'] for item in test_data]
    print("Available URLs to test:")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")
    
    choice = int(input("Select URL (number): ")) - 1
    selected_url = urls[choice]
    
    run_test_cases_for_url(selected_url, test_data)

if __name__ == "__main__":
    main()

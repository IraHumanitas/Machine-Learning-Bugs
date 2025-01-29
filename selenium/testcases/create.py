import json
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

def load_test_cases(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_test_result(test_case_name, results):
    dataset_folder = "dataset/automated_testing"
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    file_path = os.path.join(dataset_folder, f"{test_case_name}.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r+") as file:
            existing_data = json.load(file)
            existing_data.extend(results)
            file.seek(0)
            json.dump(existing_data, file, indent=4)
    else:
        with open(file_path, "w") as file:
            json.dump(results, file, indent=4)

def element_exists(driver, selector_type, value):
    try:
        driver.find_element(getattr(By, selector_type.upper()), value)
        return True
    except:
        return False

def run_create_test(driver, url, test_cases):
    driver.get(url)
    results = []
    
    for case in test_cases:
        start_time = time.time()
        has_bug = False
        error_message = ""
        status = "Passed"
        bug_type = "None"
        priority = "Low"
        
        # Input fields processing
        for field, selector_type in case['selector_input'].items():
            if element_exists(driver, selector_type, field):
                element = driver.find_element(getattr(By, selector_type.upper()), field)
                element.clear()
                element.send_keys(case['input_action'][field])
            else:
                has_bug = True
                status = "Failed"
                bug_type = "Element Not Found"
                priority = "Critical"
                error_message = f"Selector {selector_type} dengan jenis {field} tidak ditemukan."
                break
        
        if not has_bug:
            # Button click processing
            button_selector_type = case['button_selector']['button_type']
            button_name = case['button_selector']['button_name']
            
            if element_exists(driver, button_selector_type, button_name):
                button = driver.find_element(getattr(By, button_selector_type.upper()), button_name)
                button.click()
            else:
                has_bug = True
                status = "Failed"
                bug_type = "Element Not Found"
                priority = "Critical"
                error_message = f"Selector {button_name} dengan jenis {button_selector_type} tidak ditemukan."
        
        if not has_bug:
            # Expected result processing
            expected_selector = case['expected_result'].get('expected_selector', '')
            expected_value = case['expected_result'].get('expected_value', '')
            expected_url = case['expected_result'].get('url', '')
            
            expected_result_message = ""
            if expected_selector and expected_value:
                expected_result_message += f"Muncul pesan '{expected_value}' dari tag {expected_selector}"
            if expected_url:
                expected_result_message += f" dan berpindah ke halaman {expected_url}" if expected_result_message else f"Berpindah ke halaman {expected_url}"
            
            try:
                if expected_selector and expected_value:
                    result_element = driver.find_element(getattr(By, expected_selector.upper()), expected_value)
                    actual_value = result_element.text
                    if actual_value != expected_value:
                        has_bug = True
                        status = "Failed"
                        bug_type = "UI/Functional"
                        priority = "High"
                        error_message = f"Expected: {expected_value}, but got: {actual_value}"
            except:
                has_bug = True
                status = "Failed"
                bug_type = "Element Not Found"
                priority = "Critical"
                error_message = f"Expected element {expected_selector} with value {expected_value} not found."
        
        duration = time.time() - start_time
        
        results.append({
            "URL": url,
            "Metode Pengujian": "Create",
            "Input Pengguna": case['input_action'],
            "Status": status,
            "Jenis Bug": bug_type,
            "Prioritas": priority,
            "Tanggal/Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Pesan Error": error_message,
            "Fungsi/Modul": "Create Page",
            "Durasi Pengujian": f"{duration:.2f} seconds",
            "Ada Bug (False/True)": has_bug,
            "Expected Result": expected_result_message,
        })
    
    save_test_result("create", results)
    driver.quit()

def run_tests(url, test_cases):
    driver = webdriver.Chrome()
    try:
        run_create_test(driver, url, test_cases)
    finally:
        driver.quit()

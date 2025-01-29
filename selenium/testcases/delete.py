import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from datetime import datetime
import time


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

def run_delete_test(driver, url, test_cases):
    driver.get(url)
    results = []
    
    for case in test_cases:
        start_time = time.time()
        has_bug = False
        error_message = ""
        status = "Passed"
        bug_type = "None"
        priority = "Low"
        
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
                error_message = f"Selector {selector_type} with field {field} not found."
                break
        
        if not has_bug:
            button_selector_type = case['button_selector']['button_type']
            button_name = case['button_selector']['button_name']
            
            if element_exists(driver, button_selector_type, button_name):
                button = driver.find_element(getattr(By, button_selector_type.upper()), button_name)
                button.click()
                
                # Handle alertt
                try:
                    alert = Alert(driver)
                    alert.accept()  
                except:
                    pass  
                
            else:
                has_bug = True
                status = "Failed"
                bug_type = "Element Not Found"
                priority = "Critical"
                error_message = f"Button {button_name} with type {button_selector_type} not found."
        
        duration = time.time() - start_time
        log_details = {
            "type": "ErrorMessage" if has_bug else "None",
            "content": error_message,
            "details": {
                "actual_url": driver.current_url,
                "expected_error_message": case['expected_result'].get('expected_value', ''),
                "page_source": driver.page_source[:500],
                "cookies": driver.get_cookies()
            }
        }
        
        results.append({
            "URL": url,
            "Metode Pengujian": "Delete",
            "Input Pengguna": case['input_action'],
            "Status": status,
            "Jenis Bug": bug_type,
            "Prioritas": priority,
            "Tanggal/Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Pesan Error": error_message,
            "Fungsi/Modul": "Delete Operation",
            "Durasi Pengujian": f"{duration:.2f} seconds",
            "Ada Bug (False/True)": has_bug,
            "Expected Result": case['expected_result'].get('expected_value', ''),
            "log": log_details
        })
    
    save_test_result("delete", results)
    driver.quit()


def run_tests(url, test_cases):
    driver = webdriver.Chrome()
    try:
        run_delete_test(driver, url, test_cases)
    finally:
        driver.quit()

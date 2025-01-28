import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Fungsi untuk memuat data uji dari file JSON
def load_existing_data():
    try:
        with open('test_cases.json', 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Fungsi untuk menyimpan data uji ke dalam file JSON
def save_test_data(data):
    with open('test_cases.json', 'w') as f:
        json.dump(data, f, indent=4)

# Fungsi untuk menjalankan test case login menggunakan Selenium
def run_test_case(test_case_data, driver):
    url = test_case_data["url"]
    username_value = test_case_data["input_action"].get("username", "")
    password_value = test_case_data["input_action"].get("password", "")
    
    driver.get(url)
    time.sleep(2)  # Waktu tunggu agar halaman dimuat dengan baik
    
    # Mengisi username dan password
    try:
        username_input = driver.find_element(By.NAME, test_case_data["selector_input"]["username"])
        password_input = driver.find_element(By.NAME, test_case_data["selector_input"]["password"])
    except Exception as e:
        return {
            "error": f"Element not found: {e}",
            "is_bug": True,
            "log": {
                "type": "ElementNotFoundError",
                "content": f"Failed to find elements: {e}",
                "details": {
                    "url": driver.current_url,
                    "page_source": driver.page_source[:500],  # Menampilkan 500 karakter pertama dari source
                }
            }
        }

    username_input.clear()
    password_input.clear()
    username_input.send_keys(username_value)
    password_input.send_keys(password_value)
    
    # Mengklik tombol submit
    try:
        submit_button = driver.find_element(By.NAME, test_case_data["button_selector"]["button_name"])
        submit_button.click()
    except Exception as e:
        return {
            "error": f"Button click failed: {e}",
            "is_bug": True,
            "log": {
                "type": "ButtonClickError",
                "content": f"Failed to click button: {e}",
                "details": {
                    "url": driver.current_url,
                    "page_source": driver.page_source[:500],
                }
            }
        }
    
    time.sleep(2)  # Waktu tunggu setelah mengklik tombol
    
    # Mengecek error message atau URL yang diharapkan
    try:
        error_message = driver.find_element(By.CLASS_NAME, test_case_data["expected_result"]["expected_selector"]).text
        expected_error_message = test_case_data["expected_result"]["expected_value"]
        expected_url = test_case_data["expected_result"]["url"]
        
        # Menyimpan hasil
        result = {
            "test_case": test_case_data["description"],
            "username_value": username_value,
            "password_value": password_value,
            "expected_url": expected_url,
            "expected_error_message": expected_error_message,
            "url": url,
            "error": f"Message: {error_message}",
            "is_bug": error_message != expected_error_message,
            "log": {
                "type": "ErrorMessage",
                "content": error_message,
                "details": {
                    "actual_url": driver.current_url,
                    "expected_error_message": expected_error_message,
                    "page_source": driver.page_source[:500],  # Menampilkan 500 karakter pertama dari source
                    "cookies": driver.get_cookies(),
                }
            }
        }

        return result

    except Exception as e:
        return {
            "error": f"Error checking error message: {e}",
            "is_bug": True,
            "log": {
                "type": "ErrorCheckingError",
                "content": f"Failed to check error message: {e}",
                "details": {
                    "url": driver.current_url,
                    "page_source": driver.page_source[:500],
                }
            }
        }

# Fungsi utama
def main():
    # Setup WebDriver
    options = Options()
    options.headless = False  # Atur menjadi True jika ingin menjalankan tanpa tampilan browser
    driver = webdriver.Chrome(service=Service('/path/to/chromedriver'), options=options)
    
    # Memuat data uji dari file JSON
    test_cases_data = load_existing_data()
    
    results = []
    
    # Menjalankan setiap test case
    for test_case_group in test_cases_data:
        for test_case_data in test_case_group["test_cases"]:
            result = run_test_case(test_case_data, driver)
            if result:
                results.append(result)
    
    # Menyimpan hasil ke file JSON
    save_test_data(results)
    
    # Menutup driver setelah selesai
    driver.quit()

if __name__ == "__main__":
    main()

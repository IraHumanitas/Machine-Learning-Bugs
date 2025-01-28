from utils.web_driver import get_webdriver
from tests.login import run_login_test
from tests.regist import run_regist_test
from tests.create import run_create_test
from tests.delete import run_delete_test
from tests.update import run_update_test
import json

def load_test_data():
    with open('test_cases.json', 'r') as f:
        return json.load(f)

def run_tests(test_data, browser_name):
    driver = get_webdriver(browser_name)
    
    for data in test_data:
        url = data.get("url")
        for test_case in data["test_cases"]:
            case_type = test_case.get("test_case")
            if case_type == "Login":
                run_login_test(test_case, url, driver)
            elif case_type == "Registration":
                run_regist_test(test_case, url, driver)
            elif case_type == "Create":
                run_create_test(test_case, url, driver)
            elif case_type == "Delete":
                run_delete_test(test_case, url, driver)
            elif case_type == "Update":
                run_update_test(test_case, url, driver)

    driver.quit()

if __name__ == '__main__':
    test_data = load_test_data()
    browser_name = 'chrome'  
    run_tests(test_data, browser_name)

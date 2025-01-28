from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeDriverManager

def get_webdriver(browser_name='chrome'):
    """
    Fungsi untuk mendapatkan WebDriver berdasarkan browser yang dipilih.
    Dapat memilih antara Chrome, Firefox, dan Edge.
    """
    if browser_name.lower() == 'chrome':
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif browser_name.lower() == 'firefox':
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    elif browser_name.lower() == 'edge':
        service = EdgeService(executable_path=EdgeDriverManager().install())
        driver = webdriver.Edge(service=service)
    else:
        raise ValueError(f"Browser {browser_name} not supported.")
    
    return driver

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options
# from selenium import webdriver


# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

def set_up_driver(url):
	# opts = Options()
	# opts.set_headless = True
	# driver = webdriver.Firefox(options=opts)
	# driver.get(url)

	options = webdriver.ChromeOptions()
	options.add_argument("--no-sandbox")
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
	driver.get(url)
	return driver
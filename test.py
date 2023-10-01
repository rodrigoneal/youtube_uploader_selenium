import undetected_chromedriver as uc
from dotenv import dotenv_values

from youtube_uploader_selenium.page.pages import LoginPage


config = dotenv_values()


driver = uc.Chrome()

driver.get("https://www.youtube.com")
page_login = LoginPage(driver)
page_login.login.make_login(config["email"], config["password"], time_wait_login_two_factor=20)


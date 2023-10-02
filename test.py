import undetected_chromedriver as uc
from dotenv import dotenv_values

from youtube_uploader_selenium.page.pages import LoginPage
from youtube_uploader_selenium.utils.login_type import LoginType


config = dotenv_values()


driver = uc.Chrome()

driver.get("https://www.youtube.com")
page_login = LoginPage(driver)
page_login.login.login(
    config["email"],
    config["password"],
    time_wait_login_two_factor=20,
    login_type=LoginType.MANUAL,
)

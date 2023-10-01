from time import sleep
from youtube_uploader_selenium import Constant
from youtube_uploader_selenium.exceptions.exceptions import TwoFactorLoginException
from youtube_uploader_selenium.log.logger import get_logger
from youtube_uploader_selenium.page_object.page_object import Element
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

log = get_logger("youtube_uploader_selenium", verbose=True)

constants = Constant()


class Login(Element):
    btn_login = (By.XPATH, "//yt-button-shape/a/yt-touch-feedback-shape/div/div[2]")
    input_email = (By.ID, "identifierId")
    btn_next_user = (By.ID, "identifierNext")
    input_password = (By.ID, "password")
    btn_next_password = (By.ID, "passwordNext")
    two_factor = (By.XPATH, "//section[2]/div/div/section/header/div/h2/span/span")
    confirm_login = (By.XPATH, "//button/yt-icon-badge-shape/div/div[1]/yt-icon/yt-icon-shape/icon-shape")

    def make_login(self, email: str, password: str, time_wait_login_two_factor: int = 10) -> None:
        log.info("Logging in...")
        self.find_element(self.btn_login).click()
        self.find_element(self.input_email).send_keys(email)
        self.find_element(self.btn_next_user).click()

        input_password = self.find_element(self.input_password)
        sleep(1)
        ActionChains(self.driver).send_keys_to_element(input_password, password).perform()
        self.find_element(self.btn_next_password).click()
        cont = 0
        try:
            self.find_element(self.confirm_login, time=5)
        except (NoSuchElementException, TimeoutException):
            log.info(f"Two-factor login detected. Confirm login in {time_wait_login_two_factor} seconds.")
            while True:
                try:
                    self.find_element(self.two_factor, time=1)
                except (NoSuchElementException, TimeoutException):
                    try:
                        self.find_element(self.confirm_login, time=time_wait_login_two_factor)
                        self.save_cookie()
                        log.success("Two-factor login confirmed.")
                        break
                    except (NoSuchElementException, TimeoutException):
                        pass
                except Exception as e:
                    print(e)
                if cont >= time_wait_login_two_factor:
                    log.error("Two-factor login failed.")
                    raise TwoFactorLoginException("Two-factor login failed.") from None
                cont += 1
                sleep(1)
        log.success("Login successful.")
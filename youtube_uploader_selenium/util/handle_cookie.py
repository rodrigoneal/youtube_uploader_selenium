from pathlib import Path
import pickle
from undetected_chromedriver import Chrome
def write_cookies(driver: Chrome) -> None:
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

def load_cookies(driver: Chrome) -> None:
    if not Path("cookies.pkl").exists():
        return False
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

def has_cookie(driver: Chrome) -> bool:
    if not Path("cookies.pkl").exists():
        return False
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        if "youtube" in cookie.get("domain"):
            return True
        else:
            return False
"""
Modulo com Page Objects pronto.
"""

from abc import ABC
from pathlib import Path
import pickle
from typing import Callable, List, Tuple

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from youtube_uploader_selenium.log.logger import get_logger

log = get_logger("youtube_uploader_selenium", verbose=True)

class SeleniumObject:
    """Pattern Page Objects
    """

    def save_cookie(self):
        log.info("Saving cookies...")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
    
    def load_cookie(self):
        log.info("Loading cookies...")
        if not Path("cookies.pkl").exists():
            return False
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        return True


    def has_youtube_cookie(self) -> bool:
        log.info("Verifying cookies...")
        if not Path("cookies.pkl").exists():
            return False
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            if "youtube" in cookie.get("domain"):
                return True
            else:
                return False

    def find_element(self, element: Tuple[str, str],
                     condition: Callable = EC.presence_of_element_located,
                     time: float = 10) -> WebElement:
        """Encontra um elemento web.

        Args:
            element (Tuple[str, str]): Com elementos que serão buscando na tela ex:(By.XPATH, "//body").
            condition (Callable, optional): Vai aguardar até o status passando na condição. Defaults to EC.presence_of_element_located.
            time (float, optional): Tempo que vai aguardar o elemento aparecer antes de levantar exceção. Defaults to 10.

        Returns:
            WebElement
        """
        return WebDriverWait(self.driver, time).until(condition(element))

    def find_elements(self, element: Tuple[str, str],
                      condition: Callable = EC.presence_of_all_elements_located,
                      time: float = 10) -> List[WebElement]:
        """Encontra n elementos web.

        Args:
            element (Tuple[str, str]): Com elementos que serão buscando na tela ex:(By.XPATH, "//body").
            condition (Callable, optional): Vai aguardar até o status passando na condição. Defaults to EC.presence_of_element_located.
            time (float, optional): Tempo que vai aguardar o elemento aparecer antes de levantar exceção. Defaults to 10.

        Returns:
            List[WebElement]
        """
        return WebDriverWait(self.driver, time).until(condition(element))


    def execute_script(self, element: WebElement, js_script: str):
        """Executa um script.

        Args:
            element (WebElement): Elemento selenium
            js_script (str): script 

        Returns:
            str: Retorno do script
        """        
        if element:
            return self.driver.execute_script(js_script, element)
        return self.driver.execute_script(js_script)
        

    def change_frame(self, frame: WebElement):
        """Muda o frame da pagina.

        Args:
            frame (WebElement): Elemento com os dados do frame.
        """
        self.driver.switch_to.frame(frame)

    def change_window(self, index: int = 1):
        """Alterá a janela que está sendo manipulada

        Args:
            index (int, optional): index da pagina que vai manipular. Defaults to 1.
        """
        self.driver.switch_to.window(self.driver.window_handles[index])


class Page(ABC, SeleniumObject):
    """Pagina onde ficam os elementos."""

    def __init__(self, driver: webdriver, url=None):
        self.driver = driver
        self.url = url
        self._reflection()

    def _reflection(self):
        """Essa função faz com que não seja necessário ficar passando o driver para todos os elementos.
        Basta passar para a pagina e todos as suas dependencias terão o driver."""
        for atributo in dir(self):
            atributo_real = getattr(self, atributo)
            if isinstance(atributo_real, Element):
                atributo_real.driver = self.driver

    def open(self):
        """Navega para o url passado."""
        self.driver.maximize_window()
        self.driver.get(self.url)

    def close(self):
        """Fecha o browser.
        """
        self.driver.quit()

    def __enter__(self):
        """Cria um contexto que no final fecha o navegador.

        Returns:
            Self
        """
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        """Cria um contexto que no final fecha o navegador."""
        self.close()
        if traceback:
            raise type(value)


class Element(ABC, SeleniumObject):
    """Elementos da pagina."""

    def __init__(self, driver: webdriver = None):
        self.driver = driver
import os
import threading
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

PATH = os.path.join("driver", "chromedriver.exe")
options = Options()
options.add_argument("log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)
service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://monkeytype.com")
driver.implicitly_wait(3)


class Main:
    def __init__(self):
        self.typing = False
        self.delay = 0.01

    def typer(self):
        while True:
            if (self.typing and
                    len(driver.find_element(By.ID, "words").find_element(By.CLASS_NAME, "word").text) != 0):
                word = [letter for letter in driver.find_element(By.CSS_SELECTOR, ".word.active").text] + [" "]

                for letter in word:
                    ActionChains(driver).send_keys(letter).perform()
            else:
                self.typing = False

            time.sleep(self.delay)

    def main_loop(self):
        while True:
            command = input("type 'help' for commands > ").lower()

            if command == "start":
                if len(driver.find_element(By.ID, "words").text) != 0:
                    self.typing = True
                    print("started program")
                else:
                    print("failed to start")
            elif command == "stop":
                self.typing = False
                print("program stoped")
            elif command == "quit":
                print("quitting program")
                driver.quit()
                break
            elif command == "help":
                print("""
'start' - start typing
'stop' - stop typing
'quit' - quit program
""")
            else:
                print(f"'{command}' is not recognized")


def main():
    main = Main()
    typer_thred = threading.Thread(target=main.typer)
    typer_thred.daemon = True
    typer_thred.start()
    main.main_loop()


if __name__ == "__main__":
    main()

import threading
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('log-level=3')

driver = webdriver.Chrome(options=options)
driver.get("https://monkeytype.com/")
driver.implicitly_wait(3)

class Main:
    def __init__(self):
        self.typing = False
        self.delay = 0.01

    def typer(self):
        while True:
            if (self.typing and len(driver.find_element(By.ID, "words").find_element(By.CLASS_NAME, "word").text) != 0):
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
                print("program stopped")
            elif command == "quit":
                print("quitting program")
                driver.quit()
                break
            elif command == "help":
                print("'start' - start typing")
                print("'stop' - stop typing")
                print("'quit' - quit program")
            else:
                print(f"'{command}' is not recognized")


def main():
    main = Main()
    typer_thread = threading.Thread(target=main.typer)
    typer_thread.daemon = True
    typer_thread.start()
    main.main_loop()


if __name__ == "__main__":
    main()

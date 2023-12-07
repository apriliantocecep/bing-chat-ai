# filename: bing.py
# import the required packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.keys import Keys
import time


def bot(question: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')

    service = Service("/opt/homebrew/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(width=1500, height=1000)

    driver.get("https://www.bing.com/account/general")
    driver.find_element(By.XPATH, '//*[@id="adlt_set_off"]').click()
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="sv_btn"]').click()
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="adlt_confirm"]').click()
    time.sleep(1)

    # navigate to chat page
    driver.get("https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx")
    # TODO: need adjustment for the chat menu to be appear
    time.sleep(10)

    # input prompt process
    cib_serp_el = driver.find_element(By.CSS_SELECTOR, '#b_sydConvCont > cib-serp')
    shadow_root_cib_serp: ShadowRoot = driver.execute_script("return arguments[0].shadowRoot;", cib_serp_el)

    cib_action_bar_el = shadow_root_cib_serp.find_element(By.CSS_SELECTOR, '#cib-action-bar-main')
    shadow_root_cib_action_bar: ShadowRoot = driver.execute_script("return arguments[0].shadowRoot;", cib_action_bar_el)

    cib_text_input_el = shadow_root_cib_action_bar.find_element(By.CSS_SELECTOR, 'div > div.main-container > div > div.input-row > cib-text-input')
    shadow_root_cib_text_input: ShadowRoot = driver.execute_script("return arguments[0].shadowRoot;", cib_text_input_el)

    input_prompt_el: WebElement = shadow_root_cib_text_input.find_element(By.CSS_SELECTOR, '#searchbox')
    input_prompt_el.send_keys(question)
    input_prompt_el.send_keys(Keys.ENTER)
    time.sleep(5)

    # get content process
    cib_conversation = shadow_root_cib_serp.find_element(By.CSS_SELECTOR, '#cib-conversation-main')
    shadow_root_cib_conversation: ShadowRoot = driver.execute_script("return arguments[0].shadowRoot;", cib_conversation)

    cib_chat_turn_el = shadow_root_cib_conversation.find_element(By.CSS_SELECTOR, '#cib-chat-main > cib-chat-turn')
    shadow_root_cib_chat_turn: ShadowRoot = driver.execute_script("return arguments[0].shadowRoot;", cib_chat_turn_el)

    cib_message_group_el = shadow_root_cib_chat_turn.find_element(By.CSS_SELECTOR, 'cib-message-group.response-message-group')
    WebDriverWait(driver, 10).until(EC.visibility_of(cib_message_group_el), "Timeout cib-message-group.response-message-group")
    shadow_root_cib_message_group: ShadowRoot = driver.execute_script("return arguments[0].shadowRoot;", cib_message_group_el)

    cib_message_el = shadow_root_cib_message_group.find_element(By.CSS_SELECTOR, 'cib-message')
    shadow_root_cib_message: ShadowRoot = driver.execute_script("return arguments[0].shadowRoot;", cib_message_el)

    driver.save_screenshot("bing-cib-message.png")

    cib_shared_el: WebElement = shadow_root_cib_message.find_element(By.CSS_SELECTOR, 'cib-shared')
    WebDriverWait(driver, 10).until(EC.visibility_of(cib_shared_el), "Timeout cib-shared")

    # get text content
    content = cib_shared_el.text

    driver.quit()

    return content

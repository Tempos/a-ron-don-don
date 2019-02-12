from selenium.webdriver.common.by import By
# OLX
URL_PATH = 'https://www.olx.ua/transport/legkovye-avtomobili/?search%5Bfilter_float_price%3Afrom%5D=1500000'

ITEMS_LINKS_CSS = '.link.linkWithHash'
SHOW_PHONE_NUMBER_CSS = 'span.spoiler'
PHONE_NUMBER_VISIBLE = 'display: none;'
PHONE_NUMBER_CSS = 'strong.xx-large'
USER_NAME_CSS = '.offer-user__details a'
PRICE_CSS = '.price-label strong'
USER_SINCE_CLASS = 'user-since'
PAGE_LINK_CSS = '.item a'
USER_ADDRESS_CSS = 'address p'

# Telegram
TELEGRAM_URL = 'https://web.telegram.org/#/im'

MENU = '//*[@class="tg_head_btn dropdown-toggle"]'
CONTACTS = '//*[contains(text(),"Contacts")]'
NEW_CONTACT = '//*[contains(text(),"New contact")]'
FIRST_NAME = '//*[contains(text(),"First name")]'
PHONE_NUMBER = '//*[contains(text(),"Phone number")]'
BUTTON_SAVE = '//*[contains(text(),"Save")]'
ERROR_NOT_FOUND = '//*[contains(text(),"Not found")]'
ERROR_TOO_FAST = '//*[contains(text(),"Too fast")]'
PROFILE = '//*[@class="tg_head_peer_info"]'
ACTION_MORE = '//*[contains(text(),"More...")]'
ACTION_DELETE_CONTACT = '//*[contains(text(),"Delete contact")]'
CLOSE = '//*[@class="md_modal_action md_modal_action_close"]'
PROFILE_NAME = '//*[@class="peer_modal_profile_name"]'
PROFILE_SEEN = '//*[@class="peer_modal_profile_description"]'
PROFILE_DESCRIPTION = '//*[@class="md_modal_iconed_section_wrap md_modal_iconed_section_number"]'

# AUTO.RIA
RIA_PATH = """https://auto.ria.com/search/
?body.id[0]=3
&categories.main.id=1
&price.USD.gte=200000
&price.currency=1
&abroad.not=0
&custom.not=1
&size=100"""
RIA_RESULTS = (By.ID, 'staticResultsCount')
RIA_TICKETS = (By.CLASS_NAME, 'm-link-ticket')
RIA_NAME = (By.XPATH, '//*[@id="userInfoBlock"]/div[1]/div/h4')
RIA_NUMBER = (By.CLASS_NAME, 'phone')
RIA_PRICE = (By.XPATH, '//*[@id="showLeftBarView"]/section[1]/div[1]/strong')
RIA_PROFILE = (By.CLASS_NAME, 'seller_info_name')
RIA_ADDRESS = (By.CLASS_NAME, 'item_inner')
RIA_DESCRIPTION = (By.XPATH, '//*[@id="heading-cars"]/div/h1')

import selenium.webdriver as webdriver

def get_results(search_term):
    url = "https://www.startpage.com"
    browser = webdriver.firefox()
    browser.get(url)
    search_box = browser.find_element_by_id("query")
    search_box.send_keys(search_term)
    search_box.submit()

    try:
        links = browser.findelements_by_xpath("//ol[@class='web_regular_results']//h3//a")
    except:
        links = browser.findelements_by_xpath("//h3//a")
    results = []
    for link
import pytest as pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

import secrets

# When you register for a trail version, youd be given a unique url to login
# Use that url here in the URL variable
URL = "your sales force analytics personalized url page"  # Analytics Page



# init driver with options
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


# Logs into the Analytics page
def login():
    driver.get(URL)
    print(driver.title)
    driver.find_element(By.ID, "username").send_keys(secrets.USER_ID)
    driver.find_element(By.ID, "password").send_keys(secrets.PASSWORD)
    driver.find_element(By.ID, "Login").click()
    time.sleep(30)
    print(driver.title)
    driver.implicitly_wait(30)


# navigates to the dashboard tab through the main page and then clicks on the dashboard under test
def dashboard_navigation():
    # WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "createdByMeAssets")))
    driver.find_element(By.XPATH, "//*[text()='ABC Seed']").click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(driver.find_element(By.ID, "topNav_dashboard"))).click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        driver.find_element(By.XPATH, "(//*[@data-tooltip='Worldwide Fundraising - Starter'])[2]"))).click()


# a assert for dashboard components loading
def did_dashboard_components_load():
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(driver.find_element(By.XPATH, "//button[text()='Edit']")))
    dashboard_components = "//*[starts-with(@class,'widget-container')]"
    dashboard_components = WebDriverWait(driver, 60).until(
        EC.visibility_of_all_elements_located((By.XPATH, dashboard_components)))
    print(f"Total components in the dashboard are: {len(dashboard_components)}")
    assert len(dashboard_components) == 17, "One of few of the components is misisng/did not load. Please check"


# assert for dashboard title
def dashboard_title_check():
    dashboard_title = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//*[@class='gridLayoutWidget text']")))
    txt_dashboard_title = dashboard_title.text
    print(txt_dashboard_title)
    assert txt_dashboard_title == 'Worldwide Fundraising', 'Not in the right dashboard'


# asserts for grid layouts
def dashboard_grid_layouts():
    some_texts = "//*[@class='gridLayoutWidget text']"
    some_texts_looper = driver.find_elements(By.XPATH, some_texts)
    print(len(some_texts_looper))
    txt_ls = []
    for each_hdr in range(len(some_texts_looper)):
        each_txt = driver.find_element(By.XPATH, '(' + some_texts + ')' + '[' + str(each_hdr + 1) + ']')
        txt_ls.append(each_txt.text)
    print(txt_ls)
    assert txt_ls == ['Worldwide Fundraising', 'KEY METRICS', 'Goal Attainment'], 'Few components are missing'


# asserts for charts
@pytest.mark.skip
def dashboard_charts_check():
    charts_ls = []
    # charts = "//*[contains(@data-chart-name, 'chart_')]"
    charts = "//*[@class='chart']"
    charts_looper = driver.find_elements(By.XPATH, charts)
    for each_chart in range(len(charts_looper)):
        chart = driver.find_element(By.XPATH, '(' + charts + ')' + '[' + str(each_chart + 1) + ']')
        charts_ls.append(chart.text)
    print(charts_ls)


# asserts for presence of table
def dashboard_table_check():
    tbl = driver.find_elements(By.XPATH, "//*[@class='wave-table']")
    print(len(tbl))
    if len(tbl) == 1:
        print("One Table is present in the dashboard")
        assert True
    else:
        print("Either table is not loaded or not present at all. Please verify")
        assert False


if __name__ == "__main__":
    start_time = datetime.now()
    login()
    dashboard_navigation()
    did_dashboard_components_load()
    dashboard_title_check()
    dashboard_grid_layouts()
    dashboard_charts_check()
    dashboard_table_check()

    print("---- End of Tests ---- \nAll checks are complete.")
    end_time = (datetime.now() - start_time)
    print(f"Total Process Time: {end_time} \nTotal Explicit Sleeps included within the Total Process Time: 30 sec")

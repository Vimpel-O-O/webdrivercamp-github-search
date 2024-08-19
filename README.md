# Webdriver Behave Setup

## Tree

### Project
* README.md
* features
  * components
    * base.py
  * steps
    * xyz_steps.py
  * environment.py
  * xyz.feature
* venv
* PATH for ChromeDriver > "/usr/local/bin/chromedriver"

## Source

### base.py
* from selenium.webdriver
  * common.by import **By**
  * common.keys import **Keys**
  * support.ui import **WebDriverWait**
  * support import expected_condition as **EC**
  * import requests

### steps.py
from behave import *

    @step("Browser: Navigate to gh-users-search website")
    def step_impl(context):
        context.browser.get("https://gh-users-search.netlify.app/")

### environment.py
* from
  * selenium import webdriver
    * components.base import Base



    def before_all(context):
        context.browser = webdriver.Chrome()
    
    def after_all(context):
        context.browser.quit()

### feature_name.feature
    Feature:

      Scenario: Verify number of followers against API
        Given Browser: Navigate to gh-users-search website
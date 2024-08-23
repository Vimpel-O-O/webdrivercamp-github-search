import time

import requests
import page_xpathes
from behave import *
from selenium.webdriver.common.by import By


@step("Browser: Navigate to gh-users-search website")
def step_impl(context):
    context.browser.get("https://gh-users-search.netlify.app/")


@step('UI: search for {username} by {way}')
def step_impl(context, username, way):
    if way.lower() == "return":
        context.element.insert_text(username, "//input[@data-testid='search-bar']", True)
    elif way.lower() == "button":
        context.element.insert_text(username, "//input[@data-testid='search-bar']")
        context.element.click_item('//button[text() = "search"]')


@step("Sleep {num}")
def step_impl(context, num):
    time.sleep(int(num))


@step("API: send GET request to {username}'s {data}")
def step_impl(context, username, data):
    response = requests.get(f"https://api.github.com/users/{username}")
    context.response = response
    json_resp = response.json()
    context.data_name = data
    context.api_data = json_resp[data]
    return context.api_data, context.data_name


@step("API: verify status code is 200")
def step_impl(context):
    if context.response.status_code != 200:
        raise 'Invalid status code'


@step("GitHub Integration API: verify user's {data} fields values")
def step_impl(context, data):
    if data in ["public_repos", "followers", "following", "public_gists"]:
        if "public" in context.data_name:
            context.data_name = context.data_name.replace('public_', '')

        field_on_page = context.element.find_text_on_page(
            page_xpathes.user_info_nums_xpath.format(data_name=context.data_name))
        if int(field_on_page) != context.api_data:
            print(f"Fields values are not equal: OnPage: {field_on_page} and API: {context.api_data}")
            raise "Fields values are not equal"

    if data in ["name", "login", "blog", "company", "location"]:
        if data in ["name", "login"]:
            fields_on_page = context.browser.find_elements(By.XPATH, page_xpathes.header_user_info_xpath)
        else:  # ["blog", "company", "location"]
            fields_on_page = context.browser.find_elements(By.XPATH, page_xpathes.personal_info_fields_xpath)

        fields_text = []
        for field in fields_on_page:
            fields_text.append(field.text)
        if context.api_data not in fields_text:
            context.api_data = "@" + context.api_data
            if context.api_data not in fields_text:
                print(f"Fields values are not equal: API: {context.api_data} in OnPage: {fields_text}")
                raise "Fields values are not equal"

    if data == "bio":
        field_on_page = context.element.find_text_on_page(page_xpathes.user_bio_xpath)
        if context.api_data != field_on_page:
            print(f"Fields values are not equal: OnPage: {field_on_page} and API: {context.api_data}")
            raise "Fields values are not equal"

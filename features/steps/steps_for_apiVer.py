import time

import requests
import page_xpathes
from behave import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


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


@step("API: send GET request for {username}'s followers list")
def step_impl(context, username):
    response = requests.get(f"https://api.github.com/users/{username}/followers?per_page=100")
    context.json_followers_list = response.json()
    return context.json_followers_list


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

        # empty location - earth verification
        if not context.api_data:
            if 'earth' not in fields_text:
                print(f"Fields values are not equal: API: {context.api_data} in OnPage: {fields_text}")
                raise "Fields values are not equal"
        elif context.api_data not in fields_text:
            context.api_data = "@" + context.api_data
            if context.api_data not in fields_text:
                print(f"Fields values are not equal: API: {context.api_data} in OnPage: {fields_text}")
                raise "Fields values are not equal"

    if data == "bio":
        field_on_page = context.element.find_text_on_page(page_xpathes.user_bio_xpath)
        if context.api_data != field_on_page:
            print(f"Fields values are not equal: OnPage: {field_on_page} and API: {context.api_data}")
            raise "Fields values are not equal"


@step("GitHub Integration API: verify user's followers field values")
def step_impl(context):
    followers_list_on_page = context.browser.find_elements(By.XPATH, "//div[@class='followers']//h4")
    followers_count = 0

    # verify number of followers is 100
    if len(followers_list_on_page) != len(context.json_followers_list) and len(followers_list_on_page) != 100:
        print(len(followers_list_on_page), len(context.json_followers_list))
        print(f"The length of followers list is - {len(followers_list_on_page)}")
        raise "Not 100 followers listed"
    for follower in followers_list_on_page:
        if follower.text.lower() != (context.json_followers_list[followers_count]['login']).lower():
            print(f"Follower on the page and in api request are not equal: OnPage: {follower.text} and API: {(context.json_followers_list[followers_count]['login'])}")
            raise "Followers are not equal"
        followers_count += 1


@step("UI: Press follow button")
def step_impl(context):
    context.element.click_item(page_xpathes.follow_button_xpath)


@step("Verify transfer to {username} github page")
def step_impl(context, username):
    try:
        context.element.find_element_on_page(page_xpathes.github_logo_xpath)
        github_username = context.element.find_text_on_page(page_xpathes.github_username_xpath)
        if github_username != username:
            raise "Invalid user page after pressing follow"
    except TimeoutException:
        raise "Invalid user page after pressing follow"

from behave import *


@step("Browser: Navigate to gh-users-search website")
def step_impl(context):
    context.browser.get("https://gh-users-search.netlify.app/")

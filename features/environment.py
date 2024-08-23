from selenium import webdriver
from components.base import Base


def before_all(context):
    context.browser = webdriver.Chrome()
    context.element = Base(context.browser)


def after_all(context):
    context.browser.quit()

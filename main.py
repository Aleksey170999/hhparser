import time

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from some_variables import browser


def get_links(vacancy_list):
    return [link for link in vacancy_list.find_all('a') if 'https://hh.ru/vacancy/' in link.get('href', None)]


def parse_page(url):
    browser.get(url)

    search_line = browser.find_element(by=By.XPATH, value='/html/body/div[4]/div/div[3]/div[1]/div[1]/div/div/div[2]/div/form/div/div[1]/span/input')
    search_line.send_keys('python-developer')

    search_button = browser.find_element(by=By.XPATH, value='/html/body/div[4]/div/div[3]/div[1]/div[1]/div/div/div[2]/div/form/div/div[2]/button')
    search_button.click()


def get_links_paginated(page_counter):
    res = []
    for i in range(page_counter):
        cur_page_vacancy_list = BeautifulSoup(browser.page_source, features="lxml")

        links = get_links(cur_page_vacancy_list)
        res.extend(links)
        try:
            next_page_button = browser.find_element(by=By.XPATH,
                                                    value='/html/body/div[5]/div/div[3]/div[1]/div/div[3]/div[2]/div[2]/div/div[5]/div/a')
            next_page_button.click()
        except NoSuchElementException:
            res.extend(cur_page_vacancy_list)
            print('Нет кнопки Дальше')
            break

        res.extend(cur_page_vacancy_list)

    return res


def get_vacancies_info(url):
    parse_page(url)
    links = get_links_paginated(3)
    vacancy_counter = 1

    for link in links:
        if 'Произошла ошибка' not in link.get_text():
            print(f"{vacancy_counter}___{link.get('href', None), link.get_text()}")
            vacancy_counter += 1


def main():
    get_vacancies_info('https://hh.ru/')
    browser.quit()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

# 제목 : 구글 칫솔 (정상) (이미지) 크롤링 소스
# 작성자 : 전규빈

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import os
from os import path
import requests
import io
from PIL import Image
import base64
from selenium.webdriver import ActionChains


def search_selenium(search_name):
    with webdriver.Edge('msedgedriver.exe') as driver:
        search_url = "https://www.google.com/search?q=" + str(search_name) + "&hl=ko&tbm=isch"
        driver.get(search_url)

        folder_name = "train_image"
        if not path.isdir(folder_name):
            os.mkdir(folder_name)

        element_number = 1
        file_list = os.listdir(folder_name)
        file_number = len(file_list) + 1
        wait = WebDriverWait(driver, 1)
        is_image_element = True

        while True:
            image_locator = (By.CSS_SELECTOR,
                             f"#islrg > div.islrc > div:nth-child({element_number}) > a.wXeWr.islib.nfEiy.mM5pbd > div.bRMDJf.islir > img")
            image_condition = expected_conditions.presence_of_element_located(image_locator)
            element_number += 1
            try:
                image_element = wait.until(image_condition, f"The image elements don't exist.")
                ActionChains(driver).move_to_element(image_element).perform()
            except Exception as e:
                print(e)
                if is_image_element:
                    is_image_element = False
                    continue
                
                break

            is_image_element = True
            image_src = image_element.get_attribute('src')

            if image_src[0] == "d":
                src_split = image_src.split(',')
                image = base64.b64decode(src_split[1])
            else:
                header = {'User-Agent': 'Edge/89.0.774.57'}
                response = requests.get(image_src, headers=header)
                image = response.content

            file_path = f"{folder_name}/{file_number}.jpg"
            with open(file_path, 'wb') as file:
                file.write(image)
                print(file_path)
            file_number += 1

        input("press any key to exit")


if __name__ == "__main__":
    search_name = input("검색하고 싶은 키워드 : ")
    search_selenium(search_name)

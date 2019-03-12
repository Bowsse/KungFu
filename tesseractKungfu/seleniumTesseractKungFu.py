from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from PIL import Image
from io import StringIO
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os
import cv2
import sys
import pytesseract
import base64
import re
import time

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

driver.get("https://hero.pizza-online.fi/#po")

print(driver.title)

# implicit wait for canvas to load
time.sleep(3)

canvas = driver.find_element_by_xpath('/html/body/div[1]/canvas')

print(canvas.get_attribute("cursor"))

print(canvas.get_attribute("width"))
print(canvas.get_attribute("height"))
webdriver.ActionChains(driver).move_to_element_with_offset(canvas, int(canvas.get_attribute("width")) / 2, int(canvas.get_attribute("height")))

i = int(canvas.get_attribute("height")) - 100
while i > 590:
    i = i-1
    print(i)
    webdriver.ActionChains(driver).move_to_element_with_offset(canvas, int(canvas.get_attribute("width")) / 2, i).click().perform()
    #time.sleep(0.2)
while canvas:
    webdriver.ActionChains(driver).key_down(Keys.SPACE, canvas).perform()
    time.sleep(0.15)
    webdriver.ActionChains(driver).key_up(Keys.SPACE, canvas).perform()
    webdriver.ActionChains(driver).key_down(Keys.SPACE, canvas).perform()
    webdriver.ActionChains(driver).key_up(Keys.SPACE, canvas).perform()
    webdriver.ActionChains(driver).key_down(Keys.SPACE, canvas).perform()
    webdriver.ActionChains(driver).key_up(Keys.SPACE, canvas).perform()
    time.sleep(0.55)

    png_url = driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(png_url)

    # save to a file
    with open(r"canvas.png", 'wb') as f:
        f.write(canvas_png)
        imPath = "canvas.png"

    if __name__ == '__main__':
    
      # Define config parameters.
      # '-l eng'  for using the English language
      # '--oem 1' for using LSTM OCR Engine
      config = ('-l eng --oem 1 --psm 11')
    
      # Read image from disk
      im = cv2.imread(imPath, cv2.IMREAD_COLOR)
    
      # Run tesseract OCR on image
      text = pytesseract.image_to_string(im, config=config)
    
      # Print recognized text
      print(text)

      if "GAME OVER" in text:
        break

try:
    print(driver.title)

finally:
    driver.quit()

img = Image.open('canvas.png')
img.show()

import os
import platform
import xlrd
import time
from selenium import webdriver
from pathlib import Path
from itertools import zip_longest
from static_methods import get_download_folder

# remove downloads/result.xlsx if exists
path_char = '\\' if platform.system() == 'Windows' else '/'
downloaded_result_file_path = get_download_folder()+path_char+"result.xlsx"
if os.path.exists(downloaded_result_file_path):
    os.remove(downloaded_result_file_path)

# activity to choose two form files and submit the form, download file
defaultUrls = {
  "dev": 'http://localhost:5000',
  "production": 'http://pmix-borrow-web.com'
}

browser = webdriver.Chrome()
browser.get(defaultUrls["dev"])

file1 = str(Path("test/static/TestCase1/input/1.xlsx").resolve())
file2 = str(Path("test/static/TestCase1/input/2.xlsx").resolve())
if platform.system() == 'Windows':
    file1 = file1.replace("\\", "\\\\")
    file2 = file2.replace("\\", "\\\\")

file1_uploader = browser.find_element_by_id("file1")
file1_uploader.send_keys(file1)
file2_uploader = browser.find_element_by_id("file2")
file2_uploader.send_keys(file2)
button_submit = browser.find_element_by_id("btn-submit")
button_submit.click()

while not os.path.exists(downloaded_result_file_path):
    time.sleep(1)
browser.close()

# compare two files
rb1 = xlrd.open_workbook(downloaded_result_file_path)
rb2 = xlrd.open_workbook(Path("test/static/TestCase1/output/result.xlsx").resolve())

sheet1 = rb1.sheet_by_index(0)
sheet2 = rb2.sheet_by_index(0)

flag = True
for rownum in range(max(sheet1.nrows, sheet2.nrows)):
    if rownum < sheet1.nrows:
        row_rb1 = sheet1.row_values(rownum)
        row_rb2 = sheet2.row_values(rownum)

        for colnum, (c1, c2) in enumerate(zip_longest(row_rb1, row_rb2)):
            if c1 != c2:
                print("Row {} Col {} - {} != {}".format(rownum+1, colnum+1, c1, c2))
                flag = False
    else:
        print("Row {} missing".format(rownum+1))
        flag = False

if flag:
    print('success!')
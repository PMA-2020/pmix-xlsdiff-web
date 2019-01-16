from selenium import webdriver
from pathlib import Path
import platform

defaultUrls = {
  "dev": 'http://localhost:5000',
  "production": 'http://pmix-borrow-web.com'
}


browser = webdriver.Chrome()
browser.get(defaultUrls["dev"])


source_file_path_string = str(Path("test/static/Merge/input/source/translations-KER7-2018.10.02-v4-jef.xlsx").resolve())
target_file_path_string = str(Path("test/static/Merge/input/target/KER7-Female-Questionnaire-v4-jef.xlsx").resolve())
if platform.system() == 'Windows':
    source_file_path_string = source_file_path_string.replace("\\", "\\\\")
    target_file_path_string = target_file_path_string.replace("\\", "\\\\")

source_file_uploader = browser.find_element_by_id("source-file")
source_file_uploader.send_keys(source_file_path_string)
target_file_uploader = browser.find_element_by_id("target-file")
target_file_uploader.send_keys(target_file_path_string)

button_submit = browser.find_element_by_id("btn-submit")
button_submit.click()
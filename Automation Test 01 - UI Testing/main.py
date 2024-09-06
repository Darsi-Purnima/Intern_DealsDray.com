import cv2
import numpy as np
import pyautogui
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.safari.webdriver import SafariDriver #For Safari Browser

# List of Screen Resolutions & Devices 
resolutions = {
    "Desktop_1920x1080": (1920, 1080),
    "Desktop_1366x768": (1366, 768),
    "Desktop_1536x864": (1536, 864),
    "Mobile_360x640": (360, 640),
    "Mobile_414x896": (414, 896),
    "Mobile_375x667": (375, 667)
}

#List of URLs to be tested 
urls = [
    "https://www.getcalley.com/",
    "https://www.getcalley.com/calley-lifetime-offer/",
    "https://www.getcalley.com/see-a-demo/",
    "https://www.getcalley.com/calley-teams-features/",
    "https://www.getcalley.com/calley-pro-features/"
]
#To start screen recording
def start_screen_recording(filename, fps=10):
    def record():
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(f"{filename}.avi", fourcc, fps, screen_size)

        while recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        
        out.release()

    global recording, recording_thread
    recording = True
    recording_thread = threading.Thread(target=record)
    recording_thread.start()

# To stop screen recording
def stop_screen_recording():
    global recording
    recording = False
    recording_thread.join()

# To save screenshot
def save_screenshot(driver, browser_name, resolution_name, url):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    domain = url.split("//")[1].split("/")[0]
    folder_path = f"screenshots/{browser_name}/{resolution_name}/{domain}/{timestamp}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    screenshot_path = f"{folder_path}/screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Saved screenshot: {screenshot_path}")

# To perform test
def perform_test(driver, browser_name):
    try:
        # Start screen recording
        start_screen_recording(f"{browser_name}_test")
        for url in urls:
            for resolution_name, resolution in resolutions.items():
                width, height = resolution
                driver.set_window_size(width, height)
                driver.get(url)
                time.sleep(3)  
                save_screenshot(driver, browser_name, resolution_name, url)
    finally:
        stop_screen_recording()
        driver.quit()

#Chrome Browser Testing
chrome_options = webdriver.ChromeOptions()
chrome_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
perform_test(chrome_driver, "Chrome")

#Firefox Browser Testing
firefox_options = webdriver.FirefoxOptions()
firefox_driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
perform_test(firefox_driver, "Firefox")

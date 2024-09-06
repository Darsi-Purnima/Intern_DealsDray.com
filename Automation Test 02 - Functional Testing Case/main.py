import threading
import cv2
import numpy as np
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#To save screenshot
def take_screenshot(filename):
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

# To start screen recording
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

#To stop screen recording
def stop_screen_recording():
    global recording
    recording = False
    recording_thread.join()

#To set Chrome WebDriver 
chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()


try:
    # To start screen recording
    start_screen_recording("test_recording")
    
   
    driver.get('https://demo.dealsdray.com/') #Navigate to the URL
    
    
    username = driver.find_element(By.CLASS_NAME, 'css-l8vkz1')  #Find username
    password = driver.find_element(By.CLASS_NAME, 'css-r71t31')  #Find password

    username.send_keys('prexo.mis@dealsdray.com')
    password.send_keys('prexo.mis@dealsdray.com')
    
    login_button = driver.find_element(By.XPATH, '//button[contains(text(),"Login")]')  
    login_button.click()


    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Dashboard")]'))) 
  


    orders_section = driver.find_element(By.CLASS_NAME, 'css-1s178v5') #Find Orders section
    orders_section.click()
    
    orders = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Orders")]'))) #Navigate to Orders
    orders.click()
    
    
    add_bulk_order = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Add Bulk Orders")]'))) #Add Bulk Orders
    driver.execute_script("arguments[0].scrollIntoView();", add_bulk_order)
    driver.execute_script("arguments[0].click();", add_bulk_order)
    
    
    upload_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="file"]'))) #Upload XLS File
    upload_button.send_keys('C:\\Users\\eswar\\Desktop\\Automation Tester - DealsDray\\Automation Test 02 - Functional Testing Case\\demo-data.xlsx') #XLS file path

    import_button = driver.find_element(By.XPATH, '//button[contains(text(),"Import")]') 
    driver.execute_script("arguments[0].scrollIntoView();", import_button)
    driver.execute_script("arguments[0].click();", import_button)
    
    validate_button = WebDriverWait(driver, 10).until (EC.element_to_be_clickable((By.CLASS_NAME, "css-6aomwy"))) #Validate data
    driver.execute_script("arguments[0].click();", validate_button)
    
    
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept() #Accept alert
            
    time.sleep(4)

    take_screenshot('output.png') #To save screenshot
    
    
finally:
    # Stop screen recording
    stop_screen_recording()
    driver.quit()
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import move
import time


def get_latest_downloaded_file(download_folder):
    # Get the latest downloaded file in the specified folder
    files = [f for f in os.listdir(download_folder) if os.path.isfile(os.path.join(download_folder, f))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(download_folder, x)), reverse=True)
    
    if files:
        return os.path.join(download_folder, files[0])
    else:
        return None


def download_and_move_all_csvs(url, download_folder, target_folder):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        
        close_kakor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cky-banner-btn-close'))
        )
        
        close_kakor.click()
        
        list_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ocobs-stationslist-button'))
        )
        list_button.click()
        
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "stations-info-table-body"))
        )

        time.sleep(5)
        # Assuming each row has a unique identifier, adjust the XPath accordingly
        rows = table.find_elements(By.XPATH, './div[@class="stations-info-table-tr"]')

        for row in rows:
            # Click on the row to reveal the download button
            row.click()

            # Wait for the download button to appear
            download_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-id="corrected-archive"]'))
            )

            # Click on the download button
            download_button.click()


            # Add logic to handle the downloaded file, for example, move it to a specific folder
            
            WebDriverWait(driver, 10).until(
                lambda d: get_latest_downloaded_file(download_folder) is not None
                )
    
            # Wait for the file size to stabilize, indicating the download is complete
            initial_size = 0
            stable_count = 0
            while stable_count < 5:  # Adjust this count based on your download speed
                current_size = os.path.getsize(get_latest_downloaded_file(download_folder))
                if current_size == initial_size:
                    stable_count += 1
                else:
                    stable_count = 0
                    initial_size = current_size
                time.sleep(3)  # Adjust the sleep time based on your download speed
            # Get the latest downloaded file path
            downloaded_file_path = get_latest_downloaded_file(download_folder)
    
            if downloaded_file_path:
                # Move the downloaded file to the target folder
                move(downloaded_file_path, target_folder)


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


webpage_url = 'https://www.smhi.se/data/oceanografi/ladda-ner-oceanografiska-observationer#param=seatemperature,stations=core'
download_folder = '/home/kon/Downloads'
target_folder = '/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/sea-temp'
download_and_move_all_csvs(webpage_url, download_folder, target_folder)


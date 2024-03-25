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


def download_and_move_all_csvs(url, download_folder, target_folder, chosen_variable=None):
    """
    Parameters
    ----------
    url : TYPE
        DESCRIPTION.
    download_folder : TYPE
        DESCRIPTION.
    target_folder : TYPE
        DESCRIPTION.
    chosen_variable : str, optional
        DESCRIPTION. The default is None. It is the ID of the button.

    Returns
    -------
    None.

    """
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        
        close_kakor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cky-banner-btn-close'))
        )
        
        close_kakor.click()
        
        if chosen_variable:
            collapse_variable_choices_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'expandable-container-button'))
            )
            
            collapse_variable_choices_button.click()
            
            time.sleep(1)
            
            choose_variable_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'button[data-hash="{chosen_variable}"]'))
                )

            choose_variable_button.click()    
        
            time.sleep(1)

        if 'oceanografi' in url:
            list_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ocobs-stationslist-button'))
            )
            list_button.click()
        elif 'meteorologi' in url:
            list_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'metobs-stationslist-button'))
            )
            list_button.click()
        
        time.sleep(1)

        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "stations-info-table-body"))
        )

        time.sleep(5)
        # Assuming each row has a unique identifier, adjust the XPath accordingly
        rows = table.find_elements(By.XPATH, './div[@class="stations-info-table-tr"]')

        for row in rows:
            # Click on the row to reveal the download button
            row.click()

            time.sleep(1)
            # Wait for the download button to appear
            download_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-id="corrected-archive"]'))
            )

            # Click on the download button
            download_button.click()


            # Add logic to handle the downloaded file, for example, move it to a specific folder
            
            WebDriverWait(driver, 20).until(
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
            
            # Check if the target folder exists or is a file
            if not os.path.isdir(target_folder):
                # Create the target folder if it doesn't exist
                os.makedirs(target_folder)
                time.sleep(2)

            if downloaded_file_path:
                # Move the downloaded file to the target folder
                move(downloaded_file_path, target_folder)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


CHOSEN_VARIABLE = 'airPressure'
CLIMATE_FOLDER = 'meteorologi'
url ='https://www.smhi.se/data/meteorologi/ladda-ner-meteorologiska-observationer/#param=airPressure,stations=active,stationid=173810'
download_folder = '/home/kon/Downloads'
target_folder = f'/home/kon/Documents/Sweden/Master/Thesis/Code/Thesis/data/SMHI/{CLIMATE_FOLDER}/{CHOSEN_VARIABLE}'
download_and_move_all_csvs(url, download_folder, target_folder, chosen_variable=CHOSEN_VARIABLE)


# The code in this file is to take screenshots from website and from downloaded PDF.

from selenium import webdriver
import time
import pymupdf
import pdb

def capture_screenshots(url, class_folder, class_id):
    width = 1200
    overlap = 180

    print(f'capture screenshots {url}')

    # Path to WebDriver (e.g., ChromeDriver)
    webdriver_path = '/Users/ninachen/Desktop/reading_extract_code/chromedriver'
    
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(url)
    
    # Set the window width and height dynamically
    driver.set_window_size(width, 800)  # You can set an initial height (optional)
    
    # Get the actual browser window height
    browser_height = driver.get_window_size()['height']
    
    # Calculate the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    print(total_height)
    
    # Initialize variables
    screenshots = []
    offset = 0
    count_number = 0
    
    # Capture the screenshots segment by segment
    while offset < total_height:
        # Scroll to the next segment
        driver.execute_script(f"window.scrollTo(0, {offset});")
        time.sleep(1)  # Wait for page to load/adjust after scroll
        
        # Capture and save the screenshot
        screenshot_path = f'{class_folder}/{class_id}/{count_number}.png'
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)
        
        # Print or log the capture
        print(f"Captured {screenshot_path}")
        
        # Move the offset, ensuring overlap
        offset += (browser_height - overlap)
        count_number += 1
    
    # Close the browser
    driver.quit()
    screenshots_saved_path = f'{class_folder}/{class_id}'
    print(f'Web screenshots saved to {screenshots_saved_path}')



# Open local PDF, take screenshots for each page. 

import pymupdf

def take_pdf_screenshots(pdf_path, class_folder, class_id):
    count = 0
    
    # Load PDF
    pdf_content = pymupdf.open(pdf_path)
    num_pages = pdf_content.page_count
    mat = pymupdf.Matrix(2, 2)

    # Take screenshots for each PDF page.
    for page in range(num_pages):
        content_page = pdf_content.load_page(page)
        pix = content_page.get_pixmap(matrix = mat)

        # Save images to local folders
        pix.save(f'{class_folder}/{class_id}/{count}.png')
        count += 1
        
    print(f'PDF screenshots saved to {class_folder}/{class_id}')
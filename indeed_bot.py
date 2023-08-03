from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from options import INDEED_FILTERS, INDEED_URLS
import urllib.parse
import time
import pyshorteners
from datetime import datetime

class Indeed:
    def __init__(self, driver, base_url, keywords, location, url_shortener):
        self.base_url = base_url
        self.driver = driver
        self.keywords = keywords
        self.location = location
        self.url_shortener = url_shortener
    
    def get_url(self):
        url = self.base_url + "/jobs?q=" + urllib.parse.quote_plus(self.keywords) + "&l=" + urllib.parse.quote_plus(self.location)
        print(url)
        return url

    def reject_cookies(self):
        try:
            self.driver.find_element(By.ID, "onetrust-reject-all-handler").click()
        except:
            pass
    
    def check_email_popup(self):
        try:
            self.driver.find_element(By.ID, "mosaic-desktopserpjapopup").find_element(By.TAG_NAME, "button").click()
        except:
            pass
    
    def option_input(self, condition, message):
        answer=None
        while not answer:
            try:
                answer = int(input(message))
                if answer not in condition:
                    raise ValueError
            except ValueError:
                answer = None
                print("That's not a valid option!")
        return answer

    def get_filters(self): #can't do it recursively since hrefs and actual options change in parallel to other options
        print("There are multiple filters that can be set at Indeed.com depending on your location. Do you want to select them?")
        print("1. Yes")
        print("2. No")
        answer = self.option_input((1,2), "Select an option: ")
        if answer == 2:
            return
        
        for dropdown_name_ID , dropdown_list_ID in INDEED_FILTERS:
            try:
                dropdown_button = self.driver.find_element(By.ID, dropdown_name_ID)
                dropdown_name = dropdown_button.get_attribute("innerText")
                dropdown_list = self.driver.find_element(By.ID, dropdown_list_ID).find_elements(By.TAG_NAME, "a")          
            except:
                continue
            print("Please select an option for {} filter:".format(dropdown_name))
            print("1. Any")
            for index, option in enumerate(dropdown_list):
                print("{}.".format(index+2),option.get_attribute("innerText"))

            answer = self.option_input(range(1, len(dropdown_list) + 2), "Select an option: ")

            if answer == 1:
                self.check_email_popup()
                continue
            else:
                try:
                    dropdown_button.click()
                    dropdown_list[answer - 2].click()
                    # time.sleep(2)
                except (ElementClickInterceptedException, ElementNotInteractableException) as error:
                    self.check_email_popup()
                    dropdown_button.click()
                    dropdown_list[answer - 2].click()
                    continue
    
    def next_page(self):
        try:    
            next_button = self.driver.find_element(By.XPATH, "//a[@data-testid='pagination-page-next']")
            next_button.click()
            return True
        except (ElementNotInteractableException, ElementClickInterceptedException):
            self.check_email_popup()
            self.reject_cookies()
            next_button.click()
            return True
        except NoSuchElementException:
            return False

    def get_attribute(self, element, by, by_prop, attribute):
        try:
           attribute_str = element.find_element(by, by_prop).get_attribute(attribute)
           return attribute_str
        except:
            return None

    def get_job_listings(self):
        job_list = []
        try:
            cards = self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
        except:
            return job_list

        for card in cards:
            job_url_element = card.find_element(By.TAG_NAME, "a")
            job_url = self.url_shortener.tinyurl.short(job_url_element.get_attribute("href"))
            job_title = self.get_attribute(card, By.TAG_NAME, "span", "innerText")
            company_name = self.get_attribute(card, By.CLASS_NAME, "companyName", "innerText")
            company_rating = self.get_attribute(card, By.CLASS_NAME, "ratingsDisplay", "innerText")
            company_location = self.get_attribute(card, By.CLASS_NAME, "companyLocation", "innerText")
            job_snippet = self.get_attribute(card, By.CLASS_NAME, "job-snippet", "innerText").strip()
            job_posting_date = self.get_attribute(card, By.CLASS_NAME, "date", "innerText")
            extract_date = datetime.today().strftime('%Y-%m-%d')
            job_list.append([job_title, company_name, company_location, company_rating, job_snippet, job_posting_date, extract_date, job_url, "Indeed"])
        return job_list

    def scrape_jobs(self):
        run = True
        scraped_jobs = []
        while run:
            current_page_list = self.get_job_listings()
            if len(current_page_list) == 0:
                run = False
            else:
                scraped_jobs.extend(current_page_list)
                run = self.next_page()
        return scraped_jobs

    def run(self):
        self.driver.get(self.get_url())
        time.sleep(5)
        self.reject_cookies()
        time.sleep(2)
        self.get_filters()
        return self.scrape_jobs()


    
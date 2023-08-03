import os
from selenium import webdriver
from config import SEARCH_PARAMS, COUNTRY, OUTPUT_FILE_NAME, FILTER_COMPANIES, COMPANY_SIMILARITY_THRESHOLD, BOTS
from options import INDEED_URLS, TABLE_COLUMNS
from indeed_bot import Indeed
import undetected_chromedriver as uc
import pyshorteners
import pandas as pd
from fuzzywuzzy import fuzz

class Scrapper:

    def __init__(self, chromeOptions):
        self.driver = uc.Chrome(options=chromeOptions)
        url_shortener = pyshorteners.Shortener()
        self.create_bots()
        # self.indeed_bot = Indeed(self.driver,INDEED_URLS[COUNTRY], INDEED_SEARCH["KEYWORDS"], INDEED_SEARCH["LOCATION"], url_shortener)

    def create_bots(self):
        self.bots = []
        url_shortener = pyshorteners.Shortener()
        if BOTS["Indeed"]:
            self.bots.append(Indeed(self.driver,INDEED_URLS[COUNTRY], SEARCH_PARAMS["KEYWORDS"], SEARCH_PARAMS["LOCATION"], url_shortener))
        if BOTS["LinkedIn"]:
            pass

    def check_list_size(self, job_list, bot):
        job_count = len(job_list)
        message = "{} job postings were found at: {} with the following keywords: '{}' and location: '{}'".format(job_count, bot.base_url, bot.keywords, bot.location)
        save = True if job_count > 0 else False
        return save, message
    
    def filter_companies(self, df, companies, threshold,):
        count = 0
        for index, row in df.iterrows():
            for company in companies:
                if not row["Company Name"]:
                    continue
                ratio = fuzz.token_set_ratio(row["Company Name"].lower(), company.lower())
                if  ratio >= threshold:
                    count += 1
                    print("Company filtered: {} with: {}. The match ratio was: {}%".format(row["Company Name"], company, ratio))
                    df.drop(index, inplace=True)
        print("{} job listings were filtered with the following company name list: {}".format(count, FILTER_COMPANIES))

    def save_csv(self, df, file_name):
        df.to_excel(file_name + ".xlsx", index=False)
        
    def prepare_csv(self, job_list):
        df = pd.DataFrame(job_list, columns=TABLE_COLUMNS)
        df = df.drop_duplicates(subset=["Job Title", "Company Name", "Location"])
        if len(FILTER_COMPANIES) > 0:
            self.filter_companies(df, FILTER_COMPANIES, COMPANY_SIMILARITY_THRESHOLD)
        self.save_csv(df, OUTPUT_FILE_NAME)
        
    # def run(self):
    #     indeed_jobs = self.indeed_bot.run()
    #     save, message = self.check_list_size(indeed_jobs, self.indeed_bot)
    #     print(message)
    #     if save:
    #         self.prepare_csv(indeed_jobs)
        
    def run(self):
        if len(self.bots) == 0:
            print("No bots were selected! Please select at least one bot in the config.py file.")
            return

        scraped_jobs = []
        for bot in self.bots:
            job_list = bot.run()
            save, message = self.check_list_size(job_list, bot)
            print(message)
            if save:
                scraped_jobs.extend(job_list)
        if len(scraped_jobs) > 0:
            self.prepare_csv(scraped_jobs)

if __name__ == "__main__":
    options = webdriver.ChromeOptions() 
    # options.add_argument('--headless') 
    scrapper = Scrapper(options)
    scrapper.run()
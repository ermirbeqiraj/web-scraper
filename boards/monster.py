from bs4 import BeautifulSoup
import sys
from boards.helpers import HttpHelpers

class MonsterJobs:
    def __init__(self, url):
        self.url = url
        self.helpers = HttpHelpers()

    def get(self):
        page = self.helpers.download_page(self.url)
        if page is None:
            sys.exit('There was a monster downloading the monster jobs webpage. cannot continue further, so fix this first')

        monster_jobs = self.__parse_index(page)

        for job in monster_jobs:
            job_content = self.helpers.download_page(job["href"])
            if job_content is None:
                continue

            parsed_details = self.__parse_details(job_content)
            job["description_text"] = parsed_details[0]
            job["description"] = parsed_details[1]
        
        return monster_jobs

    def __parse_index(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        jobs_container = soup.find(id='ResultsContainer')
        job_items = jobs_container.find_all('section', class_='card-content')
        if job_items is None or len(job_items) == 0:
            return []
        
        all_jobs = []

        for job_elem in job_items:
            title_elem = job_elem.find('h2', class_='title')
            company_elem = job_elem.find('div', class_='company')
            url_elem = job_elem.find('a')

            if None in (title_elem, company_elem, url_elem):
                continue

            href = url_elem.get('href')
            if href is None:
                continue

            item = {
                "title" : title_elem.text.strip(),
                "company" : company_elem.text.strip(),
                "href" : href,
                "description" : "",
                "description_text" : ""
            }
            all_jobs.append(item)
        
        return all_jobs
    
    def __parse_details(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        description_element = soup.find(id='JobDescription')
        description_text = description_element.text.strip()

        return (description_text, str(description_element))
    
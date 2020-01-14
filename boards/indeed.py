from bs4 import BeautifulSoup
import sys

from boards import helpers

class IndeedJobs:
    def __init__(self, url):
        self.url = url

    def get(self):
        page = helpers.download_page(self.url)

        if page is None:
            sys.exit('indeed, there was an error downloading indeed jobs webpage. cannot continue further, so fix this first')
        
        indeed_jobs = self.__parse_index(page)

        for job in indeed_jobs:
            job_content = helpers.download_page(job["href"])
            if job_content is None:
                continue

            parsed_details = self.__parse_details(job_content)
            job["description_text"] = parsed_details[0]
            job["description"] = parsed_details[1]
        
        return indeed_jobs

    def __parse_index(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        jobs_container = soup.find(id='resultsCol')
        job_items = jobs_container.find_all('div', class_='jobsearch-SerpJobCard')

        if job_items is None or len(job_items) == 0:
            return []
        
        all_jobs = []

        for job_elem in job_items:
            url_elem = job_elem.find('a', class_='jobtitle')
            title_elem = job_elem.find('a', class_='jobtitle')
            company_elem = job_elem.find('span', class_='company')

            if None in (title_elem, company_elem, url_elem):
                continue

            href = url_elem.get('href')
            if href is None:
                continue

            item = {
                "title" : title_elem.text.strip(),
                "company" : company_elem.text.strip(),
                "href" : f'https://www.indeed.com{href}',
                "description" : "",
                "description_text" : ""
            }
            all_jobs.append(item)
        
        return all_jobs

    def __parse_details(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        description_element = soup.find(id='jobDescriptionText')
        description_text = description_element.text.strip()

        return (description_text, str(description_element))
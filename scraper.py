from decouple import config, Csv
from boards import indeed, monster

monster_url = config('MONSTER_URL')
indeed_url = config('INDEED_URL')
disgard_list = config('DESCRIPTION_DOESNT_CONTAIN', cast=Csv())

print('Getting jobs from monster.com')
monster = monster.MonsterJobs(monster_url)
monster_jobs = monster.get()
print(f'Found {len(monster_jobs)} job listings within the specified criteria')

print('Getting jobs from indeed.com')
indeed = indeed.IndeedJobs(indeed_url)
indeed_jobs = indeed.get()
print(f'Found {len(monster_jobs)} job listings within the specified criteria')

unfiltered_jobs = monster_jobs + indeed_jobs
filtered_jobs = []

for job in unfiltered_jobs:
    contains_bad_string = any(dis in job["description_text"].lower() for dis in disgard_list)
    if not contains_bad_string:
        print(f'Title: {job["title"]}')
        print(f'Company: {job["company"]}')
        print(f'Url: {job["href"]}')
        print('------------------------------------------------------------------------------')

# todo: send on email
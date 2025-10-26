import requests
from bs4 import BeautifulSoup

from urllib.parse import quote_plus
from datetime import timedelta, datetime

from enum import Enum

class JuniorsRoDate(Enum):
    Last24h = "ultimele-24h"
    Last3Days = "ultimele-3-zile"
    Last7Days = "ultimele-7-zile"
    LastMonth = "ultima-luna"

    def to_param(self) -> str:
        return f"/data:{self.value}"

class JuniorsRoJobType(Enum):
    Job = "100"
    Internship = "200"
    Intern = "300"
    Trainee = "400"
    PreEmployment = "500"
    Bootcamp = "600"
    AcademyPrograms = "650"

    def to_param(l) -> str:
        return f"/tip-job:{','.join(map(lambda x: x.value, l))}"

class JuniorsRoRemote(Enum):
    DontCare = "0"
    Remote = "1"

    def to_param(self) -> str:
        return f"/remote:{self.value}"

class JuniorsRoExperience(Enum):
    NoExperience = "100"
    ZeroTo1Year = "200"
    MoreThanAYear = "300"

    def to_param(l) -> str:
        return f"/experienta:{','.join(map(lambda x: x.value, l))}"

JUNIORS_RO_BASE = "https://www.juniors.ro/jobs"
def make_url(*, search_query: str = None, date: JuniorsRoDate = None, job_types: list[JuniorsRoJobType] = None, remote: JuniorsRoRemote = None, experience: list[JuniorsRoExperience] = None, page: int = None) -> str:
    url = JUNIORS_RO_BASE
    if date is not None:
        url += date.to_param()

    if job_types is not None:
        url += JuniorsRoJobType.to_param(job_types)

    if remote is not None:
        url += remote.to_param()

    if experience is not None:
        url += JuniorsRoJobExperience.to_param(experience)

    if search_query is not None:
        url += f"?q={quote_plus(search_query)}"
    else:
        url += "?q="

    if page is not None:
        url += f"&page={page}"

    return url

class JuniorsRoJob:
    def __init__(self, title, location, time_posted, tags, company):
        self.title = title
        self.location = location
        self.time_posted = time_posted
        self.tags = tags
        self.company = company

    def __str__(self):
        return f"Job Title: {self.title}\n\tLocation: {self.location}\n\tTime Posted: {self.time_posted}\n\tTags: {', '.join(self.tags)}\n\tCompany: {self.company}"

def approximate_time(text: str):
    amount = int(text[:text.index(" ")])

    if "zile" in text or "zi" in text:
        return timedelta(days=amount)

    if "săptămână" in text or "săptămâni" in text:
        return timedelta(weeks=amount)

    return None

def parse_html(html: str) -> (list[JuniorsRoJob], bool):
    b = BeautifulSoup(html, features="html.parser")
    job_list = b.find_all("ul", {"class": "job_list"})[0].find_all("li", {"class": "job"})
    jobs = []
    for job in job_list:
        title = job.select_one("div.job_header div.job_header_title h3").text.strip()
        location, time_posted = map(str.strip, job.select_one("div.job_header div.job_header_title strong").text.split("|"))
        tags = []
        for tag in job.select("ul.job_tags li a"):
            tags.append(tag.text)

        company = job.select_one("div.job_content div.d-flex ul.job_requirements li").text.split(":")[1].strip()
        jobs.append(JuniorsRoJob(title, location, datetime.now() - approximate_time(time_posted), tags, company))

    last_page = 0
    for page in b.select("ul.pagination li.page-item a"):
        try:
            page_num = int(page.text)
            if page_num > last_page:
                last_page = page_num
        except ValueError:
            continue

    current = list(b.find_all("li", {"class": "page-item active"}))
    if len(current) > 0:
        current = int(current[0].select_one("span.page-link").text)
        return (jobs, current, max(current, last_page))
    else:
        return (jobs, 1, 1)

if __name__ == "__main__":
    page_num = 1
    while True:
        url = make_url(search_query="", page=page_num)
        print(f"Url: {url}")
        page = requests.get(url)
        print(f"Status: {page}")
        jobs, current, last = parse_html(page.content)
        for job in jobs:
            print(job)

        print(f"Page {current}/{last}, go to previous [p], to next [n]? ")
        cmd = input()
        if cmd == "p":
            page_num = ((page_num - 2) % last) + 1
        elif cmd == "n":
            page_num = (page_num % last) + 1
        else:
            break

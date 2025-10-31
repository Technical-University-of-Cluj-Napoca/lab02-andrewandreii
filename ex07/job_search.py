import requests
from bs4 import BeautifulSoup

from urllib.parse import quote_plus
from datetime import timedelta, datetime
from argparse import ArgumentParser

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
        url += JuniorsRoExperience.to_param(experience)

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
    if " " not in text:
        return None
    amount = int(text[:text.index(" ")])

    if "ore" in text or "oră":
        return timedelta(hours=amount)

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
        tup = list(map(str.strip, job.select_one("div.job_header div.job_header_title strong").text.split("|")))
        location, time_posted = None, None
        if len(tup) == 3:
            location = tup[1]
            time_posted = tup[2]
        elif len(tup) == 2:
            location = tup[0]
            time_posted = tup[1]

        tags = []
        for tag in job.select("ul.job_tags li a"):
            tags.append(tag.text)

        company = job.select_one("div.job_content div.d-flex ul.job_requirements li").text.split(":")[1].strip()
        jobs.append(JuniorsRoJob(title, location, approximate_time(time_posted) or time_posted, tags, company))

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
    parser = ArgumentParser(prog="job_finder", description="finds jobs!")
    parser.add_argument("search_text", help="The keyword to search on juniors.ro")
    parser.add_argument("--job-types", nargs="+", help=f"A list with the types of jobs you are looking for. Can be: {', '.join(map(lambda x: x.name.lower(), iter(JuniorsRoJobType)))}")
    parser.add_argument("--remote", action="store_true", help="Whether the job should be remote")
    parser.add_argument("--experience", nargs="+", help="list of numbers: 0 - no experience; 1 - less than a year; 2 - more than a year")
    parser.add_argument("--last-days", help="Shows only offers posted in the last specified number of days")
    args = parser.parse_args()

    job_types = []
    if args.job_types:
        for job_type in args.job_types:
            for ty in JuniorsRoJobType:
                if ty.name.lower() == job_type.lower():
                    job_types.append(ty)
                    break
            else:
                print("Invalid type of job")
                exit(-1)
    else:
        job_types = None

    remote = JuniorsRoRemote.Remote if args.remote else JuniorsRoRemote.DontCare

    experiences = []
    if args.experience:
        for experience in args.experience:
            if experience == "0":
                experiences.append(JuniorsRoExperience.NoExperience)
            elif experience == "1":
                experiences.append(JuniorsRoExperience.ZeroTo1Year)
            elif experience == "2":
                experiences.append(JuniorsRoExperience.MoreThanAYear)
            else:
                print("Unknown experience")
                exit(-1)
    else:
        experiences = None

    date = None
    if args.last_days:
        try:
            days = int(args.last_days)
            if days <= 1:
                date = JuniorsRoDate.Last24h
            elif days <= 3:
                date = JuniorsRoDate.Last3Days
            elif days <= 7:
                date = JuniorsRoDate.Last7Days
            elif days <= 31:
                date = JuniorsRoDate.LastMonth
            else:
                date = None
        except ValueError:
            print("Expected number for --last-days")
            exit(-1)

    page_num = 1
    while True:
        url = make_url(search_query=args.search_text, job_types=job_types, experience=experiences, date=date, remote=remote, page=page_num)
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

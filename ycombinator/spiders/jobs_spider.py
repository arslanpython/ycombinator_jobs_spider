import re

from scrapy import Request
from scrapy.spiders import Spider

from ycombinator.items import JobItem
from ycombinator.mysql.job_helper import JobHelper


class JobsSpider(Spider):
    name = 'ycombinator'
    NAME_REGEX = r'(.*\))|(.*)\sis|(.*)\s\W|(.*?\s.*?\s)'
    LOCATION_REGEX = r'\sin\s(.*)|\sat\s(.*)'
    POSITION_REGEX = r'ing\s(.*)\sin|ing\s(.*)'

    start_urls = [
        'https://news.ycombinator.com/jobs',
    ]

    job_helper = JobHelper()
    job_ids = job_helper.get_ids()
    print(job_ids)

    def parse(self, response):
        new_jobs = []
        job_ids = response.css('.athing::attr(id)').getall()
        raw_jobs = response.css('.storylink::text').getall()

        for job_id, raw_job in zip(job_ids, raw_jobs):
            if (job_id,) in self.job_ids:
                continue
            job = JobItem()
            job['job_id'] = job_id
            job['name'] = self.get_company_name(raw_job)
            job['location'] = self.get_location(raw_job)
            job['position'] = self.get_position(raw_job)

            new_jobs.append(job)
            yield job

        self.job_helper.insert_db(new_jobs)

        urls_s = response.css('.morelink')
        yield from [response.follow(url_s, callback=self.parse) for url_s in urls_s]

        # urls = response.css('.morelink::attr(href)').getall()
        # for url in urls:
            # yield Request('/'+url, callback=self.parse)

    def get_company_name(self, text):
        return self.clean(re.search(self.NAME_REGEX, text, flags=re.I).groups(''))

    def get_location(self, text):
        return self.clean(re.findall(self.LOCATION_REGEX, text, flags=re.I))

    def get_position(self, text):
        return self.clean(re.findall(self.POSITION_REGEX, text, flags=re.I))

    def clean(self, data):
        if isinstance(data, tuple):
            return [e.strip() for e in data if e and e.strip()][0]

        if isinstance(data, list):
            data = [e.strip() for seq in data for e in seq if e and e.strip()]
            return data[0] if data else ''

        if isinstance(data, str):
            return data.strip()

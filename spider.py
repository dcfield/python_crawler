from urllib.request import urlopen
from link_finder import Linkfinder
from general import *
from domain import *


class Spider:

    # Class variables (shared among all instances)
    project_name = ''
    crawled_name = ''
    base_url = ''
    domain_name = ''
    crawled_file = ''
    queue_file = ''
    queue_set = set()
    crawled_set = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.crawled_set = file_to_set(Spider.crawled_file)
        Spider.queue_set = file_to_set(Spider.queue_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print(thread_name + ' is now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue_set)) + ' | Crawled ' + str(len(Spider.crawled_set)))

            Spider.add_links_to_queue(Spider.gather_links(page_url))

            if page_url in Spider.queue_set:
                Spider.queue_set.remove(page_url)

            Spider.crawled_set.add(page_url)

            # Update the files
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-type'):
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')

            # Get all links
            finder = Linkfinder(Spider.base_url, page_url)
            finder.feed(html_string)

            return finder.page_links()

        except Exception as e:
            print(str(e))
            return set()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:

            # Check we don't already have link
            if url in Spider.queue_set:
                continue
            if url in Spider.crawled_set:
                continue

            # Make sure we don't add a link that points towards a different site
            if Spider.domain_name != get_domain_name(url):
                continue

            # Add to waiting list
            Spider.queue_set.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue_set, Spider.queue_file)
        set_to_file(Spider.crawled_set, Spider.crawled_file)

from urllib.request import urlopen
from link_finder import Linkfinder
from general import *

class Spider:

    # Class variables (shared amoung all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue_set = set()
    crawled_set = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.crawled_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print(thread_name + ' is now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))

            Spider.add_links_to_queue(Spider.gather_links(page_url))

            # Move from waiting list to crawl list
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)

            # Update the files
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response= urlopen(page_url)
            if response.getheader('Content-type') == 'text/html':
                html_bytes = repsonse.read()
                html_string = html_bytes.decode('utf-8')

            # Get all links
            finder = LinkFinder(Spider.base_url, page_url)
            find.feed(html_string)

            return finder.page_links()

        except:
            print('Error: cannot crawl page')
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
            if Spider.domain_name not in url:
                continue

            # Add to waiting list
            queue_set.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

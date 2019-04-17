from urllib.request import urlopen, Request

from newspaper import Article

from domain_features import hardRules
from link_finder import LinkFinder
from domain import *
from general import *
import codecs


class Spider:
    # Class variables, shared among all objects
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    page_count = 0

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.html_pages = Spider.project_name + '/html/'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_project_dir(Spider.html_pages)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            if Spider.page_count<100:
                Spider.update_files()

    @staticmethod
    def gather_links_and_text(page_url):
        if page_url in Spider.crawled:
            Spider.queue.remove(page_url)
            print("***************************** Duplicate found!!!!!!!!!!!!!!!!")
            return set()

        else:
            html_string = ''
            try:
                article = Article(page_url, language='bn')
                article.download()
                article.parse()

                html_string = article.html
                Spider.news += article.title + '\n' + article.text

                Spider.page_count += 1
                file = codecs.open(Spider.html_pages + randomString(4) + '.html', "a", "utf-8")
                file.write(html_string)
                file.close()

                if Spider.page_count % 100 == 0:
                    with codecs.open(Spider.project_name + '/all_texts.txt', "a", "utf-8") as w:
                        for l in Spider.news:
                            w.write(l)
                    Spider.news = ""

                # find the links
                finder = LinkFinder(Spider.base_url, page_url)
                finder.feed(html_string)

            except Exception as e:
                print(str(e))
                return set()
            return finder.page_links()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        if page_url in Spider.crawled:
            Spider.queue.remove(page_url)
            print("***************************** Duplicate found!!!!!!!!!!!!!!!!")
            return set()

        else:
            html_string = ''
            try:
                req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(req)
                if 'text/html' in response.getheader('Content-Type'):
                    # read the html in byte format
                    html_bytes = response.read()
                    # convert the webpage in string format
                    html_string = html_bytes.decode("utf-8")

                    # save the html files
                    # file = codecs.open(Spider.html_pages+"_".join(page_url.split('/')[2:])+'.html', "w", "utf-8")
                    Spider.page_count += 1
                    # file = codecs.open(Spider.html_pages + str(Spider.page_count)+ '.html', "a", "utf-8")
                    file = codecs.open(Spider.html_pages + randomString(4) + '.html', "a", "utf-8")
                    # file = codecs.open('raw_files.txt', "a", "utf-8")
                    file.write(html_string)
                    file.close()

                    if Spider.page_count % 100 == 0:
                        Spider.update_files()

                # find the links
                finder = LinkFinder(Spider.base_url, page_url)
                finder.feed(html_string)

            except Exception as e:
                print(str(e))
                return set()
            return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue

            if hardRules(url):
                continue

            # Check if this is the same website/ Not going other site
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

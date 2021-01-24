import argparse
import os
from facebook_scraper import get_posts
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

class FbScraper:
    wordlist = ""
    page = "."

    def __init__(self, wordlist):
        self.wordlist = wordlist

    # validate that word in wordlist appears in text string
    def valid_post(self, text):
        if not self.wordlist:
            return True
        for e in self.wordlist:
            if e in text:
                return True
        return False

    # get post url and screenshot in headless browser if post is valid
    def download_post(self, post):
        # validate post
        if type(post['post_url']) == str and self.valid_post(post['text']):
            # instantiate web driver
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)

            # get post and take screenshot
            driver.get(post['post_url'])
            print(str(post["time"]) + ".png")
            driver.get_screenshot_as_file(self.page + "/" + str(post["time"]) + ".png")
            driver.quit()

    # pull list of posts from FB then using pool call screenshot on each
    def scrape_page(self, page, pages=1):
        self.page = page
        posts = get_posts(page, pages=pages)
        for e in posts:
            # rate limit to avoid fb blocking
            sleep(30)
            self.download_post(e)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--page',
                        help='Name of facebook page')
    parser.add_argument('-w',
                        '--words',
                        default=[],
                        nargs='*',
                        help='List of words to validate in page')
    parser.add_argument('-n',
                        '--num-pages',
                        type=int,
                        default=1,
                        help='Number of pages to check')

    return parser.parse_args()


if __name__ == "__main__":
    opts = parse_args()
    try:
        os.mkdir(opts.page)
    except OSError as error:
        print("Folder " + opts.page + " exists")

    scraper = FbScraper(wordlist=opts.words)
    scraper.scrape_page(opts.page, pages=opts.num_pages)

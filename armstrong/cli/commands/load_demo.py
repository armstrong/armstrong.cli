import datetime
from pyquery import PyQuery as pq
import re
import requests
from requests import async

today = datetime.datetime.now()
BASE_URL = "http://en.wikinews.org"
CATEGORY_URL = "%s/wiki/Category:%%s" % BASE_URL


def process_page(response):
    doc = pq(response.text)
    published_date = doc.find(".published")
    if published_date:
        published_date = datetime.datetime.strptime(published_date.text(),
                "%A, %B %d, %Y")
    article = pq("<article>")
    is_draft = False
    # import ipdb; ipdb.set_trace()
    for e in doc.find("div.mw-content-ltr").children():
        if e.tag == "center":
            break  # Break as soon as we see the bottom "contribute" call to action
        if e.attrib.get("class", "") in ["infobox", "toc"]:
            continue
        if not is_draft:
            is_draft = "metadata" in e.attrib.get("class", "")
            continue
        article.append(e)

    article = article.html()
    return {
        "published_date": published_date,
        "is_draft": is_draft,
        "article": article.strip() if article else "",
    }


def is_recap_post(a):
    return bool(re.findall(r"\d{4}/\w+/\d{1,2}$", a.attrib["href"]))


class LoadDemoData(object):
    """
    Load in initial demo data from WikiNews
    """

    def build_parser(self, parser):
        pass

    def __call__(self, **kwargs):
        urls = []
        data = {}
        for i in range(5):
            date = today - datetime.timedelta(days=i)
            url = CATEGORY_URL % (date.strftime("%B_%%d,_%Y") % date.day)
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception("Unable to process response: %d" % response.status_code)
                continue
            doc = pq(response.text)
            for a in doc.find("div.mw-content-ltr li a"):
                if is_recap_post(a):
                    continue
                urls.append(async.get("%s%s" % (BASE_URL, a.attrib["href"])))
            responses = async.map(urls)
            for i in range(len(responses)):
                data[urls[i].url] = process_page(responses[i])
            print "grabbed %d for %s" % (len(responses), date)

        for url in data:
            print "-" * 80
            print "URL: %s" % url
            print "Published: %s" % data[url]["published_date"]
            print "Draft: %s" % data[url]["is_draft"]
            print ""
            print data[url]["article"]
            print "\n\n"


load_demo_data = LoadDemoData()
if __name__ == "__main__":
    load_demo_data()

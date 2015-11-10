from lxml import html
import re

def get_osbmc_ids_for_weeks():

    # save http://thefive.sabic.uberspace.de/blog/list as "HTML only"

    tree = html.parse('OSMBC.htm')

    anchors = tree.xpath('//a')

    # prices = tree.xpath('//span[@class="item-price"]/text()')

    osmbc_weeks = {}

    for a in anchors:
        text = a.text
        link = a.get("href")
        if re.match(r'WN\d+', text) and re.match(r'/blog', link):
            week_number = int(re.sub(r'[^0-9]', '', text))
            osmbc_id = int(re.sub(r'[^0-9]', '', link))
            #print("\"%s\" \"%s\"" % (text, link))
            osmbc_weeks[week_number] = osmbc_id

    return osmbc_weeks


if __name__ == "__main__":
    print(get_osbmc_ids_for_weeks())

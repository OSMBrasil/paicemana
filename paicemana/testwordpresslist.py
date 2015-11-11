from lxml import html
import re

def get_wordpress_ids_for_weeks():

    # save http://www.weeklyosm.eu/wp-admin/edit.php as "HTML only"

    tree = html.parse('WEEKLYOSM.htm')

    anchors = tree.xpath('//a[@class="row-title"]')

    # prices = tree.xpath('//span[@class="item-price"]/text()')

    wordpress_weeks = {}

    for a in anchors:
        text = a.text
        link = a.get('href')
        if re.match(r'[Ww]eekly +[\d-]+', text) and re.match(r'\S+post=\d+&action=edit', link):
            week_number = text.split()[1]
            tmp = re.sub(r'\S+post=', '', link)
            tmp = re.sub(r'&action=edit', '', tmp)
            wordpress_id = int(tmp)
            #print(week_number, " ", wordpress_id)
            multiple = week_number.split('-')
            tmp = []
            for i in multiple:
                tmp.append(int(i))
            multiple = list(tmp)
            #print(multiple, wordpress_id)

            for i in multiple:
                wordpress_weeks[i] = {'wordpress':wordpress_id}
                if len(multiple) > 1:
                    tmp = list(multiple)
                    tmp.remove(i)
                    wordpress_weeks[i]['multiple'] = tmp

    return wordpress_weeks


def test_pretty_json(config):
    import json
    print(json.dumps(config, sort_keys=True, indent=4))


if __name__ == "__main__":
    #print(get_wordpress_ids_for_weeks())
    test_pretty_json(get_wordpress_ids_for_weeks())


""" Exemplo (quebrado) com dados fictícios:
{
    "277": {
        "osmbc": 36335,
        "wordpress": 262625
        "multiple": [18181, 17171, 17171],
        "image": "5751"
    }
}
"""


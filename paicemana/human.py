from lxml import html
from string import Template

import json, os, re

from primate import GetListOSMBC, GetListWordpress


def get_osbmc_ids_for_weeks():

    # save http://thefive.sabic.uberspace.de/blog/list as "HTML only"

    tree = html.parse(GetListOSMBC.FILENAME)

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


def get_wordpress_ids_for_weeks():

    # save http://www.weeklyosm.eu/wp-admin/edit.php as "HTML only"

    tree = html.parse(GetListWordpress.FILENAME)

    anchors = tree.xpath('//a[@class="row-title"]')

    # prices = tree.xpath('//span[@class="item-price"]/text()')

    wordpress_weeks = {}

    for a in anchors:
        text = a.text.replace('/', '-').replace('–', '-')
        link = a.get('href')
        if re.match(r'[Ww]eekly +[\d-]+', text) and re.match(r'\S+post=\d+&action=edit', link):
            week_number = text.split()[1]
            tmp = re.sub(r'\S+post=', '', link)
            tmp = re.sub(r'&action=edit', '', tmp)
            wordpress_id = int(tmp)
            #print(week_number, " ", wordpress_id)
            week_number = re.sub(r'^-+', '', week_number)
            week_number = re.sub(r'-+$', '', week_number)
            multiple = week_number.split('-')
            tmp = []
            for i in multiple:
                tmp.append(int(i))
            multiple = list(tmp)
            #print(multiple, wordpress_id)

            for i in multiple:
                wordpress_weeks[i] = {'wordpress': wordpress_id}
                if len(multiple) > 1:
                    tmp = list(multiple)
                    tmp.remove(i)
                    wordpress_weeks[i]['multiple'] = tmp

    return wordpress_weeks


def get_weeks_data():
    wordpress_weeks = get_wordpress_ids_for_weeks()
    osmbc_weeks = get_osbmc_ids_for_weeks()
    data = wordpress_weeks  # reference
    for week in osmbc_weeks:  # ideally the OSMBC has all
        if week in data:
            data[week]['osmbc'] = osmbc_weeks[week]
        else:
            data[week] = {'osmbc': osmbc_weeks[week]}
    return data


def test_pretty_json(config):
    print(json.dumps(config, sort_keys=True, indent=4))

def test_pretty_json_file(config):
    with open(os.path.expanduser('~/.paicemana.json'), 'w') as outfile:
        json.dump(config, outfile, sort_keys=True, indent=4)


class CorrelationJSON():  # will be like a manager

    def __init__(self):
        self.data = {}

    def load(self):
        with open(os.path.expanduser('~/.paicemana.json'), 'r') as infile:
            self.data = json.load(infile)

    def sync(self):
        with open(os.path.expanduser('~/.paicemana.json'), 'w') as outfile:
            json.dump(get_weeks_data(), outfile, sort_keys=True, indent=4)

    # obj.query(['osmbc','wordpress'], True)
    # obj.query(['multiple'], exclude=True)
    def query(self, keys, reset=False, exclude=False):
        result = {}
        for number in self.data:
            keys_present = True
            for key in keys:
                if not key in self.data[number]:
                    keys_present = False
            if (keys_present and not exclude) or (not keys_present and exclude):
                result[number] = self.data[number]
        if reset:
            self.data = result
        return result

    def non_multiples(self):
        self.query(['wordpress','osmbc'], True)
        self.query(['multiple'], True, exclude=True)

    def get_osmbc_id_for(self, week):
        return self.data[str(week)]['osmbc']

    def get_wordpress_id_for(self, week):
        return self.data[str(week)]['wordpress']


class ImageCode():

    template = '[caption id="attachment_$id" align="align$align" width="$width"]<a href="$url"><img class=" wp-image-$id" src="$url" alt="$alt" width="$width" height="$height" /></a>$text[/caption]'

    def __init__(self,
        id = 12684,
        align = 'center',
        width = 807,
        height = 606,
        url = 'http://blog.openstreetmap.de/wp-uploads//2015/11/before-after-road-styles-2.jpg',
        alt = 'neuer Carto Map Style auf osm.org',
        anchor = '#wn276_mapas',  # anchor=None to use a full HTML as text value
        text = 'New OSM Carto Map Style at osm.org [1] <br/> Data: OpenStreetMap-Contributors, Image CC-BY-SA 2.0 <a href="http://www.openstreetmap.org/">OpenStreetMap.org</a>'
    ):
        if anchor:
            text = text.replace('[1]', '<a href="%s">[1]</a>' % anchor)

        self.id = id
        self.align = align
        self.width = width
        self.height = height
        self.url = url
        self.alt = alt
        self.text = text

    def __str__(self):
        t = Template(ImageCode.template)
        return t.substitute(
            id = self.id,
            align = self.align,
            width = self.width,
            height = self.height,
            url = self.url,
            alt = self.alt,
            text = self.text
        )
        # or http://stackoverflow.com/a/2451826 (Python 2)
        # or http://stackoverflow.com/a/2452382 (Python 3)


if __name__ == "__main__":

    myjson = CorrelationJSON()
    myjson.load()
    myjson.non_multiples()
    print(myjson.get_osmbc_id_for(276))
    print(myjson.get_wordpress_id_for(276))

    exit(0)

    #print(ImageCode())
    #print(get_weeks_data())

    myjson = CorrelationJSON()
    #myjson.sync()
    myjson.load()
    #print(myjson.data)
    r = myjson.query(['wordpress','osmbc'], True)
    test_pretty_json(r)
    r = myjson.query(['multiple'], exclude=True)
    test_pretty_json(r)

    exit(0)

    print(get_osbmc_ids_for_weeks())
    data = get_wordpress_ids_for_weeks()
    #print(ids)
    test_pretty_json(data)
    test_pretty_json_file(data)


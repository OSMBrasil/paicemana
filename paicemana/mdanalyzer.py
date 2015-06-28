from codecs import open as codecs_open
from sortedcontainers import SortedList  # TODO in setup.py

import re
import math


class WorkOrganizer(object):

    def __init__(self):
        self.sections = []

    def save(self, section):
        self.sections.append(section)

    def distribute_for(self, translators):
        self.translators = TranslatorsSpinner(translators)  # do a carousel?  
        self.__assign_translations__()
        self.__assign_revisions__()

    def __new_stack__(self):
        factor = math.sqrt(len(self.sections))
        stack = SortedList(load=round(factor))
        for section in self.sections:
            stack.add(section)
        return stack

    def __assign_translations__(self):
        stack = self.__new_stack__()
        while len(stack) > 0:
            section = stack.pop()
            section.translator = self.translators.next()   
 
    def __assign_revisions__(self):
        stack = self.__new_stack__()
        while len(stack) > 0:
            section = stack.pop()
            one = self.translators.next()
            if one == section.translator:
                one = self.translators.next()  # TODO fix for unique reviser
            section.reviser = one

    def scores(self):
        s = ''
        for people in self.translators.array:
            score_translations = 0
            score_revisions = 0
            for section in self.sections:
                if section.translator == people:
                    score_translations += section.score
                if section.reviser == people:
                    score_revisions += section.score
            s += '%s %s %s\n' % (score_translations, score_revisions, people)
        return s[:-1]
    
    def __repr__(self):
        s = ''
        for section in self.sections:
            s += '%s %s %s %s\n' % (
                                        section.score,
                                        section.translator,
                                        section.name,
                                        section.reviser
                                    )
        return s[:-1]

    def __len__(self):
        return len(self.sections)

class TranslatorsSpinner(object):

    def __init__(self, array):
        self.index = 0
        self.array = array

    def next(self):
        if len(self.array) == 0:
            return None
        if self.index < len(self.array):
            return self.__next__()
        else:
            self.index = 0
            return self.__next__()

    def __next__(self):
        pos = self.index
        self.index += 1
        return self.array[pos]


class MarkdownSection(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.translator = None
        self.reviser = None

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __eq__(self, other):
        return self.score == other.score

    def __ne__(self, other):
        return self.score != other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __hash__(self):
        return hash(self.name + str(self.translator) + str(self.reviser))


class MarkdownAnalyzer(object):

    def __init__(self, filename):
        with codecs_open(filename, encoding='utf-8') as f:
            self.text = f.read()
    
    def __text_without_links__(self):
        return re.sub(r'\(http.*\)', '', self.text)

    def getOrganizer(self):
        s = self.__text_without_links__()
        md_sections_collection = s.split('\n#')  # 11
        organizer = WorkOrganizer()
        for section in md_sections_collection:
            name = section.splitlines()[0]
            name = re.sub(r'^#* *', '', name)
            score = len(section)
            organizer.save(MarkdownSection(name, score))
        return organizer


def test_spinner(spinner):
    print(spinner.next())
    print(spinner.next())
    print(spinner.next())
    print(spinner.next())
    print(spinner.next())
    print(spinner.next())
    print(spinner.next())
    print(spinner.next())
    print(spinner.next())
    print(spinner.next())
    print(len(organizer))


if __name__ == "__main__":
    analyzer = MarkdownAnalyzer('archive-4205.md')
    organizer = analyzer.getOrganizer()
    translators = ['alexandre-mbm', 'jgpacker', 'vgeorge']
    organizer.distribute_for(translators)
    #print(organizer)
    print(organizer.scores())
    #spinner = TranslatorsSpinner(translators)
    #test_spinner(spinner)


# -*- coding:utf-8 -*-

class Property:
    def __init__(self, l):
        self.label = l
        self.articles = []
        self.values = []
        self.domain = ""

class Domain:
    def __init__(self, t):
        self.domain = t #wiki template
        self.wiki_properties = {}
        self.baidu_properties = {}

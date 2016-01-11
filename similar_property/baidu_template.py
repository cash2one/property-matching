# -*- coding:utf-8 -*-
from similarity import *

import os

from fileio import *
from model import *

"""
找到enwiki Template领域下，baidu中涉及的property
"""

def replace_by_crosslingual(tem_con, *clfns):
    cl = {}
    for fn in clfns:
        for line in open(fn):
            a, b = line.strip('\n').split('\t')
            cl[a] = b

    d = {}
    for tem, cons in tem_con.iteritems():
        d[tem] = set([cl[con] for con in cons if con in cl])
    return d

def tfidf_filter(tem_attrs_count, tem_zhins):
    attr_count = {}
    #for t, ats in tem_attrs_count.iteritems():
    #    for a, c in ats.iteritems():
    #        attr_count[a] = attr_count.get(a, 0)+c
        
    for t, attrs in tem_attrs_count.iteritems():
        total = sum(attrs.values())
        for a in attrs:
            #tf = attrs[a] * 1.0/attr_count[a]
            #tf = attrs[a] * 1.0/total
            tf = attrs[a] * 1.0/len(tem_zhins[t])
            if tf > 0.3:
                print t,a,tf
            #idf = -math.log(sum([1 for c in cons if p in c.properties])*1.0/len(cons))
            idf = math.log(len(tem_attrs_count)/(0.1+sum([1 for t in tem_attrs_count if a in tem_attrs_count[t]])*1.0))
            #print t, a, tf*idf

def generate_domain_properties():
    tem_domain = read_wiki_properties(ENWIKI_INFOBOX)
    inses = []
    for domain in tem_domain.itervalues():
        for prop in domain.wiki_properties:
            inses += prop.articles

    ins_con = read_wiki_instance_concept(ENWIKI_INSTANCE_CONCEPT, set(inses))
    del inses
    tem_con = {}
    print "tem_con"
    for tem, inses in tem_ins.iteritems():
        s = []
        for ins in inses:
            s += ins_con[ins]
        tem_con[tem] = set(s)
    del tem_ins, ins_con

    tem_zhcon = replace_by_crosslingual(tem_con, WIKI_CROSSLINGUAL)
    del tem_con
    zh_con_ins = read_baidu_concept_instance(BAIDU_INSTANCE_CONCEPT)
    tem_zhins = {}
    print "tem_zhins"
    for tem, cons in tem_zhcon.iteritems():
        s = []
        for con in cons:
            if con in zh_con_ins:
                s += zh_con_ins[con]
        tem_zhins[tem] = set(s)
    del zh_con_ins
    zh_ins_attr = read_instance_property(BAIDU_INFOBOX)
    tem_baiduattr_count = {}
    for tem, inses in tem_zhins.iteritems():
        a_c = {}
        for ins in inses:
            if ins in zh_ins_attr:
                for a in zh_ins_attr[ins]:
                    a_c[a] = a_c.get(a, 0)+1
        tem_baiduattr_count[tem] = a_c
    ##### 算法
    tfidf_filter(tem_baiduattr_count, tem_zhins)
    #####

    count = 0
    f = open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE, 'w')
    print "Templates:",len(tem_baiduattr_count)
    for tem, attrs in sorted(tem_baiduattr_count.items()):
        if len(attrs) > 0:
            print tem, len(attrs)
            f.write(tem+'\t'+':::'.join(attrs.keys())+'\n')
            f.flush()
            count += 1
    f.close()
    print "Templates which have attrs Count:",count
    
    baidu_properties = read_baidu_properties(BAIDU_INFOBOX)
    for tem, attrs in tem_baiduattr_count.items():
        if len(attrs) > 0:
            for a in attrs:
                tem_domain[tem].baidu_properties[a] = baidu_properties[a]
    return tem_domain
    

def find_attribute_in_baidu():
    """
    1. 找到使用template的instance
    2. 找到这些instance涉及的概念
    3. 通过已有的跨语言概念链接，找到baidu中对应的概念
    4. 通过概念下的instance， 找到概念下的attribute
    或者？？
    直接用跨语言instance？
    """
    tem_ins = read_wiki_infobox(ENWIKI_INFOBOX)
    inses = []
    for ins in tem_ins.itervalues():
        inses += ins
    ins_con = read_wiki_instance_concept(ENWIKI_INSTANCE_CONCEPT, set(inses))
    del inses
    tem_con = {}
    print "tem_con"
    for tem, inses in tem_ins.iteritems():
        s = []
        for ins in inses:
            s += ins_con[ins]
        tem_con[tem] = set(s)
    del tem_ins, ins_con

    tem_zhcon = replace_by_crosslingual(tem_con, WIKI_CROSSLINGUAL)
    del tem_con
    zh_con_ins = read_baidu_concept_instance(BAIDU_INSTANCE_CONCEPT)
    tem_zhins = {}
    print "tem_zhins"
    for tem, cons in tem_zhcon.iteritems():
        s = []
        for con in cons:
            if con in zh_con_ins:
                s += zh_con_ins[con]
        tem_zhins[tem] = set(s)
    del zh_con_ins
    zh_ins_attr = read_instance_property(BAIDU_INFOBOX)
    tem_baiduattr_count = {}
    for tem, inses in tem_zhins.iteritems():
        a_c = {}
        for ins in inses:
            if ins in zh_ins_attr:
                for a in zh_ins_attr[ins]:
                    a_c[a] = a_c.get(a, 0)+1
        tem_baiduattr_count[tem] = a_c
    #tfidf_filter(tem_baiduattr_count, tem_zhins)

    count = 0
    f = open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE, 'w')
    print "Templates:",len(tem_baiduattr_count)
    for tem, attrs in sorted(tem_baiduattr_count.items()):
        if len(attrs) > 0:
            print tem, len(attrs)
            f.write(tem+'\t'+':::'.join(attrs.keys())+'\n')
            f.flush()
            count += 1
    f.close()
    print "Templates which have attrs Count:",count

def find_attribute_in_baidu2():
    """
    1. 找到使用template的instance
    2. 找到这些instance涉及的概念
    3. 通过已有的跨语言概念链接，找到baidu中对应的概念
    4. 通过跨语言instance， 找到template下的attribute
    """
    tem_ins = read_wiki_infobox(ENWIKI_INFOBOX)
    inses = []
    for ins in tem_ins.itervalues():
        inses += ins
    tem_zhins = replace_by_crosslingual(tem_ins, WIKI_CROSSLINGUAL)
    print "tem_zhins"
    zh_ins_attr = read_instance_property(BAIDU_INFOBOX)
    tem_baiduattr_count = {}
    for tem, inses in tem_zhins.iteritems():
        a_c = {}
        for ins in inses:
            if ins in zh_ins_attr:
                for a in zh_ins_attr[ins]:
                    a_c[a] = a_c.get(a, 0)+1
        tem_baiduattr_count[tem] = a_c
    #tfidf_filter(tem_baiduattr_count, tem_zhins)

    count = 0
    f = open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE, 'w')
    print "Templates:",len(tem_baiduattr_count)
    for tem, attrs in sorted(tem_baiduattr_count.items()):
        if len(attrs) > 0:
            print tem, len(attrs)
            f.write(tem+'\t'+':::'.join(attrs.keys())+'\n')
            f.flush()
            count += 1
    f.close()
    print "Templates which have attrs Count:",count


if __name__ == "__main__":
    import time
    start = time.time()
    find_attribute_in_baidu()
    print "Time Consuming:", time.time()-start


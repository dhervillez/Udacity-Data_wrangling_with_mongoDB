#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 22:33:39 2018

@author: thomas
"""

"""
Audit school type in the OSM_FILE
Correct school type with update_school_type function

School type shall be maternelle, élémentaire, collège or lycée
"""

import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict


def is_school_type(elem):
    """return boolean that assess value of the tag key compared to 'school:FR'"""
    return (elem.attrib['k'] == 'school:FR')


def audit(osmfile):
    """Build a set of school type"""
    osm_file = open(osmfile, "r")
    school_set = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_school_type(tag):
                    school_set.add(tag.attrib['v'])
    osm_file.close()
    return school_set


def update_school_type(name):
    """Change school type to be homogeneous"""
    name=re.sub('primaire','maternelle;élémentaire', name)
    name=re.sub('secondaire','collège;lycée', name)
    return name


if __name__ == '__main__':

    OSM_PATH = "Toulouse.osm"
    school_set = audit(OSM_PATH)
    pprint.pprint(school_set)
    
    for name in school_set:
        better_name=update_school_type(name)
        print better_name
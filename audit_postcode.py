#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 22:27:05 2018

@author: thomas
"""

"""
Audit street types in the OSM_FILE
Correct street type with update_street_name function

List of main street types is stored in expected_street_type
Mapping of street type correction is in street_mapping dictionnary
"""

import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict

#regual expression is modified because in French street type is at the beginning of the name
postcode_re=re.compile(ur'^31[0-9]{3}$')

def is_postcode(elem):
    """return boolean that assess value of the tag key compared to 'addr:postcode'"""
    return (elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    """Return a set of postcode not expected"""
    osm_file = open(osmfile, "r")
    postcode_set = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    m = postcode_re.search(tag.attrib['v'])
                    if not m:
                        postcode_set.add(tag.attrib['v'])

    osm_file.close()
    return postcode_set


def update_postcode(postcode):
    """Change postcode by keeping first 5 digits"""
    
    return postcode[:5]


if __name__ == '__main__':

    OSM_PATH = "Toulouse.osm"

#    postcode_set = audit(OSM_PATH)
#    pprint.pprint(postcode_set)
    
    for postcode in postcode_set:
        better_name=update_postcode(postcode)
        print better_name
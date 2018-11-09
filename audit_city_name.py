#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 22:33:39 2018

@author: thomas
"""

"""
Audit city name in the OSM_FILE
Correct city name with update_city_name function

Mapping of city name correction is in city_mapping dictionnary
"""

import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict


city_mapping = {"Ramonville" : "Ramonville Saint Agne","Ramonville St Agne":"Ramonville Saint Agne",
                "Rouffiac":"Rouffiac Tolosan",
                "Saint Orens":"Saint Orens De Gameville",
                "Toulouse Blagnac":"Toulouse", "Toulouse Cedex 1":"Toulouse","Toulouse Cedex 5":"Toulouse",
                "Vieille":"Vieille Toulouse"
                }


def is_city_name(elem):
    """return boolean that assess value of the tag key compared to 'addr:city'"""
    return (elem.attrib['k'] == "addr:city")


def audit(osmfile):
    """Build a set of city name"""
    osm_file = open(osmfile, "r")
    city_set = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    city_set.add(tag.attrib['v'])
    osm_file.close()
    return city_set


def update_city_name(name,mapping):
    """Change case of the city name (lowercase except first letters) and replace "-" by " " """
    """Change city name if in city_mapping dictionnay"""
    name=name.title().replace('-',' ')
    if name in mapping:
        name=mapping[name]
    return name


if __name__ == '__main__':

    OSM_PATH = "Toulouse.osm"
    city_set = audit(OSM_PATH)
    pprint.pprint(city_set)
    
    city_set2=set()
    
    for name in city_set:
        better_name=update_city_name(name,city_mapping)
        city_set2.add(better_name)
    pprint.pprint(city_set2)
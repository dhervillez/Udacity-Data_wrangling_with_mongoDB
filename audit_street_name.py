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
street_type_re = re.compile(ur'^\b\S+\.?', re.IGNORECASE)

expected_street_type = ["Allee","Avenue","Angle","Boulevard", "Chemin", "Cheminement", "Clos", "Court",
                        "Descente", "Esplanade","Impasse","Passage","Lotissement","Mail", "Place","Port",
                        "Promenade", "Quai", "Rue", "Route","Rond-Point","Square","Voie"]

street_mapping = {"ALLEE" : "Allee", u'All\xe9e':"Allee", u'All\xe9es':"Allee", u'all\xe9e':"Allee", u'all\xe9es':"Allee",
                  "AVENUE" : "Avenue", "Av." : "Avenue", "Bd": "Boulevard", "avenue": "Avenue", "chemin" : "Chemin",
                  "C.c.": "Centre Commercial", "CC": "Centre Commercial", "impasse":"Impasse", "Palce": "Place", "place": "Place",
                  "R.N" : "Route Nationale", "R.n." : "Route Nationale", "ROUTE" : "Route", "route" :"Route", "rte": "Route",
                  "RUE" : "Rue", "rue": "Rue", "esplanade": "Esplanade", "square":"Square", "voie":"Voie"}


def audit_street_type(street_types, street_name):
    """Build a dictionnary of unexpected street types (first word of street name in French)"""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street_type:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """return boolean that assess value of the tag key compared to 'addr:street'"""
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """Return a dictionnary of street types not found in the expected_street_type list"""
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_street_name(name, mapping):
    """Change street types if in street_mapping dictionnay"""
    street_type=street_type_re.search(name).group()
    if street_type in mapping:
        name=name.replace(street_type, mapping[street_type])
    return name


if __name__ == '__main__':

    OSM_PATH = "Toulouse.osm"

    st_types = audit(OSM_PATH)
    pprint.pprint(dict(st_types))
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_street_name(name, street_mapping)
            print better_name
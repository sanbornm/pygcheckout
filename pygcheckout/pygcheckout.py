"""Pygcheckout: Python Wrapper for Google Checkout"""

__author__ = 'marcrosoft@gmail.com (Mark Sanborn)'

VERSION = '0.0.1'

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from datetime import datetime, date, time
import urllib2
import ConfigParser
from base64 import b64encode

def get_config_default(default,section="Generic"):
    """Get the default configuration default from the current directory"""

    config = ConfigParser.ConfigParser()
    config.readfp(open('config.cfg'))
    try:
        value = config.get(section, default)
        return value
    except:
        return ''

def send_xml_data(url, xml):
    """Sends xml data to specified url and returns response"""

    req = urllib2.Request(url, data=xml)

    req.add_header('Authorization',
                       'Basic %s' % (b64encode('%s:%s' % (get_config_default('testId'),
                                                          get_config_default('testKey'))),))
    req.add_header('Content-Type', ' application/xml; charset=UTF-8')
    req.add_header('Accept', ' application/xml; charset=UTF-8')

    try:
        r = urllib2.urlopen(req)
        result = r.read()
    except: 
        result = "The url: %s is not responding." % (url)
    return result

def indent(elem, level=0):
    """Indents and makes XML output pretty."""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def pretify_xml_string(xml):
    """Take xml blob and indent it properly"""

    xmlObject = ET.fromstring(xml)
    indent(xmlObject)
    xmlString = ET.tostring(xmlObject)

    return xmlString

class Cart:

    def __init__(self):
        root = ET.Element("checkout-shopping-cart")
        root.set("xmlns", "http://checkout.google.com/schema/2")

        shoppingcart = ET.SubElement(root, "shopping-cart")

        items = ET.SubElement(shoppingcart, "items")
        self.root = root
    
    def get_google_url(self):
        if get_config_default('debugMode') == '1':
            upsUrl = 'https://sandbox.google.com/checkout/api/checkout/v2/request/Merchant/%s' % (get_config_default('testId'))
        else:
            upsUrl = 'https://checkout.google.com/api/checkout/v2/request/Merchant/%s' % (get_config_default('productionId'))
        return upsUrl

    def add_item(self, itemDictionary):
        root = self.root

        items = root.find("shopping-cart/items")

        item = ET.SubElement(items, "item")
        
        itemname = ET.SubElement(item, "item-name")
        itemname.text = itemDictionary['name']

        itemdescription = ET.SubElement(item, "item-description")
        itemdescription.text = itemDictionary['description']

        itemprice = ET.SubElement(item, "item-price")
        itemprice.text = itemDictionary['price']

        itemquantity = ET.SubElement(item, "item-quantity")
        itemquantity.text = itemDictionary['quantity']

        indent(root)
        xmlString = ET.tostring(root)

        self.root = root
        return xmlString
         

    def build_xml(self):
        root = self.root

        checkoutflowsupport = ET.SubElement(root, "checkout-flow-support")
        merchantcheckoutflowsupport = ET.SubElement(checkoutflowsupport, "merchant-checkout-flow-support")
        shippingmethods = ET.SubElement(merchantcheckoutflowsupport, "shipping-methods")
        flatrateshipping = ET.SubElement(shippingmethods, "flat-rate-shipping")
        flatrateshipping.set("name", "SuperShip Ground")
        
        price = ET.SubElement(flatrateshipping, "price")
        price.set("currency", "USD")
        price.text = "9.99" 

        indent(root)
        xmlString = ET.tostring(root)

        self.root = root
        return xmlString
        


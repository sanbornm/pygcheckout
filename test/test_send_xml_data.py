import unittest
from pygcheckout import pygcheckout

class Test(unittest.TestCase):
    """Unit tests for pygcheckout xml data sender"""

    def test_adding_multiple_carriers(self):
        c = pygcheckout.Cart()
        item = {
                   'name' : 'Gaszol Synthetic Oil Additive',
                   'description' : 'Simple Item',
                   'price' : '159.99',
                   'quantity' : '1',
                   'weight' : '5',
               }
        c.add_item(item)

        carrier = {
                      'price' : '10.00',
                      'carrier' : 'FedEx',
                      'pickupType' : 'REGULAR_PICKUP',
                      'service' : 'Home Delivery',
                  }
        c.add_carrier_shipping(carrier)

        carrier = {
                      'price' : '10.00',
                      'carrier' : 'FedEx',
                      'pickupType' : 'REGULAR_PICKUP',
                      'service' : 'Express Saver',
                  }
        c.add_carrier_shipping(carrier)

        carrier = {
                      'price' : '10.00',
                      'carrier' : 'FedEx',
                      'pickupType' : 'REGULAR_PICKUP',
                      'service' : '2Day',
                  }
        c.add_carrier_shipping(carrier)

        carrier = {
                      'price' : '10.00',
                      'carrier' : 'USPS',
                      'pickupType' : 'REGULAR_PICKUP',
                      'service' : 'Priority Mail',
                  }
        c.add_carrier_shipping(carrier)

        package = {
                      'height' : '7',
                      'length' : '7',
                      'width' : '7',
                  }
        c.add_package(package)
        print c.create_link()

    def test_add_carrier_shipping(self):
        """Test to see if we can build carrier shipping"""
        c = pygcheckout.Cart()
        item = {
                   'name' : 'Gaszol Synthetic Oil Additive',
                   'description' : 'Simple Item',
                   'price' : '159.99',
                   'quantity' : '1',
                   'weight' : '5',
               }
        c.add_item(item)
        carrier = {
                      'price' : '10.00',
                      'carrier' : 'FedEx',
                      'pickupType' : 'REGULAR_PICKUP',
                      'service' : 'Priority Overnight',
                  }
        c.add_carrier_shipping(carrier)
        package = {
                      'height' : '7',
                      'length' : '7',
                      'width' : '7',
                  }
        c.add_package(package)
        link = c.create_link()
        self.assertNotEqual('', link)
       

    def test_build_xml(self):
        """Test to see build_xml returns xml"""
        c = pygcheckout.Cart()
        item = {
                   'name' : 'Gaszol Synthetic Oil Additive',
                   'description' : 'Simple Item',
                   'price' : '159.99',
                   'quantity' : '1',
               }
        c.add_item(item)
        c.add_item(item)
        c.add_item(item)
        c.build_xml()

    def test_get_google_url_returns_urls(self):
        """Make sure google url returns"""
        c = pygcheckout.Cart()
        url = c.get_google_url()
        self.assertNotEqual(url, '')

    def test_get_config_default_retuns_keys(self):
        """Test that we get results back from config file"""
        testId = pygcheckout.get_config_default('testId')
        self.assertNotEqual('', testId)

    def test_response_exists_for_sandbox(self):
        """Test that we get a response from ups xml server"""

        xml = """<?xml version="1.0" encoding="UTF-8"?>
              <checkout-shopping-cart xmlns="http://checkout.google.com/schema/2">
                <shopping-cart>
                  <items>
                    <item>
                      <item-name>HelloWorld 2GB MP3 Player</item-name>
                      <item-description>HelloWorld, the simple MP3 player</item-description>
                      <unit-price currency="USD">159.99</unit-price>
                      <quantity>1</quantity>
                    </item>
                  </items>
                </shopping-cart>
                <checkout-flow-support>
                  <merchant-checkout-flow-support>
                    <shipping-methods>
                      <flat-rate-shipping name="SuperShip Ground">
                        <price currency="USD">9.99</price>
                      </flat-rate-shipping>
                    </shipping-methods>
                  </merchant-checkout-flow-support>
                </checkout-flow-support>
              </checkout-shopping-cart>"""

        response = pygcheckout.send_xml_data('https://sandbox.google.com/checkout/api/checkout/v2/merchantCheckout/Merchant/258193370883239',xml)
        self.assertNotEqual(response,'')

    def test_no_response_for_random_url(self):
        """Test to see that the script gracefully exists if no url is present"""
        
        response = pygcheckout.send_xml_data('http://asdf2991911888.com','adsf')
        self.assertEqual(response,'The url: http://asdf2991911888.com is not responding.')


if __name__ == "__main__":
    unittest.main()


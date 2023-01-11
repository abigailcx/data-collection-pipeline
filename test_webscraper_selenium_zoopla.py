from webscraper_selenium_zoopla import Scraper
import unittest

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.s = Scraper('config.yaml')
        self.s.scrape()

    def test_config_file_is_yaml(self):
        self.assertRegex(self.s.config_file, r'.yaml$')

    def test_prop_dict(self):
        self.assertIsInstance(self.s.prop_dict, dict)

    def test_prop_url_list(self):
        self.assertIsInstance(self.s.prop_url_list, list)

    def test_correct_num_elems_in_dict(self):
        num_data_points_in_prop_dict = sum(len(v) for v in self.s.prop_dict.values())
        num_expected_data_points = self.s.get_config()['page_size'] * 5
        self.assertEqual(num_data_points_in_prop_dict, num_expected_data_points )
    
    def test_price_is_num(self):
        for key in self.s.prop_dict:
            prop_price = self.s.prop_dict[key]["price"]
            #breakpoint()
            self.assertRegex(prop_price, r'^£\d+,\d+,?(\d+)?$')

    def tearDown(self):
        self.s.driver.quit()

#check url is valid
#check data types 
#check extension of img: if .jpg, test is passed
#check i
#check price is a number
#check prop_dict has 5 elems
#
#

if __name__ == '__main__':
    unittest.main()
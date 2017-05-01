'''
Created on Mar 12, 2017

@author: mjschaub
'''

import unittest,requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


'''
The api testing class
'''
class Test(unittest.TestCase):

    '''
    sets up the parameters
    '''
    def setUp(self):

        self.baseURL = 'http://localhost:5000'
        

    '''
    tests the endpoints for the portfolio website
    '''
    def test_gets(self):
        
        r = requests.get(self.baseURL+'/')
        self.assertEqual(r.status_code,200)
        r2 = requests.get(self.baseURL+'/projects')
        self.assertEqual(r2.status_code,200)
        r2 = requests.get(self.baseURL+'/projects/12')
        self.assertEqual(r2.status_code,200)
        r2 = requests.get(self.baseURL+'/projects/984028')
        self.assertEqual(r2.status_code,500)
        


if __name__ == "__main__":
    
    
    
    unittest.main()
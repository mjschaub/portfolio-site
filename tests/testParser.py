'''
Created on Mar 12, 2017

@author: mjschaub
'''
import unittest
import parser.xml_parser as parse


class Test(unittest.TestCase):

    '''
    tests that parsing the log returns a list of entries and each entry has the correct information
    '''
    def testParseLog(self):
        entries = parse.parse_log('test_log.xml')
        self.assertEqual(len(entries),1)
        self.assertEqual(entries[0][0]['revision'],u'6401')
        self.assertEqual(entries[0][1],u'mjschau2')
        self.assertEqual(entries[0][2],u'2017-03-06T16:59:20.880790Z')
        self.assertEqual(entries[0][3],['/mjschau2/Assignment2.1', '/mjschau2/Assignment2.1/Actor.py', '/mjschau2/Assignment2.1/CreateGraph.py', '/mjschau2/Assignment2.1/Graph.py', '/mjschau2/Assignment2.1/GraphVis.py', '/mjschau2/Assignment2.1/Graph_API.py', '/mjschau2/Assignment2.1/Movie.py', '/mjschau2/Assignment2.1/Test_Api.py', '/mjschau2/Assignment2.1/Test_Graph.py', '/mjschau2/Assignment2.1/Testing Plan Assignment #2.docx', '/mjschau2/Assignment2.1/graph_data.json', '/mjschau2/Assignment2.1/graph_setup.log', '/mjschau2/Assignment2.1/graphics.py'])
        self.assertEqual(entries[0][4],[{'action': 'A', 'kind': 'dir'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}, {'action': 'A', 'kind': 'file'}])
        self.assertEqual(entries[0][5],u'importing assignment 2.1')
        
      
        pass  
    '''
    tests that you can get the size of a file from the list xml (that's all I get from the list)
    '''
    def testParseList(self):
        entry = parse.parse_log('test_log.xml')
        curr_path = entry[0][3][0]
        size1 = parse.parse_list('test_list.xml',curr_path.replace('/mjschau2/',''))
        self.assertEqual(size1, 0)
        curr_path = entry[0][3][1]
        size1 = parse.parse_list('test_list.xml',curr_path.replace('/mjschau2/',''))
        self.assertEqual(size1, u'1623')
        
        pass

if __name__ == "__main__":
    
    unittest.main()
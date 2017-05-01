'''
Created on Mar 7, 2017

@author: mjschaub
'''

class log_entry(object):
    '''
    log_entry class for each commit
    '''

    def __init__(self,revision = 0, author='',date='',msg='',files = []):
        '''
        Constructor
        '''
        self.author = author
        self.date = date
        self.revision = revision
        self.msg = msg
        self.files = files
    '''
    sets the size of the file or directory
    @param path: path of the file to change
    @param size: the size of the file
    '''
    def set_size(self,path_idx,size):
        self.size[path_idx] = size
        
    
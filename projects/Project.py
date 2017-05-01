'''
Created on Mar 8, 2017

@author: mjschaub
'''

class Project(object):
    '''
    the project object
    '''


    def __init__(self,path='',size=0, action='',kind='', text='',file_id=0):
        '''
        Constructor to initialize a project
        '''
        self.path = path
        self.size = size
        self.action = action
        self.kind = kind
        self.text=text
        self.file_id = file_id
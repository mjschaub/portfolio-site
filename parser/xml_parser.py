'''
Created on Mar 6, 2017

@author: mjschaub
'''
import xml.etree.ElementTree as ET
import projects.log_entry as le
import projects.Project as proj
import json
from pymongo import MongoClient
client = MongoClient()


'''
Parse's the log to retrieve each commit and all the required data from it.
@param file: the log file to input
@return: the array of log entries
'''
def parse_log(file):
    e = ET.parse(file).getroot()
    log_entries = []
    #print(e.items())
    for logentry in e.iter('logentry'):
        curr_entry = []
        curr_entry.append(logentry.attrib)
        print(logentry.attrib)
        for auth in logentry.iter('author'):
            print(auth.text)
            curr_entry.append(auth.text)
        for date in logentry.iter('date'):
            print(date.text)
            curr_entry.append(date.text)
        paths = []
        for path in logentry.iter('path'):
            print(path.text)
            paths.append(path.text)
        curr_entry.append(paths)
        path_attribs =[]
        for path in logentry.iter('path'):
            print(path.attrib)
            path_attribs.append(path.attrib)
        curr_entry.append(path_attribs)
        for msg in logentry.iter('msg'):
            print(msg.text)
            curr_entry.append(msg.text)
        log_entries.append(curr_entry)
    return log_entries
'''
parse's the list xml file but for my implementation I only fetched the size of each file from the list as the log had all the other information
@param file: the list file
@param path_name: the path of the file to get the size of
@return: the size of the file
''' 
def parse_list(file, path_name):
    
    e = ET.parse(file).getroot()
    ret_size = 0
    for entry in e.iter('entry'):
        name = ''
        for i in entry.iter('name'):
            name = i.text
        if name == path_name:
            for i in entry.iter('size'):
                ret_size = i.text

    return ret_size


if __name__ == '__main__':
    
    list_file = 'svn_list.xml'
    log_file = 'svn_log.xml'
    
    entries = parse_log(log_file)
    
    db = client['portfolio']
    files = db['files']
    logs = db['logs']
    entry_objs = []
    curr_id = 0
    print(db['files'].count())
    print(db['logs'].count())
    db['files'].remove({})
    db['logs'].remove({})
    print(db['files'].count())
    for i in range(len(entries)):
        x = entries[i]
        kinds = [my_dict['kind'] for my_dict in x[4]]
        actions = [my_dict['action'] for my_dict in x[4]]
        projects = []
        for i in range(len(x[3])):
            curr_path = x[3][i]
            size_to_add = 0
            if kinds[i] == 'file':
                size_to_add = parse_list(list_file,curr_path.replace('/mjschau2/',''))
            svn_link = str('https://subversion.ews.illinois.edu/svn/sp17-cs242'+curr_path+'/?p='+x[0]['revision'])
            temp_proj = proj.Project(curr_path,size_to_add,actions[i],kinds[i], text=svn_link,file_id=curr_id)
            result = files.insert_one(temp_proj.__dict__)
            #print(result)
            curr_id+=1
            projects.append(temp_proj.__dict__)
        temp_obj = le.log_entry(int(x[0]['revision']),x[1],x[2],x[5],projects)
        entry_objs.append(temp_obj.__dict__)
    
    project_data = entry_objs
    
    
    #now put up on mongodb database
    
    result = logs.insert_many(project_data)
    print(result.inserted_ids)
    
    
    
    
    

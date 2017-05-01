'''
Created on Mar 7, 2017

@author: mjschaub
'''


from flask import Flask,render_template, abort, request
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
app = Flask(__name__)


'''
routes to the homepage
@return the render html template for the index page
'''
@app.route('/')
def home_page():
    return render_template('index.html')
'''
routes the project view page where you see all of the commits made
@return the html template for the page
'''
@app.route('/projects')
def assignment_page():
    return render_template('log_view.html',portfolio=portfolio)
'''
routes the invidual commit page for the certain revision number
@return the html template for this page
'''
@app.route('/projects/<revision_num>')
def project_page(revision_num=0):
    logs = db['logs'].find()
    for i in logs:
        if int(i['revision']) == int(revision_num):
            files = i['files']
    return render_template('revision_view.html',files=files,revision_num=revision_num)

'''
 routes the app for the individual file page where you do the commenting
 @param the route of the site
 @return the html template to use
 '''   
@app.route('/projects/<revision_num>/<file_id>', methods=['POST','GET'])
def file_page(file_id=0,revision_num=0):
    
    db = client['portfolio']
    comments = db['comments']
    
    if request.method == 'POST':
        
        user =  request.form['username']
        comment = request.form['comment']
        
        comment = cleanup_comment(comment)
        print({'status':'OK','user':user,'comment':comment})
        if request.form['type-of-comment'] == "normalComment":
            #add comment
            result = comments.insert_one({'user':user,'comment':comment,'file_id':file_id,'reply_id':-1,'replies':[]})
            print(result)
        else:
            #reply comment
            reply_id = request.form['type-of-comment']
            print('reply id: ',reply_id)
            result = comments.insert_one({'user':user,'comment':comment,'file_id':file_id,'reply_id':reply_id,'replies':[]})
            new_comment = comments.find({'user':user,'comment':comment})
            reply_comment = comments.find({'_id': ObjectId(reply_id)})
        
            for i in reply_comment:
                comments.update({'_id' : ObjectId(reply_id)}, { '$push': {'replies' : new_comment[0]}})
            

    file_given = None
    path = None
    files = db['files'].find()
    for i in files:
        if int(i['file_id']) == int(file_id):
            path = i['path']
            file_given = i['text']
                
    if file_given == None:
        return abort(500)
    
    comments = comments.find()
    page_comments = []
    for i in comments:
        if i['file_id'] == file_id:
            page_comments.append(i)
            print(i)

    return render_template('project.html',path=path,file=file_given,file_id=file_id,page_comments=page_comments,revision_num=revision_num)

'''
method to check each comment does not contain the filtered text and if it does then relace it with the good words
@param comment_text: the comment to filter
@return the new comment
'''
def cleanup_comment(comment_text):
    db = client['portfolio']
    word_filter = db['filter'].find()
    
    for i in word_filter:
        for j in range(len(i['bad_words'])):
            print(i['bad_words'][j])
            if i['bad_words'][j] in comment_text:
                print("old text: ",comment_text)
                comment_text = comment_text.replace(i['bad_words'][j],i['good_words'][j])
                print("new_text: ",comment_text)
            
    return comment_text

'''
sets up the database to have the filtered words in it, is run once to create the data
'''
def setup_bad_words():
    bad_words = ['moist','patriots','ugly','justin bieber','bing']
    good_words = ['wet','worst team ever', 'beautiful','he who shall not be named','google']
    db = client['portfolio']
    word_filter = db['filter']
    
    word_filter.insert_one({'bad_words':bad_words,'good_words':good_words })
    check_filter = db['filter'].find()
    for i in check_filter:
        print(i)
    

if __name__ == "__main__":
    
    db = client['portfolio']
    portfolio = db['logs'].find()
    files = db['files'].find()
    comments = db['comments'].find()
    #setup_bad_words()
    
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'mongodb'
    
    app.run()
##Author: M Durga Keerthi from IITH


import os
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

import MySQLdb
db = MySQLdb.connect("localhost","root","root","mydb" )  #username for database, password, databasename
cursor = db.cursor()

app = Flask(__name__)
app.secret_key = 'secret'

#################  login     ##############

user = ""
userpic_count = 0

@app.route('/')            #starting page
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])       #on submission of login details
def login():
   global user
   global userpic_count
   user = request.form['Username']
   passwd = request.form['Password']
  
   sql = "SELECT * FROM user \
       WHERE username = '%s'" % (user)       #checking if user is already there in database
   try:
      cursor.execute(sql)
      results = cursor.fetchall()
      if results == ():
         sql = "INSERT INTO user(username, password, pic_count, del_count) \
                     VALUES ('%s', '%s', '%d', %d)" % \
                     (user, passwd, 0, 0)       #registering the visitor
         try:
               cursor.execute(sql)
               db.commit()
         except:
               db.rollback()
      elif results[0][2]  != passwd:  
         return render_template('alert_login.html')      #if wrong password
      else:
         userpic_count = results[0][3]          #allowing user to sign in
   except:
      print "Error: unable to fetch data"      
   return render_template('actions.html')
    
##############-----uploading file-----------###################
    
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST','GET'])      #upload file webpage
def upload():
    if request.method == 'GET':
       return render_template('actions.html')       #get request
    else :  
       file = request.files['file']                #on submission of file to be uploaded
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)  #checking if the file is valid
           filen = user + '-' + str(userpic_count) + filename[-4:]  #rename file
           sql = "INSERT INTO picnames(picturename, uploader) \
                     VALUES ('%s', '%s')" % \
                     (filen, user)    #inserting the filename and user to database
           try:
               cursor.execute(sql)
               db.commit()
           except:
               db.rollback()
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filen))  #saving the file to uploads folder
           sql = "UPDATE user SET pic_count = pic_count + 1 WHERE username = '%s'" % (user)
           try:
                  cursor.execute(sql)
                  db.commit()
           except:
                  db.rollback()

           return render_template('alert_actions.html')  #on success
       else:
           return render_template('error.html')
        
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
   
###############------------Displaying all uploaded files --------###################
    
@app.route('/uploadedpics/')    
def uploadedpic():
   htmlfile = open('templates/uploadedpic.html',"w")
   copyfile = open('templates/copy_uploadedpic.html',"r")  #getting basic layout
   for line in copyfile:
      htmlfile.write(line)
   copyfile.close()
   
   sql = "SELECT * FROM user"
   try:
      cursor.execute(sql)
      results = cursor.fetchall()
      print results
      if results == ():          #if no registered user
          htmlfile.write('NO Uploaded pictures!!!')
      else:
         path= "/home/harrypotter/cookpad/uploads/"
         for root, dirs, files in os.walk(path):   
             for file in files:                                #getting all the files in the directory
                 sql = "SELECT * FROM picnames \
                        WHERE picturename = '%s'" % (file)     #getting name of user who uploaded it
                 try:
                  cursor.execute(sql)
                  uploadername = cursor.fetchall() 
                  htmlfile.write(uploadername[0][1])
                  htmlfile.write(' uploaded this picture<br>')
                 except:
                  print "Error: unable to fetch uploader"     #writing html
                 htmlfile.write('\n<img src="../uploads/')
                 htmlfile.write(file)
                 htmlfile.write('" align="center" style="width:100%;height:80%;">\n<br><br>\n <form action = "comment" method = "POST"> \n <input type = "hidden" name = "comntpic" value="')
                 htmlfile.write(file)
                 htmlfile.write('"/> \n<input type = "text" name = "comnt"/><br> \n <input type = "submit" value="comment" />\n </form>\n')
                 sql = "SELECT * FROM comments \
                        WHERE commentedpic = '%s'" % (file)   #getting the comments on pic
                 try:
                  cursor.execute(sql)
                  all_comments = cursor.fetchall()
                  print all_comments
                  if all_comments != ():
                     htmlfile.write('<p><u>previous comments:</u></p>')  #displaying the comments
                     for row in all_comments:
                        htmlfile.write('--> commented by ')
                        htmlfile.write(row[2])
                        htmlfile.write(' as: ')
                        htmlfile.write(row[1])
                        htmlfile.write('<br>')
                  htmlfile.write('<hr>')         
                 except:
                  print "Error: unable to fetch comments"
                   
   except:
      print "Error: unable to fetch data" 
   htmlfile.write('</div></body></html>')   
   htmlfile.close()   
   return  render_template('uploadedpic.html')


###############--------------inserting comments to database------##########
@app.route('/uploadedpics/comment', methods=['POST'])
def comment():
   commented = request.form['comnt']           #getting the commented text from form submitted by user
   picname = request.form['comntpic']
   print commented
   sql = "INSERT INTO comments(commentedpic,commentedtext,commenteduser) \
                     VALUES ('%s', '%s','%s')" % \
                     (picname,commented,user)
   try:
     cursor.execute(sql)
     db.commit()
   except:
     db.rollback()
     print "Error: unable to insert data"      
   return uploadedpic()

###########----------Displaying the pics uploaded by the user------#########
@app.route('/showpics/')
def showpic():
   htmlfile = open('templates/showpic.html',"w")
   copyfile = open('templates/copy_showpic.html',"r")               #getting basic layout
   for line in copyfile:
      htmlfile.write(line)
   copyfile.close()
      
   sql = "SELECT * FROM picnames \
                        WHERE uploader = '%s'" % (user)     #getting the images uploaded by user
   try:
      cursor.execute(sql)
      files = cursor.fetchall()
      print files
      if files != ():     
         for row in files:
            htmlfile.write('<input type="checkbox" name="dpic" value="')   #writing html
            htmlfile.write(row[0])
            htmlfile.write('"><img src="../uploads/')
            htmlfile.write(row[0])
            htmlfile.write('" style="width:80%;height:80%;"><hr>\n')                
         htmlfile.write('<input type="submit" value="Delete">\n</form>\n')
      else:  
         htmlfile.write('You have not uploaded pictures please upload them')  
   except:
      print "Error: unable to fetch data" 
   htmlfile.write('</body>\n</html>')   
   htmlfile.close()   
   return  render_template('showpic.html')               #displaying the html


##########---------------Deletes the selected image-----------##########
@app.route('/showpics/deletepic', methods=['POST'])
def delete():
   dfile = request.form['dpic']
   dpath = "uploads/" + dfile
   os.remove(dpath)                             #deleting file
   sql = "DELETE FROM picnames WHERE picturename = '%s'" % (dfile)
   try:
      cursor.execute(sql)
      db.commit()
   except:
      db.rollback() 
   sql = "UPDATE user SET del_count = del_count + 1 WHERE username = '%s'" % (user)   #count of deleted files
   try:
      cursor.execute(sql)
      db.commit()
   except:
      db.rollback() 
      
   return render_template('alert_actions.html')
                            
#################----------------Starts the app--------------##########                                     
if __name__ == '__main__':
     app.run(debug = True)                   #running the app             
                               

from flask import Flask, render_template, request, redirect, session, url_for, abort, jsonify, flash, send_file
from functools import wraps
from werkzeug.utils import secure_filename
from slugify import slugify
import pymongo
import os
import datetime
from bson import ObjectId

app = Flask(__name__)
app.secret_key = b'\xf26\x84\xf1\x1b\xf9\x13\x8c\xa5\x08=\xd8%\xa4\x87\xe7'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.csv']
app.config['UPLOAD_FOLDER'] = 'E:\\ECE\\MyBox\\uploads'

# Database
db = (pymongo.MongoClient('localhost', 27017)).MyBox

# decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

# routes
from user import routes

@app.route('/')
@app.route('/', methods=['POST'])
def login_page():
    return render_template('index.html')

@app.route('/user')
@login_required
def user():
    if 'redirectToUrl' in session:
        url=session['redirectToUrl']
        session.pop('redirectToUrl')
        return redirect(url)
    uploaded_files=db.files.find({
        "User_Id": session['user']['_id'],
        "isactive": True
    }).sort([("uploaded_date", pymongo.DESCENDING)])
    return render_template('UI.html', uploaded_files=uploaded_files)

@app.route('/user/handle_file_upload', methods=['POST'])
@login_required
def upload_files():
    Files = request.files.getlist('uploadedfile')
    for file in Files:
        # if no file chosen
        if file.filename == "":
            flash("No file choosen to upload")
            return redirect('/user')

        # checking file in database
        if db.files.find_one({"filename": file.filename, "User_Id": session['user']['_id'], "isactive": True}):
            flash("File with this name filename already uploaded")
            return redirect('/user')

        name=secure_filename(file.filename)
        file_ext = os.path.splitext(file.filename)[1]
        Path=os.path.join(app.config['UPLOAD_FOLDER'], session['user']['username'])
        if os.path.exists(Path) is False:
            os.mkdir(Path)
        Path=os.path.join(app.config['UPLOAD_FOLDER'], session['user']['username'], name)
        file.save(Path)
        size=os.stat(Path).st_size

        #checking file type    
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            flash("Invalid file type :(")
            os.remove(Path)
            return redirect('/user')

        #checking file size
        if size>20*1024*1024:
            flash("File size limit excceded :(")
            os.remove(Path)
            return redirect('/user')

        x=size/(1024*1024)
        if size<1024:
            filesize=str(size)+" bytes"
        elif x>=1:
            filesize=str(int(x))+" MB"
        else:
            filesize=str(int(size/1024))+" KB"

        db.files.insert_one({
            "User_Id": session['user']['_id'],
            "filename": file.filename,
            "file_type": file_ext,
            "file_size": filesize,
            "file_path": Path, 
            "isactive": True,
            "uploaded_date": datetime.datetime.now().strftime("%c")
            })

    flash("Files successfully uploaded :)")
    return redirect('/user')

@app.route('/download/<fileid>/<filename>', methods=['GET'])
def showdownloadpage(fileid, filename):
    file_object = db.files.find_one({
        "_id": ObjectId(fileid),
        "isactive": True
    })
    if file_object is None:
        abort(404)
    if 'logged_in' not in session:
        session['redirectToUrl']= '/download/' + fileid + '/' + filename
        return redirect('/')
    return render_template('downloadpage.html', file=file_object)

@app.route('/user/<fileid>', methods=['GET'])
@login_required
def deletefile(fileid):
    db.files.update_one({"_id": ObjectId(fileid)},{"$set": {"isactive": False}})
    return redirect('/user')

@app.route('/download_file/<fileid>', methods=['GET'])
@login_required
def download(fileid):
    file_object = db.files.find_one({
        "_id": ObjectId(fileid),
        "isactive": True
    })
    if file_object is None:
        abort(404)
    
    db.file_downloads.insert_one({
        "UserId": session['user']['_id'],
        "FileId": file_object['_id'],
        "DownloadedAt": datetime.datetime.now().strftime("%c")
    })
    return send_file(file_object['file_path'], as_attachment=True)   

@app.route('/download/cancel')
@login_required
def canceldownload():
    return redirect('/user')
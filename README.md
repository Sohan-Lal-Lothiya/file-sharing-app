# file-sharing-app
## Full_stack development
### Requirements-
     1.python-flask web framework
     2.Mogo-DB as database
     3.Robo-3T to browse Mongo-DB
### Specifications-
     It's a webapp model for file sharing purpose.
     Users can keep their files here and download them or share with ohers using link.
     User have to register first to use it and they cannot perform any action without logging in.
     Maximum allowed size per file to upload is 20MB.
     Allowed file types are jpg, png, gif, doc, docx, xls, xlsx, ppt, pptx, pdf and csv.
     User can delete any of their file anytime.
### Work-flow-
     Set network port to 5000 first.
     Then install virtual environment inside your project folder and activate it.
        All the commands given here are for windows-  py -3 -m venv venv to create virtual environment named 'venv' and activate it using venv\Scripts\activate 
     Install flask using pip install Flask
     Install all dependencies in requirements.txt.
     Create a directory named 'uploads' inside root directory which stores all the files uploaded by users.
     Set FLASK_APP environment variable using set FLASK_APP=app.py
     Set FLASK_ENV environment variable to development to run it in debug mode 'on' using set FLASK_ENV=development
     Then run it using flask run
     you'll get all your files at http://127.0.0.1:5000/user after login.
     

from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from hashlib import sha256
from app import db
import uuid
import datetime
import os

class User:

    def start_session(self, user): 
        session['logged_in']=True
        session['user']=user
        db.users.update_one({"username": request.form.get('username1')},{"$set":{"last_login_date":datetime.datetime.now().strftime("%c") }})
        return jsonify(user)

    def signup(self):
        print(request.form)

        #creating a user
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "last_login_date": datetime.datetime.now().strftime("%c"),
            "created_at": datetime.datetime.now().strftime("%c")
        }

        #checking username
        if db.users.find_one({ "username": user['username'] }):
            return jsonify({ "error": "Username already taken! choose different" }), 400

        #checking email
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email ID already registered" }), 400

        #checking password
        if user['password']!=request.form.get('confirm-password'):
            return jsonify({ "error": "Password didn't match" }), 400

        #encrypting password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if db.users.insert_one(user):
            return self.start_session(user)
        return jsonify({ "error": "Sign Up Failed!" }), 400

    def logout(self):
        session.clear()
        return redirect('/')

    def login(self):
        user = db.users.find_one({
            "username": request.form.get('username1')
        })

        if user :
            if pbkdf2_sha256.verify(request.form.get('password1'), user['password']):
                return self.start_session(user)
            return jsonify({ "error": "Incorrect password!" }), 401
        return jsonify({ "error": "You'are not a registered user" }), 401

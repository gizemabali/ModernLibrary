
def encyrpted(pw):
  import hashlib
  return hashlib.md5(pw).hexdigest()
  
def signup():
   # db.user.truncate()
   # global left_sidebar_enabled
   # left_sidebar_enabled = False
   
   import time
   form = FORM(
     'Username', INPUT(_name='username', requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db,db.user.username)]), BR(),
     'Password', INPUT(_name='pw1', _type='password', label='Password', requires=IS_NOT_EMPTY()), BR(),
     'Password2', INPUT(_name='pw2', _type='password', label='Confirm password',
            requires=[IS_EQUAL_TO(request.vars.pw1, "don't match"),IS_NOT_EMPTY()]), BR(),
     'Email', INPUT(_name='email', requires=[IS_EMAIL(), IS_NOT_IN_DB(db, db.user.email)]), BR(),
     INPUT(_type='submit'),
     _id="loginform", _class="bootstrapform"
   )
   if form.process().accepted:
     db.user.insert(username=form.vars.username, 
                    password=encyrpted(form.vars.pw1),
                    email = form.vars.email,
                    login_time = int(time.time()),
                    role = "rookie"
                    )
     response.flash = "Your account is saved.Please sing in now "
     #TODO: return user to the new account page               
     
   return dict(page_title="",form = form)

   
def signin():
   import time
   global userid
   username = request.vars.username
   pw = encyrpted(request.vars.pw)
   rows = db( (db.user.username == username) & (db.user.password==pw)).select()   
   if len(rows) == 0:
     response.flash = "Wrong username or password"
     return redirect(request.env.http_referer)
   else:
     db(db.user.id == rows[0].id).update(login_time=int(time.time()))
     rows[0].login_time = int(time.time())
     session.user = rows[0]
     return redirect(request.env.http_referer)
   return dict(page_title="Error")
   
def logout():
    global user
    user = None
    session.user = None
    return redirect(request.env.http_referer)
    
    

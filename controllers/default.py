# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def capitalize(title):
   words = title.split()
   words = [word.capitalize() for word in words]
   return " ".join(words)


def report():

    return dict(page_title="Report")	

def edit_comment():
    global user
    form = FORM("Your comment", BR(), 
              TEXTAREA(_name='comment', _cols= 40, _rows=5, requires=IS_NOT_EMPTY()),
              INPUT(_type='submit', _value="SEND COMMENT"))
    form_id = request.args(1)
    form_update = None
    category = request.args(0)
    image_id = request.args(2)
    account_id = request.vars['q']
    rows = db(db.post.id == form_id).select()
    if (user and user.id == account_id):
       #account = user
       account = db.user(account_id)
       
    else:   
       account = db.user(account_id)
    if form.process().accepted:
         rows = db(db.post.id == form_id).select().first()
         rows.update_record(body = form.vars.comment)
         redirect(URL(category, args=[image_id]))
    return dict(page_title="Edit Comment", form=form, form_update=rows, account_id=account_id, account = account)         
def delete_comment():
    global user
    form = FORM("Delete The Comment", BR(), 
              
              INPUT(_type='submit', _value="DELETE COMMENT"))
    form_id = request.args(1)
    form_update = None
    category = request.args(0)
    image_id = request.args(2)
    account_id = request.vars['q']
    
    if (user and user.id == account_id):
       #account = user
       account = db.user(account_id)
       
    else:   
       account = db.user(account_id)
    if form.process().accepted:
         db(db.post.id == form_id).delete()
         redirect(URL("default", category, args=[image_id]))
    return dict(page_title="Delete Comment", form=form, account_id=account_id, account = account)    

def find_author(book):
    authors_data = db().select(db.authors.ALL, orderby=db.authors.name)
    for author in authors_data:
     if book["author"] == author["id"]:
       return author
    return None
    
def authors():
    authors_list = db().select(db.authors.ALL, orderby=db.authors.name)
    authors = dict()
    books = db().select(db.books.ALL, orderby=db.books.title)
    for book in books:
        author_obj = find_author(book)
        author_name = author_obj["name"]
        if author_name in authors:
          authors[author_name] = (authors[author_name][0]+1, author_obj['id'])
        else:   
          authors[author_name] = (1, author_obj['id'])
            
     
    return dict(page_title="Authors", authors_list = authors_list, books=books, authors=authors)
    
def find_author2(author_id):
    authors_data = db().select(db.authors.ALL, orderby=db.authors.name)
    
    for author in authors_data:
        if(author.id == author_id):
           name = author.name
    
    return name
    
def book():
    global user
    book = db.books(request.args(0,cast=int)) or redirect(URL('index'))
    image_id = request.args(0,cast=int)
    db.books.id.default = book.id
    db.post.image_id.default = book.id
    category_field = request.function
    
    if user != None:
        form = FORM("Your comment", BR(), 
              TEXTAREA(_name='comment', _cols= 40, _rows=5, requires=IS_NOT_EMPTY()),
              INPUT(_type='submit', _value="SEND COMMENT"))
        if form.process().accepted:
          db.post.insert(image_id=image_id, 
                         author=user.id,
                         field=category_field,
                         body = form.vars.comment
                        )
          response.flash = 'your comment is posted. Click to exit'
    else: 
        form = None 
    comments = db( (db.post.image_id==book.id) & (db.post.field==category_field) &
                   (db.post.author == db.user.id)).select()
    book_info = db(db.books.id == book.id).select()
    author = find_author2(book.author)
    return dict(page_title=book.title + (" (%dTL)" % book.price), book_info=book_info, book=book, form=form, comments=comments, author=author)

def bestsellers():
    global user
    top100 = db.top_100(request.args(0,cast=int)) or redirect(URL('index'))
    image_id = request.args(0,cast=int)
    db.top_100.id.default = top100.id
    db.post.image_id.default = top100.id
    category_field = request.function
    
    if user != None:
        form = FORM("Your comment", BR(), 
              TEXTAREA(_name='comment', _cols= 40, _rows=5, requires=IS_NOT_EMPTY()),
              INPUT(_type='submit', _value="SEND COMMENT"))
        if form.process().accepted:
          db.post.insert(image_id=image_id, 
                         author=user.id,
                         field=category_field,
                         body = form.vars.comment
                        )
          response.flash = 'your comment is posted. Click to exit'
    else: 
        form = None 
    comments = db( (db.post.image_id==top100.id) & (db.post.field==category_field) &
                   (db.post.author == db.user.id)).select()
    title = name_changer2(top100.title)
    return dict(page_title=top100.title, top100=top100, title=title, comments=comments, form=form)
def test():
    advanced_search = SQLFORM(db.advanced_search)
    if advanced_search.process().accepted:
        return dict(form=BEAUTIFY(advanced_search.vars["author"]))    
    return dict(form=advanced_search)   
def science_fiction():   
    book_data = db().select(db.books.ALL, orderby=db.books.title)
    books = db(db.books.category == "Science Fiction").select()

    return dict(page_title="Sci-Fic", books=books) 
def classics():  
    book_data = db().select(db.books.ALL, orderby=db.books.title)
    books = db(db.books.category == "Classic").select()

    return dict(page_title="Classics", books=books) 

def shakespeare_quotes():
    quotes = db(db.quotes.author == "Shakespeare").select()
    return dict(page_title="Shakespeare's Quotes", quotes=quotes)
def bestseller_quotes():
    quotes = db().select(db.quotes.ALL)
    return dict(page_title="Shakespeare's Quotes", quotes=quotes)
def TLOTR_quotes():
    quotes = db(db.quotes.book == "The Lord of the Rings").select()
    return dict(page_title="Shakespeare's Quotes", quotes=quotes)

def shakespeare_bests():
    best_books = db(db.books.author_name == "Shakespeare").select()
    return dict(page_title="Shakespeare's Bests", best_books=best_books)
def erase_last_whitespace(name):
    if (len(name)):
      while(name[-1]==" "):
         name = name[:-1] + name[-1].replace(" ", "")
    else:
         name = None    
    return name
def splitting(name):
    name = name.lower()
    words = name.split(" ")
    name_changer = [word.capitalize() for word in words]
    whole_name = ""
    for i in name_changer:
        
	    if(i!=""):
	       whole_name = whole_name + i + " "
    if whole_name != "": 
        whole_name = erase_last_whitespace(whole_name)
    return whole_name
    
def index():
    advanced_search = SQLFORM(db.advanced_search)
    databases = []
    if advanced_search.process(dbio=False).accepted:
        
        part_string = splitting(advanced_search.vars["author"])
        last_price = advanced_search.vars["price"]
        last_book = splitting(advanced_search.vars["book"])
        last_publisher = splitting(advanced_search.vars["publisher"])
        last_year = advanced_search.vars["year"]
        last_category = splitting(advanced_search.vars["category"])
        last_book_info = db(db.books.title==last_book).select()
      
        if part_string != "":
            databases.append(db.books.author_name == part_string )
        if last_price != "":
            databases.append(db.books.price == last_price)
        if last_book != "":
            databases.append(db.books.title == last_book )
        if last_publisher != "":
            databases.append(db.books.publisher == last_publisher)
        if last_year != "":
            databases.append(db.books.year == last_year )
        if last_category != "":
            databases.append(db.books.category == last_category)
        query = reduce(lambda a,b:(a&b),databases)
        database_function_info = db(query).select()
    else:
        database_function_info = []
        
    return dict(page_title="Modern Library", advanced_search=advanced_search, database_function_info=database_function_info
                )


def encyrpted(pw):
  import hashlib
  return hashlib.md5(pw).hexdigest()
def account():
    account_id = request.args(0,cast=int)
    age = ""
    users = db().select(db.authors.ALL)
    admin = db(db.user.role == "admin").select().first()
    admin_id = admin.id
       
    if (user and (user.id == account_id or user.id == admin_id)):
       #account = user
       account = db.user(account_id)
       form = FORM(
          
          'Password', INPUT(_name='pw1', _type='password', label='Password', requires=IS_NOT_EMPTY()), BR(),
          'Password2', INPUT(_name='pw2', _type='password', label='Confirm password',
           requires=[IS_NOT_EMPTY(),IS_EQUAL_TO(request.vars.pw1, "don't match")]), BR(),
          
          'Age', INPUT(_name='age', requires=IS_INT_IN_RANGE(0,100)), BR(),
          'City', INPUT(_name='city'), BR(),
          'Information', TEXTAREA(_name='info', _cols= 40, _rows=5),
           INPUT(_type='submit', _value="UPDATE ACCOUNT"),
           _id="loginform", _class="bootstrapform"
       )
       user_db = db(db.user.id == account_id).select()
       if form.process().accepted:
           for person in user_db:
               person.update_record(
                                    password = encyrpted(form.vars.pw1),
                                    password2 = encyrpted(form.vars.pw2),
                                    city = form.vars.city,
                                    age = form.vars.age,
                                    information = form.vars.info,
                                    )
           redirect(URL("account", args=[account_id]))
          
    else:   
       account = db.user(account_id)
       form = None
       if account == None:
           redirect(URL('index'))
    return dict(page_title="Account",account=account, form=form)
    
def comments():
    name = request.args(0)
    comments = db(db.post.author==name).select() or redirect(URL('index'))
    return dict(page_title="Comments",comments=comments, name=name)  

def name_changer2(title):
      name = title.lower().replace(" ", "_")
      return name
     

   
 
def author():
    authors_data = db().select(db.authors.ALL, orderby=db.authors.name)    
    book_data = db().select(db.books.ALL, orderby=db.books.title)
	
    k = int(request.args[1])
    author_obj = None
	
	
    for author in authors_data:
      if k == author["id"]:
         author_obj = author
         break
	
    books = []
	
    for book in book_data:
      if k == book["author"]:
         books.append(book)
    
    if author_obj == None:
       # raise HTTP(404, 'Page not found', test='hello') 
       redirect(URL("error_page", vars=dict(url=request.env.path_info)))    
    return dict(page_title=author_obj["name"], author=author_obj, books=books, id=k)
	
def book_list():
    book_data = db().select(db.books.ALL, orderby=db.books.title)
    books = []	
    for book in book_data:
       book['title'] = capitalize(book['title'])
       book["author_name"] = find_author(book)['name']
       books.append(book)
	
	
    return dict(page_title="All Books", books=books)
	
def top100():
    top100_list = db(db.books.category == "Top100").select()
    return dict(page_title="Top 100", top100_list=top100_list)

def popular_films():

    global user
    film = db.films(request.args(0,cast=int)) or redirect(URL('index'))
    image_id = request.args(0,cast=int)
    db.films.id.default = film.id
    db.post.image_id.default = film.id
    category_field = request.function
    
    if user != None:
        form = FORM("Your comment", BR(), 
              TEXTAREA(_name='comment', _cols= 40, _rows=5, requires=IS_NOT_EMPTY()),
              INPUT(_type='submit', _value="SEND COMMENT"))
        if form.process().accepted:
          db.post.insert(image_id=image_id, 
                         author=user.id,
                         field=category_field,
                         body = form.vars.comment
                        )
          response.flash = 'your comment is posted. Click to exit'
    else: 
        form = None 
    comments = db( (db.post.image_id==film.id) & (db.post.field==category_field) &
                   (db.post.author == db.user.id)).select()
    title = name_changer2(film.title)
    return dict(page_title=film.title, films =film , title=title, comments=comments, form=form)
def films():
    films_list = db().select(db.films.ALL, orderby=db.films.director)
    
    return dict(page_title="Films", films_list=films_list)
    
def appguide():
    app_list=db().select(db.appguides.ALL)
    return dict(page_title="AppGuide",app_list=app_list)
  
def apps():
    appguide = db.appguides(request.args(0))
    title = name_changer2(appguide.title)
    return dict(page_title=appguide.title, appguide =appguide , title=title)
    
"""def bestsellers():
    global top100_list
    k = int(request.args[1])
    
    bests = top100_list[k]
     
    return dict(bests=bests)"""
bests1 = "a" 

def tit(title):
    top100_list = db().select(db.top_100.ALL, orderby=db.top_100.author)
    for top in top100_list:
       if title == top['title']:
           return(top['title'].replace(" ", "_"))
    return None
    
    
def series():
    seri_list=db().select(db.series.ALL)
    return dict(page_title="Series",seri_list=seri_list)
  
def seri():
    series = db.series(request.args(0))
    seri_name = name_changer2(series.seri_name)
    return dict(page_title=series.seri_name, series =series , seri_name=seri_name)
 
def history():
    history = db().select(db.history.ALL)
    return dict(page_title="History of Muğla", history=history)
def lib():
    lib = db().select(db.lib.ALL)
    return dict(page_title="History of Library", lib=lib)   
def travelling():
    travelling=db().select(db.travellings.ALL)
    return dict(page_title="Travelling",travelling=travelling)
    
def about():
    return dict(page_title="About")


def error_page():
    return dict(page_title="Error")

def library():
    return dict(page_title="Error")
	

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)




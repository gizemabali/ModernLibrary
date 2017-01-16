db = DAL("sqlite://storage.sqlite")

db.define_table('authors',
                Field('id', 'integer'),
                Field('name', unique=True),
                Field('bio',length=1000000),
                Field('file', 'upload')
                )
db.define_table('books',
                Field('author', 'integer'),
                Field('author_name'),
                Field('title', unique=True),
                Field('category'),
                Field('price', 'integer'),
                Field('year', 'integer'),
                Field('publisher'),
                Field('amazon_link', length=1000),
                Field('betterworld_link', length=1000),
                Field('idefix_link', length=1000),
                Field('id', 'integer', 'compute'),
                Field('file', 'upload'),
                Field('info', type='string', length=1000000))


db.define_table('post',
                Field('id', 'integer'),
                Field('image_id', 'integer'),
                Field('field'),
                Field('author', 'integer'),
                Field('email'),
                Field('age'),
                Field('body', 'text'))




db.define_table('advanced_search',
                Field('author'),
                Field('book'),
                Field('category'),
                Field('year'),
                Field('price'),
                Field('publisher')
                )
db.define_table('quotes',
                Field('author'),
                Field('book'),
                Field('quotes', length=1000000),
                Field('character')
                )
db.define_table('films',
                Field('id', 'integer'),
                Field('director'),
                Field('title', unique=True),
                Field('scenario'),
                Field('book_id'),
                Field('year', 'integer'),
                Field('file', 'upload'),
                Field('info', length=1000000))

db.define_table('appguides',
                Field('id', 'integer'),
                Field('title',unique=True),
                Field('google_play_link', length=1000),
                Field('file', 'upload'))
db.define_table('history',
                Field('file', 'upload'),
                Field('history', length=1000000))
db.define_table('travellings',
                Field('travelling', length=1000000))
db.define_table('lib',
                Field('lib', length=1000000))    
db.define_table('series',
                Field('id', 'integer'),
                Field('author'),
                Field('author_info', length=1000000),
                Field('seri_name', length=1000000),
                Field('file', 'upload'),
                Field('info', length=1000000))  
db.define_table('user',
  Field('id'),
  Field('username', unique=True, required=True),
  Field('password', 'password', required=True),
  Field('role'),
  Field('email'),
  Field('age', 'integer'),
  Field('city'),
  Field('information', length="100000"),
  Field('login_time', 'integer') 
)
  
db.user.email.requires = IS_EMAIL()
#db.post.image_id.requires = IS_IN_DB(db, db.books.id, '%(title)s')
db.post.author.requires = IS_NOT_EMPTY()
db.post.email.requires = IS_EMAIL()
db.user.email.requires= IS_NOT_IN_DB(db, db.user.email)
db.post.body.requires = IS_NOT_EMPTY()

db.post.image_id.writable = db.post.image_id.readable = False

print("in db.py")
if session.user:
  user = session.user
else:
  user = None  
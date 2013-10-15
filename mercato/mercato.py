import os
import urllib
import cgi

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

HTML = """\
<html>
    <head> <link type="text/css" rel="stylesheet" href="stylesheets/main.css" /> </head>
    <style>
      h1{
        position:relative;
		top:50px;

    </style>

    <h1> MERCATO </h1>

    

    <br><br>

    <hr><hr>

   <!-- <form action="/add" method="post">
      Product Name: <div><input type="text" name="productname"></div>
      Product Description: <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Add Product"></div>
    </form> -->

    <form action="/sendData" method="post">
        <fieldset>
        <legend>Add a New Product</legend>
        <p><label for="name">Product Name</label> <input type="text" name="productname" id="name" /></p>
        <p><label for="description">Product Description</label> <textarea name="content" rows="3" cols="60" id="desc"></textarea><br /></p>
        <p><label for="price">Price</label> <input type = "text" name="productprice" id="price" /> </p>
        <p class="submit"><input type="submit" value="Add Product" /></p>
        </fieldset>
        </form> 

    
</html>

"""
WELCOME_HTML = """\
<!DOCTYPE html>

<html>
	<head> <link type="text/css" rel="stylesheet" href="stylesheets/main.css" /> </head>

   <h1> R  I  A  L  T  O </h1>
    <br>
    <marquee> Welcome to NITT's online flea market! </marquee>

    <hr><hr>

  <body>
  <div class = "leftlinks">
	<a href = "addProd.html"> Add a product </a> <br><br>
	<a href = "itemList.html"> View all items </a> <br><br>
	<a href = "myItems.html"> View my items </a> <br><br>
	<a href = "search.html"> Search </a> <br><br>
    <a href = ""> Logout </a>
  </div>

  <p class = "intro">
  hello hellohellohellohellohellohellohellohello hello hello hello hello hello hello hello hello hello hello hello hello 
hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello 
  </p>


    
  </body>
</html>

"""


class Product(ndb.Model):

    name = ndb.StringProperty()
    desc = ndb.StringProperty()
    price = ndb.FloatProperty()
    owner = ndb.UserProperty()
    

class LoginPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        

        if user:
            # self.response.headers['Content-Type'] = 'text/plain'
            # self.response.write('Hello, ' + user.nickname())
            self.redirect('/welcome')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Welcome(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            name = user.nickname()
        else:
            name = 'anonymous'

        url_logout = users.create_logout_url('/')
        url_addProd = '/add'
        url_itemList = '/list'
        url_myList = '/myList'
        template_values = {
            'name': name,
            'url_logout': url_logout,
            'url_addProd': url_addProd,
            'url_itemList': url_itemList,
            'url_myList': url_myList,
        }

        template = JINJA_ENVIRONMENT.get_template('welcome.html')
        self.response.write(template.render(template_values))


    def post(self):
        p = Product()
        p.name = self.request.get('searchterm')
        products = ndb.gql("SELECT * FROM Product where name = :1",p.name)
        template_values = {
            'products': products,
        }

        template = JINJA_ENVIRONMENT.get_template('allProd.html')
        self.response.write(template.render(template_values))
        



class AddProduct(webapp2.RequestHandler):

    def get(self):
        self.response.write(HTML)

    

class SendData(webapp2.RequestHandler):

    def post(self):
        p = Product()
        p.name = self.request.get('productname')
        p.desc = self.request.get('content')
        p.price = float(self.request.get('productprice'))
        p.owner = users.get_current_user()
        p.put()

        self.redirect('/welcome')
        


        '''
        q1 = ndb.gql("SELECT * FROM Product")
        self.response.out.write('<html><body>')
        for p1 in q1:
            self.response.out.write('<br>')
            self.response.out.write(cgi.escape(p1.desc))

        self.response.out.write('</body></html>')

        for p1 in q1:
            p1.key.delete()
        '''
class ItemList(webapp2.RequestHandler):

    def get(self):
        q1 = ndb.gql("SELECT * FROM Product")
        self.response.out.write('<html><body>')
        for p1 in q1:
            self.response.out.write('<br>')
            self.response.out.write('Name : ' + cgi.escape(p1.name) + '; Description : ' + cgi.escape(p1.desc))
            self.response.out.write('; Price : ' + str(p1.price))
            if p1.owner:
                self.response.out.write('; Owner : ' + p1.owner.nickname())

        self.response.out.write('</body></html>')

        for p1 in q1:
            p1.key.delete()
        
      
class ItemList1(webapp2.RequestHandler):

    def get(self):
        products = ndb.gql("SELECT * FROM Product")
        template_values = {
            'products': products,
        }

        template = JINJA_ENVIRONMENT.get_template('allProd.html')
        self.response.write(template.render(template_values))

class MyList(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        products = ndb.gql("SELECT * FROM Product WHERE owner = :1",user)
        template_values = {
            'products': products,
        }

        template = JINJA_ENVIRONMENT.get_template('allProd.html')
        self.response.write(template.render(template_values))


        

application = webapp2.WSGIApplication([
    ('/',LoginPage),
    ('/add',AddProduct),
    ('/sendData',SendData),
    ('/list',ItemList1),
    ('/myList',MyList),
    ('/welcome',Welcome),
    ('/search',Welcome),
], debug=True)



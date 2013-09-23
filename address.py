import web

db=web.database(dbn='postgres', db='contacts')
urls = (
	'/', 'Home',
	'/add', 'Add',
	'/list', 'List',
	'/search', 'Search',
	'/detail/(.+)', 'Detail',
	'/edit/(.+)', 'Edit'
)


class Parent():
	def __init__(self):
		self.render = web.template.render('templates/')
		self.request_data = web.input()
		self.header = self.render.header()
		self.footer = self.render.footer()


class Home(Parent):
	def GET(self):
		return self.render.addressbook(self.header, self.footer)

class List(Parent):
	def GET(self):
		entries = db.select('address', order="last_name")
		return self.render.list(self.header, entries, self.footer)

class Add(Parent):
	def POST(self):
		a = web.input()
		b = db.insert('address', first_name=a.first_name, last_name=a.last_name, email=a.email, phone=a.phone, city=a.city)
		raise web.seeother('/list')


class Search(Parent):
	def GET(self):
		a = web.input()
		if a:
			criteria = dict(name='%'+a.first_name+'%')
			results = db.select('address', vars=criteria, where="first_name LIKE initcap($name) OR last_name LIKE initcap($name)")
		else:
			results = dict() #had to do this or else first visit to page would itterate over nothing. 
		return self.render.search(self.header, results, self.footer)

class Detail(Parent):
	def GET(self, index):#index comes from url patter match (.+)
		criteria = dict(id=int(index))
		results = db.select('address', vars=criteria, where="id = $id")
		person = results
		print person		
		return self.render.details(self.header, person, self.footer)
		

	def POST(self, index):
		a = web.input()
		db.update('address', vars=dict(id=int(index)),  where="id=$id",  first_name=a.first_name, last_name=a.last_name, email=a.email, phone=a.phone, city=a.city)
		raise web.seeother('/list')
		

class Edit(Parent):
	def POST(self, index):
		
		criteria = dict(id=int(index))
		db.delete('address', vars=criteria, where='id=$id')
		raise web.seeother('/list')


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
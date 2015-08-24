try:
	import MySQLdb
	import pexpect
	import excep as ex
	import time
	import sys
except ImportError:
	raise ex.ModulesNotFound()

# Start the server from the terminal sudo /usr/local/mysql/support-files/mysql.server start
# Stop the server from the terminal sudo /usr/local/mysql/support-files/mysql.server stop
# Restart the server from the terminal sudo /usr/local/mysql/support-files/mysql.server restart


class Explorer(object):

	def __init__(self,root_username,root_password):
		#username and password to start the mysql server
		self.root_user = root_username
		self.root_pass = root_password
		#start the mysql server
		self.start_server()
		#create the connection
		#using a try inside a try
		#because for some reason if i use time.sleep after the start server it fails
		try:
			#connecting the to the database
			#since this is a db explorer and is not meant to manage dbs
			#it uses the localhost and the existing test db
			self.connection = MySQLdb.connect(host='',
											user = self.root_user,
											passwd = self.root_pass,
											db='test')
		except MySQLdb.Error:
			#if the connection fails the first time we try again
			#we need to because it starts the server really slow (atleast on my mac( new computer calling))
			try:
				#using time.sleep afterall, here it doesn't fail though..
				time.sleep(4)
				self.connection = MySQLdb.connect(host='',
												user = self.root_user,
												passwd = self.root_pass,
												db='test')
			except MySQLdb.Error:
				#if it raises another Error its probably 
				#because of the credentials or because 
				#the users computer is slower than mine (new computer calling v.2))
				raise ex.NoMYSQL()
		#CURSOR ASSEMBLE!
		self.cursor = self.connection.cursor()	


	def create_table(self,info_dict):
		''' info_dict - dict containing the table name and the names of the columns

		'''
		#using try except to catch the mysql errors that might be raised
		#currently all the raised error at this level are catched and TableExist error is raised
		try:
			#statement to get the number of tables currently in the db
			desc_statement = 'SHOW TABLES'
			self.cursor.execute(desc_statement)
			table_num = [x[0] for x in self.cursor.fetchall()]
			#check the number of tables in the database
			#currently the  max number is 5 to avoid displaying issues
			#Perhaps usa a var instead of hardcoding the number ?
			if len(table_num) < 5:
				#use a var to determain if its the last value and weather a comma should be added
				comma_var = 2
				#create the initial part of the statement using format because these arguments
				#cannot be added with the standard argument passing to the execute function
				#it's not safe but currently i dont know any other way
				statement_start = 'CREATE TABLE {table_name} ('.format(table_name = info_dict['table_name'])
				statement_end = ')'
				statement_mid = ''
				items = info_dict.items()
				#iterate over the the columns in the info dict
				for key,value in items:
					#we dont need the table name when constructing the mid statement
					if key != 'table_name':
						#prepare the default value if one is selected
						if value[0] == 'VARCHAR':
							if value[3] != '':
								value[3] = 'DEFAULT "{}"'.format(value[3])
						else:
							if value[3] != '':
								value[3] = 'DEFAULT {}'.format(value[3])
						#make sure to add a coma if its not the last col
						if comma_var == len(info_dict):
							statement_mid += '{col_name} {col_type}({col_size}) {null} {default} '.format(col_name = key ,col_type = value[0], col_size = value[1], null = value[2],default = value[3])
						else:
							statement_mid += '{col_name} {col_type}({col_size}) {null} {default} ,'.format(col_name = key  ,col_type = value[0], col_size = value[1], null=value[2],default=value[3])
						comma_var += 1
				#prepare the primary key constraint
				#currently this is the only way to add a PK
				#  - check the differences between this and the normal last value in the col info PK addidng
				pk_list = [key for key,value in items if key != 'table_name' and value[4] == 'Yes']
				if len(pk_list) > 0:
					statement_mid += ',CONSTRAINT pk_{} PRIMARY KEY ({})'.format(info_dict['table_name'],','.join(pk_list))
				#construct and execute the statement
				final_statement = statement_start + statement_mid + statement_end
				self.cursor.execute(final_statement)
				#returning the statement for displaying
				return final_statement
			else:
				raise ex.MaxTableNumberReached(5)
		except MySQLdb.Error as e:
			print e
			raise ex.TableExists(info_dict['name'])

	def view_table_info(self,table_name):
		#query the db for the table info
		statement = 'DESCRIBE %s' % table_name
		self.cursor.execute(statement)
		#the different fields that every columns contains, EXTRA is missing :(
		options = ('Field','Type','Null','Key','Default')
		to_return = {x:[] for x in options}
		records = self.cursor.fetchall()
		for tupl in records:
			#preserve the order in which they should be displayed
			#Ordered dict could be used aswell
			to_return['Order'] = ('Field','Type','Null','Key','Default')
			to_return['Field'].append(tupl[0])
			to_return['Type'].append(tupl[1])
			to_return['Null'].append(tupl[2])
			to_return['Key'].append(tupl[3])
			to_return['Default'].append(tupl[4])
		to_return['query'] = statement
		return to_return

	def insert_into(self,table_name,values):
		'''table_name - string 
			values - list of values to be entered in the table
		'''
		#get all the rows in that table because we need their len, check todo.txt GLOBAL
		all_values_statement = 'SELECT * FROM {}'.format(table_name)
		self.cursor.execute(all_values_statement)
		if len(self.cursor.fetchall()) < 10:
			#using a try block to avoid checking the values
			#delegating it to the database instead
			try:
				#querying the db for the column info
				desc_statement = 'DESCRIBE {}'.format(table_name)
				self.cursor.execute(desc_statement)
				columns = self.cursor.fetchall()
				#extracting the column names [0], the col types [1] and the null status [2]
				column_names,types,nulls = [[x[index] for x in columns] for index in xrange(3)]
				#preparing the statement
				start_statement = 'INSERT INTO {} ('.format(table_name)
				column_names = ','.join(column_names)
				mid_statement = ') VALUES ('
				#delegating the work to check and prepare the values to check_values
				values = ','.join(self.check_values(values,types,nulls))
				end_statement = ')'
				#prepare and execute the statement
				final_statement = start_statement+column_names+mid_statement+values+end_statement
				self.cursor.execute(final_statement)
				#return the statement for displaying
				return final_statement
			except MySQLdb.Error as e:
				#if a value is too big for the field catch the exception and raise more user friendly error
				if e[0] == 1264:
					raise ex.ValueTooBig()
				#raise this if a user enters a chars in int field
				elif e[0] == 1054:
					raise ex.InvalidIntValue()
				#raise this if a pk field uses already existing value
				elif e[0] == 1062:
					raise ex.PKDuplicate()
				#for dev purposes, print any error meseges that i still havent seen
				else:
					print e
		else:
			raise ex.MaxRowReached()

	def check_values(self,values_list,types_list,nulls_list):
		''' values_list = list of values to be prepared and checked
			types_list = list of the the types of the said values
			nulls_list = list that shows weather the values or NULL

		'''
		#check the null values and insert them as NULL instead of an empty string 
		#or raise a NullValue if there is no value in a primary key field
		for index in xrange(len(nulls_list)):
			if nulls_list[index] == 'NO':
				if values_list[index] == '':
					raise ex.NullValue()
			elif nulls_list[index] == 'YES':
				if values_list[index] == '':
					values_list[index] = 'NULL'

		#ccreating a list containing the indeces of the values that are int or are Null
		how_many = [x for x in xrange(len(types_list)) if types_list[x].startswith('int') or values_list[x] == 'NULL']
		#using the how_many list to determine if there should be quotes around the values or not
		values_list = ['"'+value+'"' if values_list.index(value) not in how_many else value for value in values_list]
		return values_list

	def get_columns(self,table_name,option=None):
		''' table_name - string
			option - if its not none, it will return the types and the col names
					else it will return only the names
			CHECK todo.txt GLOBAL > 1.1
		'''
		statement = 'DESCRIBE {}'.format(table_name)
		self.cursor.execute(statement)
		fetched = self.cursor.fetchall()
		columns = [column[0] for column in fetched]
		if option :
			types = [column[1] for column in fetched]
			return columns,types
		return columns

	def show_tables(self):
		''' check the todo.txt GLOBAL > 1.1 '''
		statement = 'SHOW TABLES'
		self.cursor.execute(statement)
		to_return = {'Name': [x[0] for x in self.cursor.fetchall()]}
		to_return['query'] = statement
		#returns a dictionary containing the raw sql query and the table names
		return to_return

	def show_table(self,table_name):
		''' table_name - string

		'''
		#get all values for the given table_name
		statement = 'SELECT * FROM {}'.format(table_name)
		to_return = {}
		#execute describe to get the column names
		column_statement = 'DESCRIBE {}'.format(table_name)
		self.cursor.execute(column_statement)
		column_info = self.cursor.fetchall()
		self.cursor.execute(statement)
		values = self.cursor.fetchall()
		#iterate over the rows add them to the dictionary
		for row in values:
			for index in xrange(len(row)):
				try:
					to_return[column_info[index][0]].append(row[index])
				except KeyError:
					to_return[column_info[index][0]] = [row[index]]
		to_return['query'] = statement
		return to_return

	def delete_table(self,table_name):
		statement = 'DROP TABLE {}'.format(table_name)
		self.cursor.execute(statement)
		return statement

	def alter_table(self,option,table_name,col_info):
		if option == 'add':
			columns = self.get_columns(table_name)
			if col_info[0] in columns:
				raise ex.ColumnExists()
			elif len(columns) >= 5:
				raise ex.MaxColumnReached()
			else:
				statement = 'ALTER TABLE {} ADD {} {}({})'.format(table_name,*col_info)
		elif option == 'drop':
			statement = 'ALTER TABLE {} DROP COLUMN {}'.format(table_name,col_info)
		try:
			self.cursor.execute(statement)
		except MySQLdb.OperationalError as e:
			if e[0] == 1091:
				raise ex.ColumnDeleted()
			elif e[0] == 1090:
				raise ex.OneColLeft()
		return statement

	def get_values(self,table_name,column_name):
		statement = 'SELECT {} FROM {}'.format(column_name,table_name)
		self.cursor.execute(statement)
		return [x[0] for x in self.cursor.fetchall()]

	def update(self,table_name,col_name,new_var,old_var):
		desc_statement = 'DESCRIBE {}'.format(table_name)
		self.cursor.execute(desc_statement)
		col_info = self.cursor.fetchall()
		for column in col_info:
			if column[0] == col_name:
				if not column[1].startswith('int'):
					old_var = '"' + old_var + '"'
					new_var = '"' + new_var + '"'
		statement = 'UPDATE {} SET {}={} WHERE {}={}'.format(table_name,col_name,new_var,col_name,old_var)
		self.cursor.execute(statement)
		return statement

	def select(self,table_name,col_name,value):
		desc_statement = 'DESCRIBE {}'.format(table_name)
		self.cursor.execute(desc_statement)
		col_info = self.cursor.fetchall()
		to_return = {}
		for column in col_info:
			to_return[column[0]] = []
			if column[0] == col_name:
				if not column[1].startswith('int'):
					value = '"' + value + '"'
		statement = 'SELECT * FROM {} WHERE {}={}'.format(table_name,col_name,value)
		self.cursor.execute(statement)
		keys = to_return.keys()
		for tupl in self.cursor.fetchall():
			for index in xrange(len(tupl)):
				to_return[keys[index]].append(tupl[index])
		to_return['query'] = statement
		return to_return

	def show_dbs(self):
		statement = 'SHOW DATABASES'
		self.cursor.execute(statement)
		return  {'Name' : [x[0] for x in self.cursor.fetchall()]}


	def start_server(self):
		''' VERY IMPORTANT NOTE : If the server is started manually it has to be closed manually'''
		process = pexpect.spawn('sudo -v')
		try:
			process.expect('Password:')
			process.sendline(self.root_pass)
		except pexpect.EOF:
			pass
		process2 = pexpect.spawn('sudo /usr/local/mysql/support-files/mysql.server start')

	def stop_server(self):
		self.connection.commit()
		self.connection.close()
		process = pexpect.spawn('sudo /usr/local/mysql/support-files/mysql.server stop')
		try:
			process.expect('Password:')
			process.sendline(self.root_pass)
		except pexpect.EOF:
			pass

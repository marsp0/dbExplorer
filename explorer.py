import MySQLdb
import pexpect
import excep as ex
import time
import sys

# Start the server from the terminal sudo /usr/local/mysql/support-files/mysql.server start
# Stop the server from the terminal sudo /usr/local/mysql/support-files/mysql.server stop
# Restart the server from the terminal sudo /usr/local/mysql/support-files/mysql.server restart


class Explorer(object):

	def __init__(self,root_username,root_password):
		#get the username for the root user, needed for the connection object
		self.root_user = root_username
		#get the password for the connection object and to start the server
		self.root_pass = root_password
		#start the mysql server
		#self.start_server()
		#time.sleep(2)
		#create the connection
		self.connection = MySQLdb.connect(host='',
											user = self.root_user,
											passwd = self.root_pass,
											db='test')
		self.cursor = self.connection.cursor()

	def create_table(self,info_dict):
		try:
			sentinel = 2
			statement_start = 'CREATE TABLE {table_name} ('.format(table_name = info_dict['table_name'])
			statement_end = ')'
			statement_mid = ''
			print info_dict
			for key,value in info_dict.items():
				if key != 'table_name':
					if sentinel == len(info_dict):
						statement_mid += '{col_name} {col_type}({col_size}) {null} {default} {extra}'.format(col_name = key  ,col_type = value[0], col_size = value[1], null=value[2],default=value[3],extra=value[4])
					else:
						statement_mid += '{col_name} {col_type}({col_size}) {null} {default} {extra},'.format(col_name = key  ,col_type = value[0], col_size = value[1], null=value[2],default=value[3],extra=value[4])
					sentinel += 1
			final_statemet = statement_start+statement_mid+statement_end
			self.cursor.execute(final_statemet)
			return True
		except Exception as e:
			raise ex.TableExists(info_dict['table_name'])

	def view_table_info(self,table_name):
		try:
			statement = 'DESCRIBE %s' % table_name
			self.cursor.execute(statement)
			to_return = {'Field':[],'Type':[],'Null':[],'Key':[],'Default':[],'Extra':[]}
			records = self.cursor.fetchall()
			for tupl in records:
				to_return['Order'] = ('Field','Type','Null','Key','Default','Extra')
				to_return['Field'].append(tupl[0])
				to_return['Type'].append(tupl[1])
				to_return['Null'].append(tupl[2])
				to_return['Key'].append(tupl[3])
				to_return['Default'].append(tupl[4])
				to_return['Extra'].append(tupl[5])
			return to_return
		except Exception:
			raise ex.TableDoesntExist(table_name)

	def insert_into(self,table_name,values):
		columns,types = self.get_columns(table_name,1)
		start_statement = 'INSERT INTO {} ('.format(table_name)
		columns = ','.join(columns)
		mid_statement = ') VALUES ('
		values = ','.join(self.check_values(values,types))
		end_statement = ')'
		final = start_statement+columns+mid_statement+values+end_statement
		self.cursor.execute(final)

	def check_values(self,values,types):	
		print types
		how_many = [x for x in xrange(len(types)) if types[x].startswith('int')]
		values = ['"'+value+'"' if values.index(value) not in how_many else value for value in values]
		return values

	def get_columns(self,table_name,option=None):
		statement = 'DESCRIBE {}'.format(table_name)
		self.cursor.execute(statement)
		fetched = self.cursor.fetchall()
		columns = [column[0] for column in fetched]
		if option :
			types = [column[1] for column in fetched]
			return columns,types
		return columns

	def show_tables(self):
		statement = 'SHOW TABLES'
		self.cursor.execute(statement)
		return {'Name': [x[0] for x in self.cursor.fetchall()]}

	def show_table(self,table_name):
		statement = 'SELECT * FROM {}'.format(table_name)
		to_return = {}
		column_statement = 'DESCRIBE {}'.format(table_name)
		self.cursor.execute(column_statement)
		checker = []
		for tupl in self.cursor.fetchall():
			to_return[tupl[0]] = []
			checker.append(tupl[0])
		self.cursor.execute(statement)
		for tupl in self.cursor.fetchall():
			for index in xrange(len(checker)):
				to_return[checker[index]].append(tupl[index])
		return to_return

	def delete_table(self,table_name):
		statement = 'DROP TABLE {}'.format(table_name)
		self.cursor.execute(statement)

	def alter_table(self,option,table_name,*args):
		if option == 'add':
			statement = 'ALTER TABLE {} ADD {} {}({})'.format(table_name,*args)
		elif option == 'drop':
			statement = 'ALTER TABLE {} DROP COLUMN {}'.format(table_name,*args)
		self.cursor.execute(statement)


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
			
		
	
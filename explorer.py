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
		self.start_server()
		time.sleep(8)
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
			items = info_dict.items()
			for key,value in items:
				if key != 'table_name':
					if sentinel == len(info_dict):
						statement_mid += '{col_name} {col_type}({col_size}) {null} {default} '.format(col_name = key ,col_type = value[0], col_size = value[1], null = value[2],default = 'DEFAULT ' + '"' + value[3] + '"' if value[0] == 'VARCHAR' else 'DEFAULT ' + value[3])
					else:
						statement_mid += '{col_name} {col_type}({col_size}) {null} {default} ,'.format(col_name = key  ,col_type = value[0], col_size = value[1], null=value[2],default='DEFAULT ' + '"' + value[3] + '"' if value[0] == 'VARCHAR' else 'DEFAULT ' + value[3])
					sentinel += 1
			
			pk_list = [key for key,value in items if value[4] == 'Yes']
			if len(pk_list) > 1:
				statement_mid += ',CONSTRAINT pk_{} PRIMARY KEY ({})'.format(info_dict['table_name'],','.join(pk_list))
			elif len(pk_list) == 1:
				statement_mid += ',CONSTRAINT pk_{} PRIMARY KEY ({})'.format(info_dict['table_name'],pk_list[0])
			final_statement = statement_start+statement_mid+statement_end
			self.cursor.execute(final_statement)
			return True
		except Exception as e:
			print e
			raise ex.TableExists(info_dict['table_name'])

	def view_table_info(self,table_name):
		try:
			statement = 'DESCRIBE %s' % table_name
			self.cursor.execute(statement)
			to_return = {'Field':[],'Type':[],'Null':[],'Key':[],'Default':[]}
			records = self.cursor.fetchall()
			for tupl in records:
				to_return['Order'] = ('Field','Type','Null','Key','Default')
				to_return['Field'].append(tupl[0])
				to_return['Type'].append(tupl[1])
				to_return['Null'].append(tupl[2])
				to_return['Key'].append(tupl[3])
				to_return['Default'].append(tupl[4])
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
		return to_return

	def show_dbs(self):
		statement = 'SHOW DATABASES'
		self.cursor.execute(statement)
		return  {'Name' : [x[0] for x in self.cursor.fetchall()]}


	def start_server(self):
		''' VERY IMPORTANT NOTE : If the server is started manually it has to be closed manually'''
		process = pexpect.spawn('sudo -v')
		#process.logfile = sys.stdout
		try:
			process.expect('Password:')
			process.sendline(self.root_pass)
		except pexpect.EOF:
			pass
		process2 = pexpect.spawn('sudo /usr/local/mysql/support-files/mysql.server start')
		#process2.logfile = sys.stdout

	def stop_server(self):
		self.connection.commit()
		self.connection.close()
		process = pexpect.spawn('sudo /usr/local/mysql/support-files/mysql.server stop')
		process.logfile = sys.stdout
		try:
			process.expect('Password:')
			process.sendline(self.root_pass)
		except pexpect.EOF:
			pass

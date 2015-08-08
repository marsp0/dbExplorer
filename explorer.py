import MySQLdb
import pexpect
import excep as ex
import time

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
		#create the connection
		#time.sleep(3)
		self.connection = MySQLdb.connect(host='',
											user = self.root_user,
											passwd = self.root_pass,
											db='test')
		self.cursor = self.connection.cursor()

	def create_table(self,table_name,col_info):
		try:
			statement_start = 'CREATE TABLE {table_name} ('.format(table_name = table_name)
			statement_end = ')'
			statement_mid = ''
			for key,value in col_info.items():
				statement_mid += '{col_name} {col_type} ({col_size})\n'.format(col_name = key, col_size = value[1],col_type = value[0])
			final_statemet = statement_start+statement_mid+statement_end
			self.cursor.execute(final_statemet)
			return True
		except Exception:
			raise ex.TableExists(table_name)

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

	def show_dbs(self):
		statement = 'SHOW DATABASES'
		self.cursor.execute(statement)
		return  {'Name' : [x[0] for x in self.cursor.fetchall()]}


	def start_server(self):
		''' VERY IMPORTANT NOTE : If the server is started manually it has to be closed manually'''
		process = pexpect.spawn('sudo /usr/local/mysql/support-files/mysql.server start')
		try:
			process.expect('Password:')
			process.send(self.root_pass)
		except pexpect.EOF:
			pass
		

if __name__=='__main__':
	p = Explorer('root','0899504274')
	#table_info = {'col1':('varchar','255')}
	#table_name = 'ssa'
	#p.create_table('ssa',table_info)
	print p.show_table('ssa')
	
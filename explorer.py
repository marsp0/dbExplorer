import MySQLdb
import pexpect
import excep as ex

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
		#create the connection
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
		except Exception:
			raise ex.TableDoesntExist(table_name)


	def start_server(self):
		''' VERY IMPORTANT NOTE : If the server is started manually it has to be closed manually'''
		process = pexpect.spawn('sudo /usr/local/mysql/support-files/mysql.server start')
		process.expect('Password:')
		process.send(self.root_pass)

if __name__=='__main__':
	p = Explorer('root','0899504274')
	table_info = {'col1':('varchar','255')}
	table_name = 'ssa'
	p.create_table('ssa',table_info)
	p.cursor.execute('SHOW tables')
	print p.cursor.fetchall()
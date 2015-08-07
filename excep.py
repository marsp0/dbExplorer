class DBException(Exception):

	pass

class TableErrors(DBException):

	def __init__(self,table_name):
		self.table_name = table_name

class TableExists(TableErrors):

	pass

class TableDoesntExist(TableErrors):

	pass
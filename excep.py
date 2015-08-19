class DBException(Exception):

	pass

class TableErrors(DBException):

	def __init__(self,table_name=None):
		self.table_name = table_name

class TableExists(TableErrors):

	pass

class TableDoesntExist(TableErrors):

	pass

class MaxTableNumberReached(TableErrors):

	def __init__(self,number):
		self.number = number

class ColumnDeleted(TableErrors):

	pass

class OneColLeft(TableErrors):
	pass

class ColumnExists(TableErrors):

	pass

class MaxColumnReached(TableErrors):

	pass

class MaxRowReached(TableErrors):
	pass

class ValueTooBig(TableErrors):

	pass

class InvalidIntValue(TableErrors):

	pass

class PKDuplicate(TableErrors):

	pass

class NullValue(TableErrors):

	pass

class ModulesNotFound(Exception):
	pass

class NoMYSQL(Exception):
	pass
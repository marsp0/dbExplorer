import Tkinter as tk
from collections import OrderedDict
import tkMessageBox as mb
import tkFileDialog as fd
from explorer import *

class Gui(tk.Frame):

	def __init__(self,parent=None,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)

		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.pack()

		'''main'''
		self.main_display = tk.Frame(self)
		self.table_main_display = tk.Frame(self)
		self.db_main_display = tk.Frame(self)
		self.login_display = tk.Frame(self)
		

		self.main_options = (
							('DB',(self.packer,(self.main_display,self.db_view))),
							('Table',(self.packer,(self.main_display,self.table_view))),
							('Export',(self.not_implemented,)),
							('Quit',(self.quit,))
							)

		self.db_options = (
							('Show DBs',(self.show_dbs,)),
							('Change DB',(self.not_implemented,)),
							('Delete DB',(self.not_implemented,)),
							('Back',(self.packer,(self.db_main_display,self.main_view)))
						)

		self.table_options = (
								('Tables',(self.show_tables,)),
								('View',(self.view_table,)),
								('Create',(self.create_table,)),
								('Alter',(self.alter_view,)),
								('Delete',(self.delete_table,)),
								('Insert',(self.insert,)),
								('Update',(self.update_view,)),
								('Select',(self.select_view,)),
								('Back',(self.packer,(self.table_main_display,self.main_view))),
							)
		self.main_explanations = (('Relational DB -' , 'collection of information stored in a tabular format. The data can be easily stored and retrieved.'),
									('Table -','structure inside the database that contains rows and columns. Example : Person'),
									('Column -',' defines the different qualities of the table. Example : Name, Age etc.'),
									('Row -',' contains the different records. Example : Ron, 34 , etc.'))

		self.table_name_var = tk.StringVar()
		self.column_var = tk.StringVar()
		self.alter_action_var = tk.StringVar()
		self.alter_add_vars = [tk.StringVar() for x in xrange(3)]

		self.update_new_var = tk.StringVar()
		self.update_old_var = tk.StringVar()

		self.select_val_var = tk.StringVar()

		self.data_type = ('VARCHAR','INT')
		self.create_table_vars = {i:[tk.StringVar() for x in xrange(6)] for i in xrange(1,6)}

		self.login_view()

	def login_view(self):
		self.login_display.pack()
		self.user_var = tk.StringVar()
		self.pass_var = tk.StringVar()
		tk.Label(self.login_display,text='Admin Username',width=20,pady=3,bd=2,relief='raised').grid(row=1,column=1)
		tk.Entry(self.login_display,textvariable=self.user_var).grid(row=1,column=2)
		tk.Label(self.login_display,text='Admin Password',width=20,pady=3,bd=2,relief='raised').grid(row=2,column=1)
		tk.Entry(self.login_display,textvariable=self.pass_var,show='*').grid(row=2,column=2)
		tk.Button(self.login_display,text='Quit',command=self.master.quit).grid(row=3,column=1)
		tk.Button(self.login_display,text='Login',command = self.login).grid(row=3,column=2)

	def login(self):
		try:
			self.explorer = Explorer(self.user_var.get(),self.pass_var.get())
			self.packer(self.login_display,self.main_view)
		except ex.ModulesNotFound:
			mb.showwarning('Error','Please make sure that the following modules are installed on your computer :\n- MySQLdb\n-pexpect\n\nLinks for these modules can be found in the readme file.')
		except ex.NoMYSQL:
			mb.showwarning('Error','Please make sure that MySQL is installed on this computer and that the credentials given are for the admin account.')

	def main_view(self):
		self.master.title('DB Explorer')
		'''create inside frames and pack them'''
		self.main_buttons_display = tk.Frame(self.main_display)
		self.main_expl_display = tk.Frame(self.main_display,bd=2,relief='raised')
		self.main_display.pack()
		self.main_buttons_display.pack(anchor='n')
		self.main_expl_display.pack()

		self.create_buttons(self.main_buttons_display,self.main_options)

		tk.Label(self.main_expl_display,text='Welcome to DB Explorer',width=20).grid(row=1,column=1,columnspan=2)
		tk.Label(self.main_expl_display,text='').grid(row=2,column=1)
		self.create_main_labels(self.main_expl_display,self.main_explanations)

	def db_view(self):
		self.master.title('DB')
		'''create inside frames and pack them'''
		self.db_buttons_display = tk.Frame(self.db_main_display)
		self.db_inner_display = tk.Frame(self.db_main_display,bd=2,relief='raised')
		self.db_main_display.pack()
		self.db_buttons_display.pack(anchor='n')
		self.create_buttons(self.db_buttons_display,self.db_options)

	def show_dbs(self):
		self.clean_inner_frame(self.db_inner_display)
		to_display = self.explorer.show_dbs()
		self.create_labels(self.db_inner_display,to_display)

	def table_view(self):
		self.master.title('Table')
		self.table_main_display.pack()
		'''create inside frames and pack them'''

		self.table_buttons_display = tk.Frame(self.table_main_display)
		self.table_buttons_display.pack(anchor='n')
		self.create_buttons(self.table_buttons_display,self.table_options)

		self.inner_parent_display = tk.Frame(self.table_main_display)
		self.inner_third_display = tk.Frame(self.inner_parent_display,bd=2,relief='raised')
		self.inner_second_display = tk.Frame(self.inner_parent_display)
		self.inner_first_display = tk.Frame(self.inner_parent_display)
		
		
		self.inner_parent_display.pack()
		

	def show_tables(self):
		self.clean_inner_parent()
		self.inner_second_display.pack()
		self.inner_second_display.config(bd=2,relief='raised')
		to_display = self.explorer.show_tables()
		query = to_display['query']
		del to_display['query']
		self.create_labels(self.inner_second_display,to_display)
		self.show_query(query)


	def view_table(self):
		self.clean_inner_parent()
		self.inner_first_display.pack()
		tables = self.explorer.show_tables()['Name']
		tk.Label(self.inner_first_display,text='Table Name').grid(row=1,column=1)
		tk.OptionMenu(self.inner_first_display,self.table_name_var,*tables).grid(row=1,column=2)
		tk.Button(self.inner_first_display,text='Search',command = self.search_table).grid(row=1,column=3)
		tk.Button(self.inner_first_display,text='Describe',command = self.describe_table).grid(row=1,column=4)

	def describe_table(self):
		if self.table_name_var.get() == '':
			mb.showwarning('Error','Please select a table from the list')
		else:
			self.clean_inner_frame(self.inner_second_display)
			self.inner_second_display.config(bd=2,relief='raised')
			results = self.explorer.view_table_info(self.table_name_var.get())
			order = results['Order']
			query = results['query']
			del results['Order']
			del results['query']
			col = 1
			width = 80/len(results)-1
			for item in order:
				tk.Label(self.inner_second_display,width = width,text=item,bd=3,relief='raised',pady=3).grid(row=0,column=col)
				for index in xrange(1,len(results[item])+1):
					tk.Label(self.inner_second_display,text=results[item][index-1],pady=3,bd=2,relief='raised',width = width).grid(row=index,column=col)
				col += 1
			self.show_query(query)

	def search_table(self):
		if self.table_name_var.get() == '':
			mb.showwarning('Error','Please select a table from the list')
		else:
			self.clean_inner_frame(self.inner_second_display)
			self.inner_second_display.config(bd=2,relief='raised')
			results = self.explorer.show_table(self.table_name_var.get())
			query = results['query']
			del results['query']
			self.create_labels(self.inner_second_display,results)
			self.table_name_var.set('')

			self.show_query(query)

	def create_table(self):
		self.clean_inner_parent()
		self.inner_first_display.pack()
		self.inner_second_display.pack()
		self.inner_second_display.config(bd=2,relief='raised')
		tk.Label(self.inner_first_display,text='Table Name').grid(row=1,column=1)
		tk.Entry(self.inner_first_display,textvariable=self.table_name_var).grid(row=1,column=2)
		

		tk.Label(self.inner_second_display,text='Name',width=13,bd=2,relief='raised',pady=3).grid(row=1,column=1)
		tk.Label(self.inner_second_display,text='Type',width=18,relief='raised',pady=3).grid(row=1,column=2)
		tk.Label(self.inner_second_display,text='Size',width=5,relief='raised',pady=3).grid(row=1,column=3)
		tk.Label(self.inner_second_display,text='Null',width=18,relief='raised',pady=3).grid(row=1,column=4)
		tk.Label(self.inner_second_display,text='Default',width=12,relief='raised',pady=3).grid(row=1,column=5)
		tk.Label(self.inner_second_display,text='Prime Key',width=12,relief='raised',pady=3).grid(row=1,column=6)

		for i in xrange(2,7):
			tk.Entry(self.inner_second_display,textvariable = self.create_table_vars[i-1][0],width=12).grid(row=i,column=1)
			tk.OptionMenu(self.inner_second_display,self.create_table_vars[i-1][1],*self.data_type).grid(row=i,column=2)
			tk.Entry(self.inner_second_display,textvariable = self.create_table_vars[i-1][2],width=3).grid(row=i,column=3)
			tk.OptionMenu(self.inner_second_display,self.create_table_vars[i-1][3],'NULL','NOT NULL').grid(row=i,column=4)
			tk.Entry(self.inner_second_display,textvariable=self.create_table_vars[i-1][4],width=11).grid(row=i,column=5)
			tk.OptionMenu(self.inner_second_display,self.create_table_vars[i-1][5],'Yes','No').grid(row=i,column=6)
			self.create_table_vars[i-1][5].set('No')

		tk.Button(self.inner_second_display,text='Save',command = self.save_table).grid(row=7,column=6)
	
	def save_table(self):
		result = self.prepare_check()
		if result:
			try:
				query = self.explorer.create_table(result)
				self.clean_create_table_vars()
				mb.showinfo('Success','The table is created :)')
				self.show_query(query)

			except ex.TableExists:
				mb.showwarning('Error','The name of the Table already exists in this database')
			except ex.MaxTableNumberReached as e:
				mb.showwarning('Error','You have reached the maximum number of tables allowed : {}'.format(e.number))
				self.table_name_var.set('')
		else:
			mb.showwarning('Error','Some of the fields you have entered are empty or contain an invalid value. Check again :)')

	def prepare_check(self):
		to_return = {}
		if self.table_name_var.get() == '' or all(self.create_table_vars[check][0].get() == '' for check in self.create_table_vars):
			return False
		to_return['table_name'] = self.table_name_var.get().replace(' ','_')
		for col in self.create_table_vars:
			name = self.create_table_vars[col][0].get()
			if name != '' and (self.create_table_vars[col][1].get() == '' or self.create_table_vars[col][2].get() == '' or self.create_table_vars[col][3].get() == ''):
				return False
			if name != '':
				if (not self.create_table_vars[col][2].get().isdigit()) or to_return.has_key(name):
					return False
				elif ' ' in [var.get() for var in self.create_table_vars[col][1:]]:
					return False
				else:
					to_return[name.replace(' ','_')] = [var.get().strip("'").replace('"',"'") for var in self.create_table_vars[col][1:]]
		return to_return

	def delete_table(self):
		self.clean_inner_parent()
		self.inner_first_display.pack()
		tables = self.explorer.show_tables()['Name']
		tk.Label(self.inner_first_display,text='Table Name').grid(row=1,column=1)
		tk.OptionMenu(self.inner_first_display,self.table_name_var,*tables).grid(row=1,column=2)
		tk.Button(self.inner_first_display,text='Delete',command = self.del_table).grid(row=1,column=3)

	def del_table(self):
		if self.table_name_var.get() == '':
			mb.showwarning('Error','Please select a table from the list')
		else:
			try:
				table_name = self.table_name_var.get()
				query = self.explorer.delete_table(table_name)
				self.table_name_var.set('')
				mb.showinfo('Table Deleted','The {} table was successfuly deleted'.format(table_name))

				self.show_query(query)
			except MySQLdb.Error:
				mb.showwarning('Error','The table you requested has already been deleted, please refresh')

	def insert(self):
		self.clean_inner_parent()
		self.inner_first_display.pack()
		self.inner_second_display.pack()
		tables = self.explorer.show_tables()['Name']
		tk.Label(self.inner_first_display,text='Table Name').grid(row=1,column=1)
		tk.OptionMenu(self.inner_first_display,self.table_name_var,*tables).grid(row=1,column=2)
		self.check_insert_button = tk.Button(self.inner_first_display,text='Check',command = self.insert_form)
		self.check_insert_button.grid(row=1,column=3)

	def insert_form(self):
		if self.table_name_var.get() == '':
			mb.showwarning('Error','You have to select a table')
		else:
			self.inner_second_display.config(bd=2,relief='raised')
			self.clean_inner_frame(self.inner_second_display)
			columns = self.explorer.get_columns(self.table_name_var.get())
			self.create_labels(self.inner_second_display,columns)
			self.create_insert_form(self.inner_second_display,len(columns))

	def save_insert(self):
		try:
			query = self.explorer.insert_into(self.table_name_var.get(),[var.get() for var in self.insert_vars])
			mb.showinfo('Success','The row was inserted in the table')
			self.table_name_var.set('')
			for var in self.insert_vars:
				var.set('')
			self.show_query(query)
			self.insert_button.config(command = self.refresh_page)
			self.check_insert_button.config(command = self.refresh_page)
		except ex.MaxRowReached:
			mb.showwarning('Error','Max number of rows reached : 10')
		except ex.ValueTooBig:
			mb.showwarning('Error','One of the values you are trying to insert is bigger than the specified column size')
		except ex.InvalidIntValue:
			mb.showwarning('Error','You are trying to insert a characters in an INT column')
		except ex.PKDuplicate:
			mb.showwarning('Error','One of the columns that you specified as PRIMARY KEY contains duplicate value that is already being used')
		except ex.NullValue:
			mb.showwarning('Error','You are passing a NULL value to a NO NULL column')

	def alter_view(self):
		self.clean_inner_parent()
		self.inner_first_display.pack()
		tables = self.explorer.show_tables()['Name']
		self.alter_action_var.set('Add')
		tk.Label(self.inner_first_display,text='Table Name').grid(row=1,column=1)
		tk.OptionMenu(self.inner_first_display,self.table_name_var,*tables).grid(row=1,column=2)
		tk.Label(self.inner_first_display,text='Action').grid(row=1,column=3)
		tk.OptionMenu(self.inner_first_display,self.alter_action_var,'Add','Drop','Alter').grid(row=1,column=4)
		self.alter_continue = tk.Button(self.inner_first_display,text='Continue',command = self.alter_table)
		self.alter_continue.grid(row=1,column=5)

	def alter_table(self):
		self.clean_inner_frame(self.inner_second_display)
		if self.table_name_var.get() == '' or self.alter_action_var.get() == '':
			mb.showwarning('Error','One of the values provided is incorect :(')
		else:
			self.inner_second_display.config(bd=2,relief='raised')
			table_name = self.table_name_var.get()
			action = self.alter_action_var.get()
			columns = self.explorer.get_columns(table_name) 
			if action == 'Add':
				self.create_labels(self.inner_second_display,('Column Name','Column Type','Column Size'))
				tk.Entry(self.inner_second_display,width=25,textvariable=self.alter_add_vars[0]).grid(row=2,column=1)
				tk.OptionMenu(self.inner_second_display,self.alter_add_vars[1],'VARCHAR','INT').grid(row=2,column=2)
				tk.Entry(self.inner_second_display,width=25,textvariable=self.alter_add_vars[2]).grid(row=2,column=3)
				self.alter_add = tk.Button(self.inner_second_display,text='Add',command = lambda : self.alter('add',table_name))
				self.alter_add.grid(row=3,column=3)
			elif action == 'Drop':
				row = 0
				for column in columns:
					tk.Label(self.inner_second_display,text=column,width = 56,bd=2,relief='raised',pady=3).grid(row=row,columns=1)
					tk.Button(self.inner_second_display,text='Drop',width = 20,command = lambda col = column: self.alter('drop',table_name,col)).grid(row=row,column=2)
					row += 1
			elif action == 'Alter':
				mb.showwarning('Error','This option is not yet implemented :(')

	def alter(self,option,table_name,*args):
		if option == 'add':
			if self.alter_add_vars[2].get().isdigit():
				try:
					query = self.explorer.alter_table('add',table_name,[var.get() for var in self.alter_add_vars])
					self.show_query(query)
					self.alter_add.config(command = self.refresh_page)
					self.alter_continue.config(command = self.refresh_page)
				except ex.ColumnExists as e:
					mb.showwarning('Error','The column already exists')
				except ex.MaxColumnReached:
					mb.showwarning('Error','Max number of columns reached : 5')
			else:
				mb.showwarning('Error','The value in the column size field should be a whole number')
		elif option == 'drop':
			try:
				query = self.explorer.alter_table('drop',table_name,*args)
				self.show_query(query)
			except ex.OneColLeft:
				mb.showwarning('Error','You cannot delete the last column of a table, try Delete Table')
			except ex.ColumnDeleted:
				mb.showwarning('Error','The column you are trying to delete is already deleted')

	def update_view(self):
		self.clean_inner_parent()
		self.inner_first_display.pack()
		tables = self.explorer.show_tables()['Name']
		tk.Label(self.inner_first_display,text='Table Name').grid(row=1,column=1)
		tk.OptionMenu(self.inner_first_display,self.table_name_var,*tables).grid(row=1,column=2)
		self.update_button = tk.Button(self.inner_first_display,text='Continue',command=self.update_view_cols)
		self.update_button.grid(row=1,column=5)

	def update_view_cols(self):
		if self.table_name_var.get() == '':
			mb.showwarning('Error','Please select a table')
		else:
			table_name = self.table_name_var.get()
			columns = self.explorer.get_columns(table_name)
			tk.Label(self.inner_first_display,text='Column Name').grid(row=1,column=3)
			tk.OptionMenu(self.inner_first_display,self.column_var,*columns).grid(row=1,column=4)
			self.update_button.config(command = lambda : self.display_update_options(table_name))

	def display_update_options(self,table_name):
		if self.column_var.get() == '':
			mb.showwarning('Error','Please select a column from the list')
		else:
			column = self.column_var.get()
			self.clean_inner_frame(self.inner_second_display)
			self.inner_second_display.config(bd=2,relief='raised')
			values = self.explorer.get_values(table_name, column)
			self.create_labels(self.inner_second_display,('New Value','Old Value'))
			tk.Entry(self.inner_second_display,textvariable=self.update_new_var,width=39).grid(row=2,column=1)
			tk.OptionMenu(self.inner_second_display,self.update_old_var,*values).grid(row=2,column=2)
			self.second_update_button = tk.Button(self.inner_second_display,text='Update',command = lambda : self.update(table_name,column))
			self.second_update_button.grid(row=3,column=2)

	def update(self,table_name,column):
		new_var = self.update_new_var.get()
		old_var = self.update_old_var.get()
		query = self.explorer.update(table_name,column,new_var,old_var)
		self.table_name_var.set('')
		self.column_var.set('')
		self.update_old_var.set('')
		self.update_new_var.set('')
		mb.showinfo('Success','The row was successfuly updated')
		self.show_query(query)
		self.update_button.config(command = self.refresh_page)
		self.second_update_button.config(command = self.refresh_page)

	def select_view(self):
		self.clean_inner_parent()
		self.inner_first_display.pack()
		tables = self.explorer.show_tables()['Name']
		tk.Label(self.inner_first_display,text='Table').grid(row = 1,column = 1)
		tk.OptionMenu(self.inner_first_display,self.table_name_var,*tables).grid(row=1,column=2)
		self.select_button = tk.Button(self.inner_first_display,text='Continue',command = self.display_select_options)
		self.select_button.grid(row=1,column=7)

	def display_select_options(self):
		if self.table_name_var.get() == '':
			mb.showwarning('Error','Please select a table')
		else:
			table_name = self.table_name_var.get()
			columns = self.explorer.get_columns(table_name)
			tk.Label(self.inner_first_display,text='Column').grid(row = 1,column = 3)
			tk.OptionMenu(self.inner_first_display,self.column_var,*columns).grid(row=1,column=4)
			self.select_button.config(command = lambda : self.display_select(table_name))

	def display_select(self,table_name):
		if self.column_var.get() == '':
			mb.showwarning('Error','Please select a column from the list')
		else:
			self.inner_second_display.pack()
			col_name = self.column_var.get()
			values = self.explorer.get_values(table_name,col_name)
			tk.Label(self.inner_first_display,text='Value').grid(row = 1,column = 5)
			tk.OptionMenu(self.inner_first_display,self.select_val_var,*values).grid(row=1,column=6)
			self.select_button.config(command = lambda : self.display_select_results(table_name,col_name))

	def display_select_results(self,table_name,col_name):
		if self.select_val_var.get() == '':
			mb.showwarning('Error','Please select a value from the list')
		else:
			value = self.select_val_var.get()
			self.inner_second_display.config(bd=2,relief='raised')
			to_display = self.explorer.select(table_name,col_name,value)
			query = to_display['query']
			del to_display['query']
			self.table_name_var.set('')
			self.column_var.set('')
			self.select_val_var.set('')
			self.create_labels(self.inner_second_display,to_display)
			self.show_query(query)
			self.select_button.config(command = self.refresh_page)

	''' HELPERS '''

	def refresh_page(self):
		mb.showwarning('Invalid Query','Please refresh the page before querying the database')

	def create_buttons(self,frame,options):
		column = 1
		for key,value in options:
			if len(value) > 1:
				function = value[0]
				args = value[1]
				tk.Button(frame,text = key,command = lambda args = args: function(*args) ).grid(row=0,column=column)
			else:
				tk.Button(frame,text=key,command = value[0]).grid(row=0,column=column)
			column += 1

	def create_main_labels(self,frame,options):
		row=3
		for name,desc in options:
			tk.Label(frame,text=name,width=15).grid(row=row,column=1)
			tk.Label(frame,text=desc,width=65,wraplength=300).grid(row=row,column=2)
			row+=1

	def create_labels(self,frame,options):
		current = 1
		if isinstance(options,dict):
			keys = options.keys()
			width = 80 / len(keys) if len(keys) < 5 else 80/len(keys) - 1
			while current != len(keys)+1:
				row=2
				tk.Label(frame,text=keys[current-1],bd=3,relief='raised',width=width,pady=3).grid(row=1,column=current)
				for value in options[keys[current-1]]:
					tk.Label(frame,text=value,bd=1,relief='raised',width=width,pady=3).grid(row=row,column=current)
					row += 1
				current += 1
		else:
			width = 80/len(options)
			for item in options:
				tk.Label(frame,text=item,bd=2,relief='raised',width=width).grid(row=1,column=current)
				current += 1

	def create_insert_form(self,frame,len_cols):
		self.insert_vars = [tk.StringVar() for x in xrange(len_cols)]
		width = (80/len_cols) - 1
		for index in xrange(1,len_cols+1):

			tk.Entry(frame,textvariable=self.insert_vars[index-1],width=width).grid(row=2,column=index)
		self.insert_button = tk.Button(frame,text='Insert',command = self.save_insert)
		self.insert_button.grid(row=3,column=index)


	def clean_create_table_vars(self):
		for col in self.create_table_vars:
			for item in self.create_table_vars[col]:
				item.set('')
		self.table_name_var.set('')

	def clean_inner_frame(self,frame):
		for child in frame.winfo_children():
			child.destroy()
		frame.pack()

	def clean_inner_parent(self):
		for child in self.inner_parent_display.winfo_children():
			if isinstance(child,tk.Frame):
				child.config(bd=0)
				try:
					child.pack_forget()
				except:
					child.grid_forget()
				finally:
					for ch in child.winfo_children():
						ch.destroy()
			else:
				child.destroy()

	def show_query(self,query):
		self.clean_inner_frame(self.inner_third_display)
		self.inner_third_display.config(relief='raised',bd=2)
		tk.Label(self.inner_third_display,text=query+';',width=80,pady=10,wraplength=500).grid(row=1,column=1)


	def packer(self,to_unpack,to_pack):
		for child in to_unpack.winfo_children():
			child.destroy()
		to_unpack.pack_forget()
		to_pack()

	def not_implemented(self):
		mb.showwarning('Error','The option is not yet implemented :(')

	def quit(self):
		self.explorer.stop_server()
		self.master.quit()

if __name__=='__main__':
	p = Gui()
	p.mainloop()
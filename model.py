import mysql.connector

class Model:
	def __init__(self, host_arg, user_arg, password_arg, database_arg = None):
		self.db = mysql.connector.connect(
			host=host_arg,
			user=user_arg,
			password = password_arg,
			database = database_arg
		)
		self.cursor = self.db.cursor()

	def save_user(self, voiceit_id, azure_ver_id="", azure_iden_id="", name=""):
		try:
			sql = """
			INSERT INTO voice_users (voiceit_id, azure_ver_id, azure_iden_id) 
				values (%s, %s, %s)
			"""
			values = (voiceit_id, azure_ver_id, azure_iden_id)
			self.cursor.execute(sql, values)
			self.db.commit()
			return "success"
		except Exception as e:
			return str(e)

	def get_user(self, voiceit_id):
		try:
			sql = "SELECT * FROM voice_users WHERE voiceit_id = %s"
			param = (voiceit_id, )
			self.cursor.execute(sql, param)
			result = self.cursor.fetchone()
			#print(result)
			return result
		except Exception as e:
			return str(e)

	def update_user(self, voiceit_id, name):
		try:
			sql = "UPDATE voice_users SET name = %s WHERE voiceit_id = %s"
			param = (voiceit_id, name, )
			self.cursor.execute(sql, param)
			result = self.cursor.fetchone()
			self.db.commit()
			return result
		except Exception as e:
			return str(e)

	def delete_user(self, voiceit_id):
		try:
			sql = "DELETE FROM voice_users WHERE voiceit_id = %s"
			param = (voiceit_id, )
			self.cursor.execute(sql, param)
			result = self.cursor.fetchone()
			self.db.commit()
			return result
		except Exception as e:
			return str(e)

	def create_group(name):
		try:
			sql = """
			"""
			param = (voiceit_id, )
			self.cursor.execute(sql, param)
			result = self.cursor.fetchone()
			self.db.commit()
			return result
		except Exception as e:
			return str(e)


#model = Model("localhost", 'root', 'Mysql_pw1?', 'silverservers')

#r1 = model.save_user("usr_1dd5ce96a0bd42a5990145384aa49ec4", 'id1', 'id2', 'diego')
#print(r1)

#r = model.get_user("usr_1dd5ce96a0bd42a5990145384aa49ec4")

#r = model.delete_user("usr_1dd5ce96a0bd42a5990145384aa49ec4")

mydb = mysql.connector.connect(
 	host="localhost",
 	user="root",
 	passwd="Mysql_pw1?",
 	database = 'silverservers'
)

cursor = mydb.cursor()

#mysql: silverservers2020

# cursor.execute("SELECT * FROM voice_users")

# result = cursor.fetchall()
# print(cursor)
# print(result)
# #sql.execute("SHOW DATABASES")

# q = """
# CREATE TABLE voice_users (
# 	p_key INT AUTO_INCREMENT PRIMARY KEY,
# 	name VARCHAR(64), 
# 	voiceit_id VARCHAR(40), 
# 	azure_ver_id VARCHAR(40), 
# 	azure_iden_id VARCHAR(40)
# )"""


# q = """
# CREATE TABLE voice_groups (
# 	p_key INT AUTO_INCREMENT PRIMARY KEY, 
# 	employee VARCHAR(128),
# 	voiceit_id VARCHAR(64),
# 	azure_id VARCHAR(64)
# )"""

# q = """
# CREATE TABLE user_groups(
# 	user_id INT, 
# 	group_id INT
# )
# """

# q = """
# CREATE TABLE azure_group(
# 	p_key INT AUTO_INCREMENT PRIMARY KEY, 
# 	name VARCHAR(128) 
# )
# """

cursor.execute("SHOW TABLES")

r = cursor.fetchall()
print(r)

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
            INSERT INTO voice_users (voiceit_id, name) 
                values (%s, %s)
            """
            values = (voiceit_id, name)
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
    
    def create_group(self, name, voiceit_id=None, azure_id=None):
        try:
            sql = """
            INSERT INTO voice_groups (name, voiceit_id) 
                values (%s, %s)
            """
            values = (name, voiceit_id)
            self.cursor.execute(sql, values)
            self.db.commit()
            return "success"
        except Exception as e:
            return str(e)
    
    def add_user_to_group(self, userId, groupId=1, name=""):
        try:
            result = self.get_user(userId)
            sql = """
            INSERT INTO user_groups (user_id, group_id)
                VALUES (%s, %s)
            """
            values = (result[0], groupId)
            self.cursor.execute(sql, values)
            self.db.commit()
            return "success"
        except Exception as e:
            return str(e)

model = Model("localhost", 'admin', 'silverserver2020', 'voiceauth')
#r1 = model.create_group(name = "general", voiceit_id = 'grp_bc595294f94341568dc66dd7a09790bc')
#r1 = model.get_user()
#print(r1)

#r = model.get_user("usr_1dd5ce96a0bd42a5990145384aa49ec4")

#r = model.delete_user("usr_1dd5ce96a0bd42a5990145384aa49ec4")

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    passwd="silverserver2020",
    database = 'voiceauth'
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
#   p_key INT AUTO_INCREMENT PRIMARY KEY,
#   name VARCHAR(64), 
#   voiceit_id VARCHAR(40), 
#   azure_ver_id VARCHAR(40), 
#   azure_iden_id VARCHAR(40)
# )"""


# q = """
# CREATE TABLE voice_groups (
#   p_key INT AUTO_INCREMENT PRIMARY KEY, 
#   name VARCHAR(128),
#   voiceit_id VARCHAR(64),
#   azure_id VARCHAR(64)
# )"""

# q = """
# CREATE TABLE user_groups(
#   user_id INT, 
#   group_id INT
# )
# """

# q = """
# CREATE TABLE azure_group(
#   p_key INT AUTO_INCREMENT PRIMARY KEY, 
#   name VARCHAR(128) 
# )
# """
# 
cursor.execute("select * from user_groups")
r = cursor.fetchall()
print(r)

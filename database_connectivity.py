import mysql.connector
def bot_user_response_storage(user_response, bot_response): 
              print("user_response", user_response)
              print("bot_response", bot_response)
              if(bot_response!='user'):
                mydb = mysql.connector.connect(
                        host="localhost", 
                        user="root",  
                        passwd="root", 
                        database="bits_chatbot") 
                mycursor = mydb.cursor()
                table_create="CREATE TABLE IF NOT EXISTS bot_storage (user_response VARCHAR(255), bot_response LONGTEXT)"
                mycursor.execute(table_create) 
                mydb.commit()
                sql='INSERT INTO bot_storage (user_response, bot_response) VALUES ("{0}", "{1}");'.format(user_response, bot_response) 
                mycursor.execute(sql)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")

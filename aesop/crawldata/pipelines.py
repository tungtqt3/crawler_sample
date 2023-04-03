# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#pip install mysql-connector-python
import mysql.connector,re
from mysql.connector import Error
from crawldata.functions import *

class CrawldataPipeline:
    def open_spider(self,spider):
        self.DATABASE_NAME='crawler'
        self.HOST='localhost'
        self.username='root'
        self.password='Crawler@2022'

        #self.DATABASE_NAME='crawler'
        #self.HOST='dev1.crawler.pro.vn'
        #self.username='root'
        #self.password='Crawler@2021'
        self.TABLE={}
        try:
            spider.conn = mysql.connector.connect(host=self.HOST,database=self.DATABASE_NAME,user=self.username,password=self.password,charset='utf8')
            if spider.conn.is_connected():
                print('Connected to DB')
                db_Info = spider.conn.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                SQL="SELECT table_name FROM information_schema.tables WHERE table_schema = '"+self.DATABASE_NAME+"' AND table_name='"+spider.name+"';"
                mycursor = spider.conn.cursor()
                mycursor.execute(SQL)
                myresult = mycursor.fetchall()
                for x in myresult:
                    self.TABLE[x[0]]=[]
                    SQL="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = Database() AND TABLE_NAME = '"+x[0]+"';"
                    mycursor.execute(SQL)
                    myresult1 = mycursor.fetchall()
                    for x1 in myresult1:
                        if not x1[0] in self.TABLE[x[0]]:
                            self.TABLE[x[0]].append(x1[0])
            else:
                print('Not connect to DB')
        except Error as e:
            print("Error while connecting to MySQL", e)
            spider.conn=None
    def close_spider(self,spider):
        if spider.conn.is_connected():
            spider.conn.close()
    def process_item(self, ITEM, spider):
        #print('Do with DB')
        # Check and add more field if not existed in data table
        item={}
        for K,V in ITEM.items():
            item[self.Get_Key_String(K)]=str(V).replace('\\','').replace("'","\'")
        if not 'SHEET' in item.keys():
            item['SHEET']=spider.name
        if not item['SHEET'] in self.TABLE:
            self.TABLE[item['SHEET']]=[]
            self.create_table(spider.conn,item['SHEET'],item)
        for key in item.keys():
            if not key in self.TABLE[item['SHEET']] and key!='SHEET':
                self.TABLE[item['SHEET']].append(key)
                self.add_column_to_db(spider.conn,item['SHEET'],key)
        # Insert data to table
        SQL="INSERT INTO "+item['SHEET']
        LIST_FIELDS=''
        VALUES=''
        STR_UPDATE=''
        for key in self.TABLE[item['SHEET']]:
            if LIST_FIELDS=='':
                LIST_FIELDS="`"+key+"`"
            else:
                LIST_FIELDS+=',`'+key+"`"
            if key in item:
                V=str(item[key]).replace("'","''").replace("\\","\\\\")
                if V=='None':
                    V=""
            else:
                V=""
            if VALUES=='':
                VALUES="'"+V+"'"
            else:
                VALUES+=",'"+V+"'"
            if not 'KEY_' in key:
                if STR_UPDATE=="":
                    STR_UPDATE="`"+key+"`='"+V+"'"
                else:
                    STR_UPDATE+=", `"+key+"`='"+V+"'"
        SQL+="("+LIST_FIELDS+") VALUES("+VALUES+") ON DUPLICATE KEY UPDATE "+STR_UPDATE+";"
        try:
            cursor = spider.conn.cursor()
            cursor.execute(SQL)
            spider.conn.commit()
            print('Isnerted to DB')
        except:
            print('Error: ',item,'\n',SQL)
        #return item
    def get_DataType(self,strtxt):
        strtxt=str(strtxt).strip()
        if Get_Number(strtxt)==strtxt:
            if '.' in strtxt and str(strtxt).count('.')==1:
                return 'FLOAT'
            elif not '.' in str(strtxt):
                return 'INT'
            else:
                return 'TEXT'
        else:
            return 'TEXT'
    def create_table(self,connection,table_name,item):
        SQL='CREATE TABLE IF NOT EXISTS '+table_name+'('
        KEY=' PRIMARY KEY ('
        i=0
        for K in item.keys():
            if 'KEY_' in K:
                SQL+=K+' VARCHAR(255) NOT NULL, '
                if i==0:
                    KEY+=K
                else:
                    KEY+=', '+K
                i+=1
        KEY+=')'
        SQL+=KEY+');'
        try:
            print('Creating Table:',table_name)
            print(SQL)
            cursor = connection.cursor()
            cursor.execute(SQL)
            connection.commit()
        except:
            print(SQL)
    def add_column_to_db(self,connection,table_name,field):
        SQL="ALTER TABLE "+table_name+" ADD COLUMN `"+field+"` "+self.get_DataType(field)+ " DEFAULT NULL;"
        #SQL="ALTER TABLE "+table_name+" ADD COLUMN "+field+" "+self.get_DataType(field)+ " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;"
        try:
            print('Adding column name:',field)
            cursor = connection.cursor()
            cursor.execute(SQL)
            connection.commit()
        except:
            print(SQL)
    def Get_Key_String(self,xau):
        KQ=re.sub(r"([^A-Za-z0-9])","_", str(xau).strip())
        return KQ
import sqlite3

class SQLlitePipeline(object):
   
    def open_spider(self,spider):
        self.connection = sqlite3.connect("DataBase.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE table_name(
                    UWI TEXT,
                    Pool TEXT,
                    Date DATE,
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self,spider):
        self.connection.close()
    
    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO prod_table (UWI,Pool,Date) VALUES(?,?,?)
        ''', (
            item.get('UWI'),
            item.get('Pool'),
            item.get('Date'),
        ))
        self.connection.commit()
        return item


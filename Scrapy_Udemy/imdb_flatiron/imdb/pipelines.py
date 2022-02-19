# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import sqlite3

# class SQLlitePipeline_Production(object):
   
#     def open_spider(self,spider):
#         self.connection = sqlite3.connect("movie_database.db")
#         self.c = self.connection.cursor()
#         try:
#             self.c.execute('''
#                 CREATE TABLE movie_table(
#                     UWI INT,           
#                     Gas INT
#                 )
#             ''')
#             self.connection.commit()
#         except sqlite3.OperationalError:
#             pass

#     def close_spider(self,spider):
#         self.connection.close()
    
#     def process_item(self, item, spider):
#         self.c.execute('''
#             INSERT INTO movie_table (UWI,Gas) VALUES(?,?)
#         ''', (
#             item.get('UWI'),
#             item.get('Gas')
#         ))
#         self.connection.commit()
#         return item


    

#!/usr/local/bin/python3

# psycopg2 to connect SQL database with python
import psycopg2

# set database as variable name
dbname = 'news'

# What are the most popular three articles of all time?
query1_title = '\n1. What are the most popular three articles of all time?'
query1 = 'select title, total from top_articles limit 3'

# Who are the most popular article authors of all time?
query2_title = '\n2. Who are the most popular article authors of all time?'
query2 = 'select name, total from top_authors'

# On which days did more than 1% of requests lead to errors?
query3_title = '\n3. On which days did more than'\
    ' 1 percent requests lead to errors?'
query3 = 'select date, error_percent from'\
    ' log_view_final where error_percent > 1.0'


def get_query_result(query):
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_output(input):
    for a in input:
        print('  ', a[0], '=>', a[1], 'views')

query1_result = get_query_result(query1)
query2_result = get_query_result(query2)
query3_result = get_query_result(query3)

print(query1_title)
print_output(query1_result)

print(query2_title)
print_output(query2_result)

print(query3_title)
print(query3_result[0][0], ' ', query3_result[0][1], 'errors')

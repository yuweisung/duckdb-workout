
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import duckdb
from IPython.display import display

g = np.random.default_rng()

months = 'Sep Oct Nov Dec Jan Feb Mar Apr May Jun'.split()
df = Series(g.integers(70,101, 10), index=months).to_frame()
df.columns = ['score']
df['month'] = df.index

display(df)

conn = duckdb.connect('test_score.db')
conn.execute('''
        CREATE TABLE if not exists scores (month varchar, score integer)
''')

conn.execute('''
        insert into scores select month,score from df
             ''')

display(conn.execute('select * from scores').df())

first = '''
    select avg(score) as first_average from scores where month in ('Sep','Oct','Nov','Dec','Jan')
'''

display(conn.execute(first).df())

second = '''
    select avg(score) as second_average from scores where month in ('Feb', 'Mar', 'Apr','May','Jun')
'''

display (conn.execute(second).df())

conn.execute('''truncate scores''')
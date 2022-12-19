import streamlit as st
import pandas as pd
import glob


def connect_db(database):
    # sqlite db in /home/Data (this is persistent storage in web apps azure)
    conn = sqlite3.connect(database)
    return conn


def initialize_db(db_name):
    con = connect_db(f'{DB_PATH}{db_name}')
    cur = con.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS table1 (
        log text,
        time text
    )
    '''
    cur.execute(sql)
    con.commit()
    con.close()



def create_table_entry(txt):
    '''add a row to a sqlite table'''
    con = connect_db(f'{DB_PATH}{db_name}')
    cur = con.cursor()
    sql = f'''
    INSERT INTO table1 VALUES
        ('{txt}, {time.time()}')
    '''
    cur.execute(sql)
    con.commit()
    con.close()

def display_table():
    '''read table into df and display in app'''
    con = connect_db(f'{DB_PATH}{db_name}')
    sql = f'''
    select * from table1;
    '''
    df = pd.read_sql(sql, con)
    st.dataframe(df)
    con.close()




def page():
    # create database button test...
    st.write('DB testing...')
    q = st.text_input('ls arg', '/')
    if st.button('list files...'):
        st.dataframe(pd.DataFrame(data=glob.glob(q), columns=['files']))

    db_name = st.text_input('Database file name:','database.db')
    if st.button('init database'):
        initialize_db(db_name)

    txt = st.text_input('log entry text', '')
    if st.button('submit log entry'):
        create_table_entry(txt)

    if st.button('show logs'):
        display_table()

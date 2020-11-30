import sqlite3
from sqlite3 import Error
DBPATH = "bot.db"

def db_connect():
  conn = None
  try:
    conn = sqlite3.connect(DBPATH)
    return conn
  except Error as e:
      print(e)
  return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def init_db():

  sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS members (
                                        id integer PRIMARY KEY,
                                        discord_name text NOT NULL,
                                        in_game_name text,
                                        contact text
                                    ); """

  sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS epic_bp_needed (
                                    id integer PRIMARY KEY,
                                    discord_name text NOT NULL,
                                    ship_name text NOT NULL UNIQUE,
                                    bp_have integer NOT NULL
                                );"""

  conn = db_connect()

  if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
  else:
        print("Error! cannot create the database connection.")

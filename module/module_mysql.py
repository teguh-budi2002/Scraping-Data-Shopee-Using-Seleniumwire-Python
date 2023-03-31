import mysql.connector as mysql

class MySQL:
  def connection(self):
    try:
      connect_sesion = mysql.connect(
        host= '127.0.0.1',
        user= "teguhdb",
        password= "teguhbudi",
        database= "warehouse"
      )
      return connect_sesion
    except mysql.Error as e:
      err_mess = print(f"Error While Connection: {e}")
      return err_mess

  def query(self, conn):
    cursor = conn.cursor()
    return cursor

  def get_all_data_from_table(self, conn, table):
    try:
      query = self.query(conn)
      query.execute(f"SELECT * FROM {table}")
      results = query.fetchall()
      for res in results:
        return res
    except mysql.Error as e:
      err_mess = print(f"Something Went Wrong: {e}")
      return err_mess

  def add_data(self, conn, table, data_list):
    try:
      placeholders = ', '.join(['%s'] * len(data_list[0]))
      columns = ', '.join(data_list[0].keys())
      sql =  "INSERT INTO {} ({}) VALUES ({})".format(table, columns, placeholders)

      for data in data_list:
        query = self.query(conn)
        query.execute(sql, list(data.values()))
        conn.commit()
      return print(f"Data Success Inserted {query.rowcount}")

    except mysql.Error as e:
      err_mess = print(f"Something Went Wrong: {e}")
      return err_mess
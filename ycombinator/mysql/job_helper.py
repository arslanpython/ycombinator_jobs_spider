from mysql.connector import connect
from mysql.connector import Error


class JobHelper:
    def open_db_conn(self):
        try:
            conn = connect(host='localhost', user='root',
                           password='admin', database='jobs')
            # if conn.is_connected():
            #     print("Connected With Database")
            return conn
        except Error as err:
            print(err)

    def close_db_conn(self, conn, cursor):
        if conn.is_connected():
            cursor.close()
            conn.close()

    def insert(self, jobs):
        conn = self.open_db_conn()
        cursor = conn.cursor()
        try:
            if jobs:
                columns = ', '.join(jobs[0].keys())
                placeholders = ', '.join(['%s'] * len(jobs[0]))
                sql = f'INSERT INTO new_jobs ({columns}) VALUES({placeholders})'
                for job in jobs:
                    cursor.execute(sql, tuple(job.values()))

                conn.commit()
        except Error as error:
            print(error)

        finally:
            self.close_db_conn(conn, cursor)

    def get_ids(self):
        conn = self.open_db_conn()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT job_id from new_jobs')
            ids = cursor.fetchall()
            return ids

        except Error:
            print(Error)

        finally:
            self.close_db_conn(conn, cursor)

    def filter(self, job_id):
        conn = self.open_db_conn()
        cursor = conn.cursor()

        try:
            sql = f'SELECT job_id FROM new_jobs WHERE job_id = {job_id}'
            cursor.execute(sql)
            return cursor.fetchone()

        except Error:
            print(Error)

        finally:
            self.close_db_conn(conn, cursor)

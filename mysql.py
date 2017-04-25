# -*- coding: utf-8 -*-
import pymysql.cursors


class Mysql:

    def __init__(self):
        self._connect = pymysql.connect(host='localhost', user='root',
                                        password='', db='crawler', charset='utf8')

    def migrate(self, ddl):
        try:
            with self._connect.cursor() as cursor:
                # Create a new record
                cursor.execute(ddl)

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                self._connect.commit()
        except Exception as inst:
            print(inst)
            self._connect.close()

    def read(self, ddl):
        try:
            with self._connect.cursor() as cursor:
                # Read a single record
                cursor.execute(ddl)
                result = cursor.fetchone()
                print(result)
        except Exception as inst:
            print(inst)
            self._connect.close()

    def close(self):
        self._connect.close()


if __name__ == "__main__":
    sql = Mysql()
    with open("db/migration/V201704242121__add_tables.sql", "r") as f:
        sql.migrate(f.read())
    with open("db/migration/V__init_tables.sql", "r", encoding="utf-8") as f:
        sql.migrate(f.read())
    sql.close()


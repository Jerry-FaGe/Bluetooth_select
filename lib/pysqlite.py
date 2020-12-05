import sqlite3
import os

server_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ConnSql(object):
    def __init__(self, db_path=r'{}'.format(server_root_path), db_name='bluetooth.sqlite3'):
        self.db_path = '{}/{}'.format(db_path, db_name)
        self.cxn = None
        self.cur = None

    def conn_db(self):
        self.cxn = sqlite3.connect(self.db_path)
        self.cur = self.cxn.cursor()

    def close_db(self):
        if self.cxn and self.cur:
            self.cur.close()
            self.cxn.close()

    def create_table(self, create_teble_sql):
        # self.cur.execute('''
        #     CREATE TABLE users(
        #         id INTEGER primary key,
        #         name varchar(20)
        #         )
        #     ''')
        self.cur.execute(create_teble_sql)

    def drop_table(self, table):
        self.cur.execute("drop table %s;" % table)

    def search_info(self, search_sql):
        # get_info = self.cur.execute('''
        #         select * from users
        #     ''')
        get_info = self.cur.execute(search_sql)
        print(get_info)
        return get_info

    def update_info(self, update_sql):
        # self.cur.execute('''
        #         insert into users (name) values ('test_name1')
        #     ''')
        self.cur.execute(update_sql)
        self.cxn.commit()

    def show_table(self):
        """
        sqlite3 存在一个系统表 sqlite_master,结构如下：
        sqlite_master(
            type TEXT,
            name TEXT,
            tbl_name TEXT,
            rootpage INTEGER,
            sql TEXT
        )
        通过这个表，可以查看当前数据库有哪些表
        """

        get_table_sql = "select * from sqlite_master where type='table' "
        tables_info = self.cur.execute(get_table_sql)
        # print(self.cur.fetchall())

        result = []
        for table_info in tables_info:
            result.append(table_info[1])

        return result


def sql_main():
    sql_obj = ConnSql()
    sql_obj.conn_db()
    # sql_obj.create_table(create_teble_sql='''
    #         CREATE TABLE test_info(
    #             id INTEGER primary key,
    #             uuttype varchar(20),
    #             sn varchar(20),
    #             product_name varchar(20),
    #             date date(20)
    #             )
    #         ''')
    # sql_obj.update_info(update_sql='''
    #                 insert into test_info (uuttype,sn,product_name,date) values
    #                 ('74-123646-01','foc23264602','bermuda','19-06-02')
    #                 ''')
    # info = sql_obj.search_info(search_sql='''select * from test_info''')
    # for i in info:
    #     print(i)
    sql_obj.show_table()

    sql_obj.close_db()


if __name__ == '__main__':
    sql_main()

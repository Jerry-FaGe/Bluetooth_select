import requests
from lxml import etree
from lib import pysqlite

url = "https://www.bluetooth.com/specifications/gatt/services/"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 '
                  'Safari/537.36',
}


# 定义请求函数
def get_html(url, headers):
    try:
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return response.content.decode()
    except requests.RequestException:
        return None


# 定义解析函数
def resolve_html(content):
    html = etree.HTML(content)
    result = html.xpath('//tbody/tr')
    for i in result:
        ls = i.xpath('td/text()')
        yield {
            'Name': ls[0],
            'Uniform Type Identifier': ls[1],
            'Assigned Number': ls[2],
            'Specification': ls[3],
        }


# 写入文件
def write_item_to_db(item, conn, table):
    print('开始写入数据 ====> ' + str(item))
    conn.update_info(update_sql="""
            insert into %s ('NAME' ,'Uniform Type Identifier', 'Assigned Number', 'Specification')
                values ("%s","%s","%s","%s")""" % (table,
                                                   item['Name'],
                                                   item['Uniform Type Identifier'],
                                                   item['Assigned Number'],
                                                   item['Specification']))


# 主函数
def main():
    table = "Bluetooth_services"
    conn = pysqlite.ConnSql()
    conn.conn_db()
    if table in conn.show_table():
        conn.drop_table(table)
    conn.create_table(create_teble_sql='''
            CREATE TABLE %s(
                'NAME'                    CHAR(50),
                'Uniform Type Identifier'  CHAR(50),
                'Assigned Number'         CHAR(50),
                'Specification'           CHAR(50));''' % table)
    content = get_html(url, headers)
    items = resolve_html(content)
    for item in items:
        write_item_to_db(item, conn, table)


if __name__ == "__main__":
    main()

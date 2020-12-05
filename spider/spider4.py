import requests
from lxml import etree
from lib import pysqlite

url = "https://www.bluetooth.com/specif5yications/assigned-numbers/generic-access-profile/"
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
            'Data Type Value': ls[0],
            'Data Type Name': ls[1],
            'Reference for Definition': ls[2] if len(ls) == 3 else "",
        }


# 写入文件
def write_item_to_db(item, conn, table):
    print('开始写入数据 ====> ' + str(item))
    conn.update_info(update_sql="""
                insert into %s
                    ('Data Type Value' ,'Data Type Name', 'Reference for Definition')
                    values ("%s","%s","%s")""" % (table,
                                                  item['Data Type Value'],
                                                  item['Data Type Name'],
                                                  item['Reference for Definition']))


# 主函数
def main():
    table = "Bluetooth_generic_access_profile"
    conn = pysqlite.ConnSql()
    conn.conn_db()
    if table in conn.show_table():
        conn.drop_table(table)
    conn.create_table(create_teble_sql='''
            CREATE TABLE %s(
                'Data Type Value'                  CHAR(50),
                'Data Type Name'                   CHAR(50),
                'Reference for Definition'         CHAR(50));''' % table)
    content = get_html(url, headers)
    items = resolve_html(content)
    for item in items:
        write_item_to_db(item, conn, table)


if __name__ == "__main__":
    main()

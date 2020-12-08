import requests
from bs4 import BeautifulSoup as bs
import csv
from zipfile import ZipFile
import dateutil.parser
from datetime import datetime
import mysql.connector
from flask import Config


config = Config('..')
config.from_pyfile('settings.cfg')

conn = mysql.connector.connect(**config['BRAZIL_DB'])

url ='http://www.portaltransparencia.gov.br/download-de-dados/ceaf'

def get_date_info():

    page = requests.get(url)
    soup = bs(page.content,'html.parser')
    script_load = ''
    date={'ano':'','mes':'','dia':''}
    for script in soup.find_all('script'):
        for s in script.contents:
            if 'arquivos.push' in s:
                script_load =s.split('"')
    date['ano'] = script_load[script_load.index('ano') + 2]
    date['mes'] = script_load[script_load.index('mes') + 2]
    date['dia'] = script_load[script_load.index('dia') + 2]

    str_date = date['ano'] + date['mes'] + date['dia']

    return str_date

def collect_data(conn):
    c = conn.cursor()
    date = get_date_info()
    sql_check ='''Select distinct date_dump from Brazil_demo where date_dump =%s; '''
    c.execute(sql_check, (date,))
    check_date = c.fetchone()
    if check_date is None:
        link = url + '/' + date
        data = requests.get(link)
        path_zip = date +'.zip'
        open(path_zip, 'wb').write(data.content)
        # Extract file csv
        with ZipFile(path_zip,"r") as zip_ref:
            listfiles = zip_ref.filelist
            for name in listfiles:
                zip_ref.extract(name.filename, 'crawl_data')
                with open('crawl_data/{}'.format(name.filename), encoding='latin-1') as csv_file:
                    reader = csv.reader(csv_file, delimiter='\t')
                    next(reader, None)
                    sql = '''Insert ignore into Brazil_demo values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
                    for row in reader:
                        check = []
                        for check_list in row:
                            res_split =check_list.split(';')
                            check.extend(res_split)

                        res = []

                        for fixed_row in check:
                            r = fixed_row.split('\"')
                            res.append(r[len(r)-2])
                        if res[9] =='NI':
                            res[9] = None
                        c.execute(sql, (res[0], res[1], res[2], res[3], res[4],res[5], res[6],
                                        res[7], datetime.fromtimestamp(dateutil.parser.parse(str(res[8])).timestamp()).strftime("%Y-%m-%d"),
                                        res[9], res[10], res[11],
                                        res[12], ''.join(res[13:]), date))
                        conn.commit()
    conn.close()

run = collect_data(conn)
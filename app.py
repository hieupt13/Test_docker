import connexion
import logging
import sys
import mysql.connector
from flask_env import MetaFlaskEnv
from mysql.connector import pooling

def apikeyauth(apikey, required_scopes):
    """
    Look up apikey in table users, return id and username in dict form
    """
    if apikey == application.config['AUTH_KEY']:
        ret = {'username': "test"}
    else:
        ret = None
    return ret

def create_connection():
    """Create a database connection to the mySQL database

    :return: connection object or None
    """
    conn = None
    try:
        conn = cnxpool.get_connection()

    except Exception as e:
        print('Error occured: {}'.format(str(e)))

    return conn

def get_find_information(conn, input):
    """
    Get all result getList based on particular priority
    :param conn: connection to database
    :param input: options to get relavent term
    :return: getList
    """
    getList = []
    term = '%' + input + '%'
    cur = conn.cursor()
    sqlst = '''select * from Brazil_demo where name like %s ;'''
    cur.execute(sqlst, (term,))
    response = cur.fetchall()
    for res in response:
        info = {'Name': res[0], 'CPF': res[1], 'MAT': res[2], 'ORG': res[3], 'State': res[4],
                'charge': res[5], 'CFC': res[6], 'NPP': res[7], 'charge_date': res[8],
                "pages": res[9], 'sessions': res[10], 'types': res[11], 'Num_pro': res[12],
                'law': res[13], 'date_dump': res[14]}
        for check in info.copy():
            if info[check] is None or info[check] == '':
                info.pop(check)
        getList.append(info)
    return getList

def search(find):
    conn = create_connection()
    get_list = get_find_information(conn, find)
    conn.close()
    if len(get_list) == 0:
        return [], 404
    return get_list, 200

logger = logging.getLogger('brazil_ceaf')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info("Starting: {}".format(__file__))

app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('brazil_ceaf.yaml')
application = app.app

class Configuration(metaclass=MetaFlaskEnv):
    BRAZIL_DB = {
        "user": "brazil",
        "password": "brazil2020",
        "host": "mysql-service",
        "port": '3306',
        "database": "Brazil_ceaf"
    }
    AUTH_KEY = 'xxxxxxxxxx'
try:
    application.config.from_pyfile('settings.cfg')
except FileNotFoundError:
    application.config.from_object(Configuration)

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="brazil_ceaf",
                                                      database=application.config['BRAZIL_DB']['database'],
                                                      user=application.config['BRAZIL_DB']['user'],
                                                      host =application.config['BRAZIL_DB']['host'],
                                                      password=application.config['BRAZIL_DB']['password'],
                                                      port=application.config['BRAZIL_DB']['port'],
                                                      pool_size=20)
if __name__ == '__main__':
    app.run()
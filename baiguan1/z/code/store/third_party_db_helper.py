import sqlalchemy
import logging


class OracleHelper(object):

    def __init__(self, host, user, passwd, dbname, port='1521'):
        self.db_url = 'oracle+cx_oracle://%s:%s@%s:%s/%s' % \
            (user, passwd, host, port, dbname)
        self.engine = sqlalchemy.create_engine(self.db_url)
        logging.info('dburl: ' + self.db_url)

    def __exec_query(self, query, params={}):
        with self.engine.connect() as con:
            result = con.execute(sqlalchemy.text(query), {})
            return [r for r in result]

    def __check_permission(self, con, query, name):
        try:
            r = con.execute(query).fetchall()
            if len(r) > 0:
                return {'code': 0, 'name': name}
            else:
                return {'code': 1, 'name': name}
        except Exception as e:
            return {'code': 2, 'name': name, 'msg':
                    'failed to retrieved the inforamation' +
                    e.message}

    def verify_permissions(self):
        job_queue_processes_val_query = \
            "SELECT value from v$parameter WHERE name='job_queue_processes'"
        has_change_notification_query = \
            "SELECT * FROM SESSION_PRIVS WHERE PRIVILEGE='CHANGE NOTIFICATION'"
        has_dbms_change_notification_query = \
            "SELECT * FROM USER_TAB_PRIVS WHERE TABLE_NAME='DBMS_CHANGE_NOTIFICATION'"
        has_create_any_trigger = \
            "SELECT * FROM SESSION_PRIVS WHERE PRIVILEGE='CREATE ANY TRIGGER'"
        has_dbms_laert_query = \
            "SELECT * FROM USER_TAB_PRIVS WHERE TABLE_NAME='DBMS_ALERT'"
        # 0 -- ok
        # 1 -- no privilege
        # 2 -- failed to retrieve
        result = []
        with self.engine.connect() as con:
            try:
                r = con.execute(job_queue_processes_val_query).fetchall()[0]
                if r[0] > 0:
                    result.append({'code': 0,
                                   'name': 'job_queue_processes > 1'})
                else:
                    result.append({'code': 1,
                                   'name': 'job_queue_processes > 1'})
            except Exception as e:
                result.append(
                    {'code': 2, 'name': 'job_queue_processes > 1', 'msg':
                     'failed to retrieved the inforamation' +
                     e.message})

            result.append(self.__check_permission(
                con,
                has_change_notification_query,
                'CHANGE NOTIFICATION'))
            """
            result.append(self.__check_permission(
                con,
                has_dbms_change_notification_query,
                'EXECUTE DBMS_CHANGE_NOTIFICATION'))
            result.append(self.__check_permission(
                con,
                has_create_any_trigger,
                'CREATE ANY TRIGGER'))
                """
            result.append(self.__check_permission(
                con,
                has_dbms_laert_query,
                'EXECUTE DBMS_ALERT'))
            return result

    def get_column_names(self, table_name):
        query = """
SELECT column_name
FROM   all_tab_cols
WHERE  table_name = :table_name
                """
        with self.engine.connect() as con:
            r = con.execute(sqlalchemy.text(query), table_name=table_name)
            return [i[0] for i in r.fetchall()]

    def gen_alert_str(self, columns):
        cols_str = ["',%s:' || :new.%s" % (c, c) for c in columns]
        return ' || '.join(cols_str)

    def add_db_notification_trigger(self, table_name):
        trigger_name = 'cmdata_dbtrigger_%s' % table_name
        alert_name = 'cmdata_dbalert_%s' % table_name
        logging.info('Creating trigger with name %s' % trigger_name)
        columns = self.get_column_names(table_name)
        alert_str = self.gen_alert_str(columns)
        query = """CREATE OR REPLACE TRIGGER %s
AFTER INSERT
    ON %s
   FOR EACH ROW
DECLARE
  PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
   dbms_alert.signal('%s', %s);
   commit;
END;
""" % (trigger_name, table_name, alert_name, alert_str)
        print(query)
        with self.engine.connect() as conn:
            conn.execute(query)
        return (trigger_name, alert_name)

    def get_user_table_names(self):
        query = """SELECT table_name,owner
        FROM all_tables
        WHERE
          OWNER != 'SYS'
        AND
          OWNER != 'CTXSYS'
        AND
          OWNER !='SYSTEM'
        AND
          OWNER != 'OUTLN'
        AND
          OWNER != 'DBSNMP'
        AND
          OWNER != 'APPQOSSYS'
        """
        res = self.__exec_query(query)
        print('Get %d table names' % len(res))
        return [r[0] + ',' + r[1] for r in res]


def get_db_helper_by_type(db_type_code, host, user, passwd, dbname, port=None):
    if db_type_code is 0:
        if port is None:
            port = '1521'
        return OracleHelper(host, user, passwd, dbname, port)


if __name__ == "__main__":
    """for testing"""
    host = "cm-oracle-test.cdl8ar96w1hm.rds.cn-north-1.amazonaws.com.cn"
    port = "1521"
    dbname = "ORCL"
    user = "cmdata"
    password = "cmdata2016"
    user = 'test'
    password = 'test'
    helper = get_db_helper_by_type(
        0,
        host,
        user,
        password,
        dbname,
        port)
    r = helper.get_user_table_names()
    for i in r:
        print(i)
    r = helper.get_column_names('ORDERS')
    for i in r:
        print(i)
    # print(helper.gen_alert_str(r))

    # print(helper.add_db_notification_trigger('ORDERS'))
    print(helper.verify_permissions())

import pymysql
import configparser

#   pip install pymysql
#   pip install configparser

#   使用方法一：要么在目录下建名称为config.ini的文件，然后写入
'''
[mysql]
HOST = 127.0.0.1
USER = root
PASS = 123456
CHAR = utf8
DB = bigsoft
PORT = 3306
PREFIX =
'''
#    使用方法二：要么直接改如下参数，方式一调用失败会使用下面参数

HOST = '127.0.0.1'  # 链接地址
USER = 'root'  # 数据库用户
PASS = '123456'  # 数据库密码
CHAR = 'utf8'  # 编码格式
DB = 'bigsoft'  # 数据库名称
PORT = 3306     # 数据库端口号
PREFIX = ''  # 表前缀

#   1、实例化类 sql = Db()
#   参数类：
#   table方法：入参：表名
#       使用方法: sql.table('test') 或 sql.name('test')
#   where方法：可多次调用，入参：字符串或字典(key:字段名,val:值,type:对应关系,默认为'=')或数组
#       使用方法: sql.where('id=1')
#       使用方法: sql.where({'id',1})
#       使用方法: sql.where({'id',1,'<>'})
#       使用方法: sql.where({'id','(1,2)','in'})
#       使用方法: sql.where([{'id','(1,2)','in'},{'name','%我%','like'}])
#   whereRow方法:可多次调用，入参：字段名,值,对应关系
#       使用方法: sql.whereRow('id',1)
#       使用方法: sql.whereRow('id',1,'>')
#   whereIn方法:可多次调用，入参：字段名,值(逗号拼接的字符串或元组)
#       使用方法: sql.whereIn('id','1,2')
#       使用方法: sql.whereIn('id',(1,2))
#   whereLike方法:可多次调用，入参：字段名,值
#       使用方法: sql.whereLike('name','%我%')
#   alias方法:对 table 方法的表名设置 别名
#       使用方法: sql.table('test').alias('a')
#   limit方法：查询前N条数据，入参：数量
#       使用方法: sql.limit(10)
#   order方法：排序，入参：排序字符串
#       使用方法: sql.order('id desc')
#   group方法:分组，入参：字符串
#       使用方法: sql.group('name,title')
#   field方法：查询字段,入参：字符串
#       使用方法: sql.field('id,name,title,create_time')
#   distinct方法：去重，入参：True或False，默认为True
#       使用方法: sql.distinct()
#   having方法：入参：字符串
#       使用方法: sql.having('b.id=1')
# =====================================================================================
#   操作类：
#   buildSql    返回select查询语句，出参：字符串
#       使用方法: sql.buildSql()
#   find    返回符合条件的第一条数据，出参：字典
#       使用方法: sql.find()
#   count   返回符合条件的数量：出参：Int
#       使用方法: sql.count()
#   value   入参：字段名，返回符合条件的一个字段的值，出参：值
#       使用方法: sql.value('name')
#   select  返回符合条件的多数据，出参：数组<字典>
#       使用方法: sql.select()
#   get 入参：值，识别主键返回符合条件的第一条数据，出参：字典
#       使用方法: sql.get(2)
#   insert  入参：字典,字段识别后根据键名插入数据,自动剔除表中没有的字段，出参：变更数量
#       使用方法: sql.insert({'id':1,'name':'你好'})
#   insertGetId 入参：字典,字段识别后根据键名插入数据并返回自增主键值，出参：值
#       使用方法: sql.insertGetId({'id':1,'name':'你好'})
#   insertAll   入参：数组<字典>，同 insert 的数组版，出参：变更数量
#       使用方法: sql.insertAll([{'id':1,'name':'你好'}])
#   update  入参：字典，根据条件更新数据，出参：变更数量
#       使用方法: sql.update({'name':'你好'})
#   setOption 入参：字段名，变更值，根据条件更新数据，出参：变更数量
#       使用方法: sql.setOption('name','你好')
#   delete 根据条件删除数据，出参：变更数量
#       使用方法: sql.delete()
#   setInc 入参：字段名，数字(步仅值，默认为1)；字段值自增，出参：变更数量
#       使用方法: sql.setInc('num')
#       使用方法: sql.setInc('num',2)
#   setDec 入参：字段名，数字(步仅值，默认为1)；字段值自减，出参：变更数量
#       使用方法: sql.setDec('num')
#       使用方法: sql.setDec('num',2)
#   query 入参：数据库语句
#       使用方法: sql.query('delete from id=1')
#   clear 刷新传入数据
#       使用方法: sql.clear()


def format_field(val, mold):
    mold = str(mold).lower()
    if 'int' in mold:
        if val == '':
            return '0'
        return str(val)
    if 'decimal' in mold:
        if val == '':
            return '0'
        return str(val)
    if 'float' in mold:
        if val == '':
            return '0'
        return str(float(val))
    if 'double' in mold:
        if val == '':
            return '0'
        return str(float(val))
    if 'char' in mold:
        return format_val(val)
    if 'text' in mold:
        return format_val(val)
    if 'date' == mold:
        return format_val(str(val))
    if 'time' == mold:
        return format_val(str(val))
    if 'year' in mold:
        return format_val(str(val))
    if 'blob' in mold:
        return format_val(val)
    if 'datetime' == mold:
        return format_val(val)
    return format_val(val)


def format_val(val):
    types = typeof(val)
    if val is None:
        return 'null'
    if types == 'str':
        return "'%s'" % str(val).replace('\\', '').replace('\'', '"')
    if types == 'int':
        return "%s" % val
    if types == 'double':
        return "%s" % val
    return "'%s'" % str(val).replace('\\', '').replace('\'', '"')


def typeof(variate):
    mold = None
    if isinstance(variate, int):
        mold = "int"
    elif isinstance(variate, str):
        mold = "str"
    elif isinstance(variate, float):
        mold = "float"
    elif isinstance(variate, list):
        mold = "list"
    elif isinstance(variate, tuple):
        mold = "tuple"
    elif isinstance(variate, dict):
        mold = "dict"
    elif isinstance(variate, set):
        mold = "set"
    return mold


class Db(object):
    __conn = None
    __map = []
    __name = ''
    __column = '*'
    __alias = ''
    __join = []
    __having = []
    __distinct = False
    __option = {}
    __build = False

    def __init__(self):
        try:
            self.conf = configparser.ConfigParser()
            self.conf.read("config.ini", encoding="utf-8")
            self.host = self.conf.get("mysql", "HOST")
            self.username = self.conf.get("mysql", "USER")
            self.password = self.conf.get("mysql", "PASS")
            self.db = self.conf.get("mysql", "DB")
            self.charset = self.conf.get("mysql", "CHAR")
            self.port = int(self.conf.get("mysql", "PORT"))
            self.prefix = self.conf.get("mysql", "PREFIX")
        except Exception as e:
            self.host = HOST
            self.username = USER
            self.password = PASS
            self.db = DB
            self.charset = CHAR
            self.port = int(PORT)
            self.prefix = PREFIX



    def __connect(self):
        self.__conn = pymysql.connect(host=self.host, port=self.port, user=self.username, password=self.password,
                                      db=self.db, charset=self.charset)
        self.cursor = self.__conn.cursor()

    def __close(self):
        self.cursor.close()
        self.__conn.close()

    def table(self, table):
        self.clear()
        self.__name = self.prefix + table
        return self

    def name(self, table):
        self.clear()
        self.__name = self.prefix + table
        return self

    def where(self, where=None):
        if where is None:
            return self
        if typeof(where) == 'dict':
            self.__map.append({'key': where.get('key'), 'val': where.get('val'), 'type': where.get('type')})

        if typeof(where) == 'list':
            for item in where:
                self.where(item)
        if typeof(where) == 'str':
            self.__map.append(where)
        return self

    def whereRow(self, key, val, mark='='):
        return self.where({'key': key, 'val': val, 'type': mark})

    def whereIn(self, key, val):
        if typeof(val) == 'tuple':
            return self.where({'key': key, 'val': '(' + ','.join(val) + ')', 'type': 'in'})
        return self.where({'key': key, 'val': '(' + val + ')', 'type': 'in'})

    def whereLike(self, key, val):
        return self.where({'key': key, 'val': val, 'type': 'like'})

    def alias(self, name=''):
        self.__alias = name + ' '
        return self

    #   字段没处理明白，暂时禁用
    # def join(self, table, where, mold='inner'):
    # table = self.prefix + table
    # self.__join.append({'table': table, 'where': where, 'mold': mold})
    # return self
    #

    def limit(self, limit=1):
        self.__option['limit'] = format_val(limit)
        return self

    def order(self, order):
        self.__option['order'] = order
        return self

    def group(self, group):
        self.__option['group'] = group
        return self

    def field(self, field):
        self.__column = field
        return self

    def distinct(self, is_true=True):
        self.__distinct = is_true
        return self

    def having(self, where):
        self.__having.append(where)
        return self

    def __comQuerySql(self):
        if self.__name is None:
            return None

        column = self.__column
        if column == '*':
            column = self.__showColumn(True)

        sql = "select "
        if self.__distinct:
            sql += ' distinct '

        sql += str(column) + " from " + str(self.__name)

        if self.__alias != '':
            sql += ' ' + self.__alias

        if len(self.__join) > 0:
            if '*' in column:
                print('使用 join 必须指定字段名')
                exit(-1)
                return None
            for item in self.__join:
                sql += item['mold'] + ' join ' + item['table'] + ' on ' + item['where'] + ' '

        if len(self.__map) > 0:
            all_column = self.__showColumn()
            sql += ' where 1=1 '
            for item in self.__map:
                if typeof(item) == 'str':
                    sql += ' and ( ' + item + ' ) '
                elif typeof(item) == 'dict':
                    values = 'null'
                    for column in all_column:
                        if column['field'] == item.get('key'):
                            values = format_field(item.get('val'), column['type'])
                            break
                    sql += ' and ( ' + item.get('key') + ' ' + item.get('type') + ' ' + values + ' ) '

        if self.__option.get('group'):
            sql += ' group by ' + self.__option['group'] + ' '

        if len(self.__having) > 0:
            for item in self.__having:
                sql += ' ' + item

        if self.__option.get('order'):
            sql += ' order by ' + self.__option['order'] + ' '

        if self.__option.get('limit'):
            sql += ' limit ' + self.__option['limit']
        return sql

    def buildSql(self, build=True):
        column = self.__column

        if column == '*':
            column = self.__showColumn(True)
        self.__build = build
        return self

    def __getField(self, table=None):
        column = self.__column
        if '*' in column:
            column = self.__showColumn(True, table=table)

        return column

    # 接下来是数据库操作

    def find(self):

        column = self.__getField()
        sql = self.__comQuerySql()
        if self.__build:
            return sql
        if sql is None:
            return None
        result = None
        try:
            self.__connect()
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            self.__close()
        except Exception as e:
            print(sql)
            print(e)
            exit(-1)
        if result is None:
            return None
        data = {}
        for index, k in enumerate(column.split(',')):
            data[k] = result[index]
        return data

    def select(self):
        if self.__name is None:
            return

        column = self.__getField()

        sql = self.__comQuerySql()
        if self.__build:
            return sql
        if sql is None:
            return None
        result = None
        try:
            self.__connect()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.__close()
        except Exception as e:
            print(sql)
            print(e)
            exit(-1)
        if result is None:
            return None
        data = []
        sp = column.split(',')
        for index, item in enumerate(result):
            dicts = {}
            for index2, k in enumerate(sp):
                dicts[k] = result[index][index2]
            data.append(dicts)
        return data

    def get(self, vid):
        pk = self.__getPk()
        if pk is not None:
            self.whereRow(pk, vid)
        return self.find()

    def value(self, field):
        self.__column = field
        sql = self.__comQuerySql()
        if self.__build:
            return sql
        result = None
        try:
            self.__connect()
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            self.__close()
        except Exception as e:
            print(sql)
            print(e)
            exit(-1)
        if result is not None:
            return result[0]
        else:
            return None

    def count(self):
        return self.value('count(*)')

    def insert(self, data):
        all_column = self.__showColumn()
        fields = ''
        values = ''
        i = 0
        for key in data:
            for column in all_column:
                if column['field'] == key:
                    if i == 0:
                        fields = key
                        values = format_field(data[key], column['type'])
                    else:
                        fields += ',' + key
                        values += ',' + format_field(data[key], column['type'])
                    i += 1
        if fields == '' or values == '':
            return 0
        sql = str(" insert into " + self.__name + " ( " + fields + ") values ( " + values + " ) ")

        return self.__edit(sql)

    def update(self, data):
        if typeof(data) != 'dict':
            return None
        all_column = self.__showColumn()
        fields = ''
        i = 0
        sql = ''
        if len(self.__map) > 0:
            sql += ' where 1=1 '
            for item in self.__map:
                if typeof(item) == 'str':
                    sql += ' and ( ' + item + ' ) '
                elif typeof(item) == 'dict':
                    values = 'null'
                    for column in all_column:
                        if column['field'] == item.get('key'):
                            values = format_field(item.get('val'), column['type'])
                            break
                    sql += ' and ( ' + item.get('key') + ' ' + item.get('type') + ' ' + values + ' ) '
        else:
            print('禁止不使用 where 更新数据')
        for key in data:
            for column in all_column:
                if column['field'] == key:
                    if i == 0:
                        fields = key + '=' + format_field(data[key], column['type'])
                    else:
                        fields += str(',' + key + '=' + format_field(data[key], column['type']))
                    i += 1
        if fields == '':
            return 0
        sql = str("update " + self.__name + " set " + fields + ' ' + sql)
        return self.__edit(sql)

    def insertGetId(self, data):
        if typeof(data) != 'dict':
            return None
        all_column = self.__showColumn()
        fields = ''
        values = ''
        i = 0
        for key in data:
            for column in all_column:
                if column['field'] == key:
                    if i == 0:
                        fields = key
                        values = format_field(data[key], column['type'])
                    else:
                        fields += ',' + key
                        values += ',' + format_field(data[key], column['type'])
                    i += 1
        if fields == '' or values == '':
            return 0
        sql = str(" insert into " + self.__name + " ( " + fields + ") values ( " + values + " ) ")
        pk = 0
        try:
            self.__connect()
            self.cursor.execute(sql)
            pk = self.__conn.insert_id()
            self.__close()
        except Exception as e:
            self.__conn.rollback()
        return pk

    def setOption(self, key, val):
        return self.update({key: val})

    def insertAll(self, datas):
        if typeof(datas) != 'list':
            return None
        count = 0
        for data in datas:
            count += self.insert(data)
        return count

    def delete(self):
        i = 0
        sql = ''
        if len(self.__map) > 0:
            sql += ' where 1=1 '
            for item in self.__map:
                if typeof(item) == 'str':
                    sql += ' and ( ' + item + ' ) '
                elif typeof(item) == 'dict':
                    sql += ' and ( ' + item.get('key') + ' ' + item.get('type') + ' ' + str(item.get('val')) + ' ) '
        else:
            print('禁止不使用 where 删除数据')
        sql = str("delete from " + self.__name + sql)
        return self.__edit(sql)

    def setInc(self, key, step=1):
        return self.update({key: key + '+' + str(step)})

    def setDec(self, key, step=1):
        return self.update({key: key + '-' + str(step)})

    def query(self, sql):
        return self.__edit(sql)

    def __showColumn(self, is_str=False, table=None):
        if table is None:
            table = self.__name
        list_data = None
        sql = "SHOW FULL COLUMNS FROM " + table
        try:
            self.__connect()
            self.cursor.execute(sql)
            list_data = self.cursor.fetchall()
            self.__close()
            if is_str:
                return ','.join(list([item[0] for item in list_data]))
        except Exception as e:
            print(e)

        return list([{'field': item[0], 'type': item[1], 'key': item[4]} for item in list_data])

    def __getPk(self):
        fields = self.__showColumn()
        for field in fields:
            if field['key'] == 'PRI':
                return field['field']
        return None

    def __edit(self, sql):
        if self.__build:
            return sql
        count = 0
        try:
            self.__connect()
            count = self.cursor.execute(sql)
            self.__conn.commit()
            self.__close()
        except Exception as e:
            self.__conn.rollback()
            print('Error:  ', sql)
            print(e)
        return count

    def clear(self):
        self.__map = []
        self.__name = ''
        self.__column = '*'
        self.__alias = ''
        self.__join = []
        self.__having = []
        self.__distinct = False
        self.__option = {}

#    前置操作
      pip install pymysql
      pip install configparser
#    使用方法
##   方法一：要么在目录下建名称为config.ini的文件，然后写入
      [mysql]
      HOST = 127.0.0.1
      USER = root
      PASS = 123456
      CHAR = utf8
      DB = bigsoft
      PORT = 3306
      PREFIX =
##    方法二：要么直接改如下参数，方式一调用失败会使用下面参数

      HOST = '127.0.0.1'  # 链接地址
      USER = 'root'  # 数据库用户
      PASS = '123456'  # 数据库密码
      CHAR = 'utf8'  # 编码格式
      DB = 'bigsoft'  # 数据库名称
      PORT = 3306     # 数据库端口号
      PREFIX = ''  # 表前缀

#    实例化类 sql = Db()
#   参数类：
##   table方法：入参：表名
      使用方法: sql.table('test')
##   where方法：可多次调用，入参：字符串或字典(key:字段名,val:值,type:对应关系,默认为'=')或数组
      使用方法: sql.where('id=1')
      使用方法: sql.where({'id',1})
      使用方法: sql.where({'id',1,'<>'})
      使用方法: sql.where({'id','(1,2)','in'})
      使用方法: sql.where([{'id','(1,2)','in'},{'name','%我%','like'}])
##   whereRow方法:可多次调用，入参：字段名,值,对应关系
      使用方法: sql.whereRow('id',1)
      使用方法: sql.whereRow('id',1,'>')
##   whereIn方法:可多次调用，入参：字段名,值(逗号拼接的字符串或元组)
      使用方法: sql.whereIn('id','1,2')
      使用方法: sql.whereIn('id',(1,2))
##   whereLike方法:可多次调用，入参：字段名,值
      使用方法: sql.whereLike('name','%我%')
##   alias方法:对 table 方法的表名设置 别名
      使用方法: sql.table('test').alias('a')
##   limit方法：查询前N条数据，入参：数量
      使用方法: sql.limit(10)
##   order方法：排序，入参：排序字符串
      使用方法: sql.order('id desc')
##   group方法:分组，入参：字符串
      使用方法: sql.group('name,title')
##   field方法：查询字段,入参：字符串
      使用方法: sql.field('id,name,title,create_time')
##   distinct方法：去重，入参：True或False，默认为True
      使用方法: sql.distinct()
##   having方法：入参：字符串
      使用方法: sql.having('b.id=1')

#   操作类：
##   buildSql    返回select查询语句，出参：字符串
      使用方法: sql.buildSql()
##   find    返回符合条件的第一条数据，出参：字典
      使用方法: sql.find()
##   count   返回符合条件的数量：出参：Int
      使用方法: sql.count()
##   value   入参：字段名，返回符合条件的一个字段的值，出参：值
      使用方法: sql.value('name')
##   select  返回符合条件的多数据，出参：数组<字典>
      使用方法: sql.select()
##   get 入参：值，识别主键返回符合条件的第一条数据，出参：字典
      使用方法: sql.get(2)
##   insert  入参：字典,字段识别后根据键名插入数据,自动剔除表中没有的字段，出参：变更数量
      使用方法: sql.insert({'id':1,'name':'你好'})
##   insertGetId 入参：字典,字段识别后根据键名插入数据并返回自增主键值，出参：值
      使用方法: sql.insertGetId({'id':1,'name':'你好'})
##   insertAll   入参：数组<字典>，同 insert 的数组版，出参：变更数量
      使用方法: sql.insertAll([{'id':1,'name':'你好'}])
##   update  入参：字典，根据条件更新数据，出参：变更数量
      使用方法: sql.update({'name':'你好'})
##   setOption 入参：字段名，变更值，根据条件更新数据，出参：变更数量
      使用方法: sql.setOption('name','你好')
##   delete 根据条件删除数据，出参：变更数量
      使用方法: sql.delete()
##   setInc 入参：字段名，数字(步仅值，默认为1)；字段值自增，出参：变更数量
      使用方法: sql.setInc('num')
      使用方法: sql.setInc('num',2)
##   setDec 入参：字段名，数字(步仅值，默认为1)；字段值自减，出参：变更数量
      使用方法: sql.setDec('num')
      使用方法: sql.setDec('num',2)
##   query 入参：数据库语句
      使用方法: sql.query('delete from id=1')
##   clear 刷新传入数据
      使用方法: sql.clear()

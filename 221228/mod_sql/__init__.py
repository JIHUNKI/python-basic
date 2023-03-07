import pymysql
import pandas as pd

class Database():
    def __init__(self, _host, _user, _pass):
        self._db = pymysql.connect(
            host = _host,
            user = _user,
            password = _pass,
            database= 'ubion',
            port = 3306
        ) 
        self.cursor = self._db.cursor(pymysql.cursors.DictCursor)
 ## select 쿼리문을 실행하는 경우 사용하는 함수
    def excuteAll(self, _sql, _values=[], _limit=0):
        self.cursor.execute(_sql,_values)
        self.result  = self.cursor.fetchall()
        if _limit !=0:
            self.df = pd.DataFrame(self.result).head(_limit)
        else:
            self.df = pd.DataFrame(self.result)

        return self.df
        
 ## select문을 제외한 데이터베이스의 내용을 삽입, 수정, 삭제하는 경우
    def execute(self, _sql, _values=[]):
        self.cursor.execute(_sql,_values)
        self.result = self.cursor.fetchall()
        return self.result

    def commit (self):
        self._db.commit()
        return ' commit complete'

## 모든 작업을 끝낸 후 데이터베이스와의 접속을 종료
    def  close (self):
        self._db.close()
        return 'Database close'
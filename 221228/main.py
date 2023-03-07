from flask import Flask, request
import mod_sql
import json

app = Flask(__name__)
db = mod_sql.Database("172.16.12.149",'ubion','1234')

@app.route('/corona')  # localhost:8080/corona 사이트 접속시 아래의 함수를 실행
def corona():
    _id = request.args.get('id')
    _pass = request.args.get('password')
    print(_id,_pass)
    login_sql = """ 
        select * from user_list where `id`= %s and `psssword` = %s
    """
    check = db.execute(login_sql,[_id,_pass])
    ## 로그인 성공시 check -> [{id:xxx, password:xxxx}]
    ## 로그인 실패시 check -> ()
    if check:
        sql = """
            select * 
            from corona
            """
        result = db.execute(sql)    ## 데이터프레임형태가아닌 딕셔너리형태까지만 해서 보내겠다
        # print(result)
        return json.dumps(result)  ## 딕셔너리형태를 json형태로 변경하여 보내겠다.
    else :
        return "login fail"
app.run(port=8080)  # host='0.0.0.0' 다른 사람들도 들어올 수 있게
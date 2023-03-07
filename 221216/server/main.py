from flask import Flask   ## Flask 는 class 

## Flask 라는 클래스 생성(파일의 이름)
## __name__ : 파일의 이름 (자기자신을 나타내는 함수)
app = Flask(__name__)

@app.route('/')   ## '/' request(요청)가 왔을때 아래에 있는 함수를 실행
def index():
    return "Hello"    ## user에게 response(응답)

app.run()


## cmd 창에서 cd C:\ubion\221216\server 로 디렉토리를 바꿔준다. cd : change directory
## set FLASK_APP = main
## flask run
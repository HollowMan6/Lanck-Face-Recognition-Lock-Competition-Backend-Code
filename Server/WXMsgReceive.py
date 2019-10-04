

# 用于接收小程序的信息


# coding:utf-8
 
import json
from wsgiref.simple_server import make_server
import re
from socket import *
import sys

 
# 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
def application(environ, start_response):
    # 定义文件请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body
    
    request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))
    
    json_str = request_body.decode('utf-8') # byte 转 str
#    json_str = request_body
    json_str = re.sub('\'','\"', json_str) # 单引号转双引号, json.loads 必须使用双引号
    json_dict = json.loads(json_str) #（注意：key值必须双引号）
    print(json_dict)
    
    sock1 = socket(AF_INET, SOCK_STREAM)
    id = (sys.argv[1], 1022)
    sock1.connect(id)
    str1 = json_dict["Name"] + ',' + json_dict["CardID"]
    sock1.send(str1.encode("utf-8"))

    
    return [json.dumps(json_dict)]
 
 
if __name__ == "__main__":
    port = 8080
    httpd = make_server("0.0.0.0", port, application)
    print("serving http on port {0}...".format(str(port)))
    httpd.serve_forever()


import json

dic = {
    'status':'true',
    "resultMessage": "注册成功"
}

# dumps 将字典转换为json字符串
j = json.dumps(dic,indent=2,ensure_ascii=False)
print(f"{type(j)}:{j}")

# loads 将json字符串转换为字典
string = '{"status": "true", "resultMessage": "注册成功"}'
js = json.loads(string)
print(f'{type(js)}:{js}')

# dump json 数据写入文件
with open('data.json', 'w') as wf:
    json.dump(j, wf)
 
# load 文件中读取 json
with open('data.json', 'r', encoding='utf-8') as rf:
    data = json.load(rf)
    print(f'{type(data)}:{data}')
from flask import Flask
from flask import request
from flask import Response
import requests
from bs4 import BeautifulSoup as bs

 
TOKEN = "YourToken"
app = Flask(__name__)
 
def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    name_client = message['message']['chat']['first_name'] + ' ' + message['message']['chat']['last_name']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    print("name_client-->", name_client)
    return chat_id,txt,name_client
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 

def kqxs():
    r = requests.get('http://ketqua2.net')
    tree = bs(markup=r.text, features='html.parser')
    node = tree.find(name='div', attrs={'id':'rs_0_0'})
    
    return f"Giải đặc biệt kết quả xổ số miền Bắc: {node.text}"


def tel_send_kq(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    kq = kqxs()
    payload = {
                'chat_id': chat_id,
                'text': kq
                }
   
    r = requests.post(url,json=payload)
    return r


def weather():
    r = requests.get('https://thoitiet.vn/ha-noi')
    tree = bs(markup=r.text, features='html.parser')
    node1 = tree.find('span', attrs={'class': 'current-temperature'})
    node2 = tree.find(name='div', attrs={'class': 'overview-caption ml-3'})

    return node1.text + node2.text


def tel_send_wt(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    wt = weather()
    payload = {
                'chat_id': chat_id,
                'text': wt
                }
   
    r = requests.post(url,json=payload)
    return r


def tel_send_hi(chat_id, text, name_client):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text,
                'name_client': name_client
                }
   
    r = requests.post(url,json=payload)
    return r

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
       
        chat_id,txt, name_client = parse_message(msg)
        if txt == "/start":
            tel_send_hi(chat_id,"Xin chào " + name_client, name_client)
        elif txt == "help":
            tel_send_message(chat_id,
                '''Các tính năng chính:
            - Gõ 'kqxs' để biết kết quả giải đặc biệt XSKT miền Bắc kỳ mới nhất.
            - Gõ 'thời tiết' để biết thông tin thời tiết Hà Nội hiện tại. 
                ''')
        elif txt == "kqxs":
            tel_send_kq(chat_id)
        elif txt == "thời tiết":
            tel_send_wt(chat_id)   
        else:
            tel_send_message(chat_id,"Gõ 'help' để tìm hiểu thêm")
       
        return Response('OK', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)
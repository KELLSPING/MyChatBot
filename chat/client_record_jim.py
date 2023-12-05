from tkinter import *
from datetime import *
from socket import *
import threading
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import os

import speech_recognition as sr
import time

from googletrans import Translator

from tkinter import ttk


from gtts import gTTS
from pygame import mixer
import tempfile

# generate WAV
import pyaudio
import wave

#image
import base64
import eel

tempMsg = ''
tempAudio = 0

language_list = ['en','ja','zh-tw','zh-cn','ko','es']

class Recorder:
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    def start(self):
        threading._start_new_thread(self.__recording, ())

    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while self._running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self._running = False

    def save(self):

        p = pyaudio.PyAudio()

        wf = wave.open("tmp.wav", 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()



language = 'en'
def set_language():
    global language
    language = language_list[box.current()]
    language_window.destroy()


def speak(sentence, lang, loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp: 
        if len(sentence.replace(' ',''))!=0:
            tts=gTTS(text=sentence, lang=lang)
            tts.save('{}.mp3'.format(fp.name))
            mixer.init()
            mixer.music.load('{}.mp3'.format(fp.name))
            mixer.music.play(loops)
        else:
            print('empty sentence.')

def get_ip():
    tmp_s = socket(AF_INET, SOCK_DGRAM)
    tmp_s.connect(("8.8.8.8", 80))
    ip = tmp_s.getsockname()[0]
    tmp_s.close()
    return ip

def scan_chatroom():
    global s
    ip = get_ip()
    chatroom_ip_list = []
    for x in range(0,255):
        s = socket()
        tmp_ip = ip.split('.')[0]+'.'+ip.split('.')[1]+'.'+ip.split('.')[2]+'.'+str(x)
        try:
            s.settimeout(5)
            #s.connect((tmp_ip,9999))
            #Only for test ChromeOS
            tmp_ip = '192.168.0.121'
            s.connect((tmp_ip,3388))
            #print('~~~~~'+tmp_ip+'~~~~')
            return tmp_ip
        except Exception as e:
            s.close()
# 登录窗口
def Login_gui_run():                                            

    def login_in():                                             # 登录函数（检查用户名是否为空，以及长度）
        name = nickname.get()                                   # 长度是考虑用户列表那边能否完整显示
        if not name:
            tkinter.messagebox.showwarning('Warning', message=login_warning_message1)
        elif len(name)>10:
            tkinter.messagebox.showwarning('Warning', message=login_warning_message2)
        else:
            root.destroy()
            #s.connect(('127.1.1.1', 30000))                     # 建立连接
            #s.connect(('192.168.86.43', 9999))                     # 建立连接
            chatroom_ip = scan_chatroom()
            if chatroom_ip !=None:

                s.settimeout(60) 
                print('chatroom_ip:'+ chatroom_ip)
                #s.connect((chatroom_ip,9999))
                s.send(nickname.get().encode('utf-8'))              # 传递用户昵称
                Chat_gui_run()                                      # 打开聊天窗口
            else:
                print('Not found chatroom')
                return 
 
    root = Tk()
    
    root.title(login_window_title)          # 窗口标题
    frm = Frame(root)
 
    root.geometry('300x150')                # 窗口大小
 
    nickname = StringVar()                                      # 昵称变量

 
    # 登录按钮、输入提示标签、输入框
    Button(root, text = login_window_button_login, command = login_in, width = 8, height = 1).place(x=100, y=90, width=100, height=35)
    Label(root, text=login_window_label_hint1, font=('Fangsong',12)).place(x=10, y=20, height=50, width=80)
    Entry(root, textvariable = nickname, font=('Fangsong', 11)).place(x=100, y=30, height=30, width=180)
    root.mainloop()


# 聊天窗口
def Chat_gui_run():
    eel.init('web')
    user_list = []
    user_list = s.recv(2048).decode('utf-8').split(',')     # 从服务器端获取当前用户列表
    user_list.insert(0, chat_window_label_userlist)                             
    
    nickname = user_list[len(user_list)-1]                  # 获取正式昵称，经过了服务器端的查重修改
    
    def close_callback(route, websockets):
        if not websockets:
            print('Bye!')
            line = '****LEAVE****'
            s.send(line.encode('utf-8'))
            os._exit(0)
        
    @eel.expose
    def get_message(message):
        global tempMsg
        tempMsg = message
        s.send(tempMsg.encode('utf-8'))
        #return f'eel get_message : {tempMsg}'

    
    def read_server(s):
        while True:
            try:
                content = s.recv(2048).decode('utf-8')                      # 接收服务器端发来的消息
            except:
                print('joel error meet expected')
                continue
            print(content)
            user_name = content.split(':')[0]
            info_txt = content.replace(user_name+':','')
            if user_name == '**System Info**':
                translator = Translator()
                name = info_txt.replace(' join the chatroom!','').replace(' leave the chatroom!','')
                info_txt = info_txt.replace(name,'')
                print('before')
                print(info_txt)
                print(language)
                translation = translator.translate(info_txt, dest=language)
                info_txt = name+translation.text
                print('here')
                print(info_txt)

            elif user_name != nickname :
                translator = Translator()
                translation = translator.translate(info_txt, dest=language)
                info_txt = translation.text
            curtime = datetime.now().strftime(ISOTIMEFORMAT)
            eel.update('['+str(curtime)+']'+' '+user_name+':'+info_txt)
            #here gtts
            if user_name != nickname :
                speak(info_txt,language)
 
    threading.Thread(target = read_server, args = (s,)).start()
    
    re = Recorder()
    
    def recordtext():
        global r,mic
        with sr.WavFile("tmp.wav") as source:    #read WAV files
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            try:
                text = r.recognize_google(audio,language = language)
                print(text)
                return text
            except :
                print ("Could not understand audio")

    @eel.expose
    def on_press():
        print("button was pressed")
        re.start()
    
    @eel.expose
    def on_release():
        print("button was released")
        re.stop()
        re.save()
        t=recordtext()
        eel.showText(t)

    
    eel.start('chat.html',size=(800, 600),close_callback=close_callback)



if __name__ ==  '__main__':
    s=''
    r=''
    mic=''
    r = sr.Recognizer()
    mic = sr.Microphone()
    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'         # 时间格式声明
    s = socket()                                # 套接字

    def closeWindow():
        language_window.destroy()
        os._exit(0)

    language_window = Tk()
    language_window.protocol('WM_DELETE_WINDOW', closeWindow)
    language_window.title('Language Select')
    language_window.geometry('300x100')
    
    box = ttk.Combobox(language_window, values= language_list)
    box.pack()
    box.current(0)
    ttk.Button(language_window, text="Confirm", command=set_language).pack()
    language_window.mainloop()
    
    print(language)
    if language =='en':
        login_warning_message1 = 'User name is empty!'
        login_warning_message2 = 'Too long, please in 10 characters.'
        login_window_title = 'ChatRoom*Login'
        login_window_button_login = 'Login'
        login_window_label_hint1 = 'Name:'
        login_window_label_close = 'Are you sure you want to leave?'
        chat_window_label_userlist = '------User list------'
        chat_window_title = 'ChatRoom--'
        chat_window_button_send = 'SEND'
        chat_window_button_say = 'Say'
    elif language =='es':
        login_warning_message1 = '¡El nombre de usuario está vacío!'
        login_warning_message2 = '¡El nombre de usuario es demasiado largo! Máximo 10 caracteres'
        login_window_title = 'Sala de chat*Iniciar sesión'
        login_window_button_login = 'Acceso'
        login_window_label_hint1 = 'Nombre:'
        login_window_label_close = 'Estás seguro que quieres irte?'
        chat_window_label_userlist = '----Lista de salas de chat----'
        chat_window_title = 'sala de chatm--'
        chat_window_button_send = 'enviar'
        chat_window_button_say = 'Say'
    
    elif language =='zh-tw':
        login_warning_message1 = '用戶名為空！'
        login_warning_message2 = '用戶明過長！最多10個字符'
        login_window_title = '聊天系統*登錄'
        login_window_button_login = '登錄'
        login_window_label_hint1 = '使用者名稱'
        login_window_label_close =  '確定要離開？'
        chat_window_label_userlist = '----聊天室名單----'
        chat_window_title = '聊天室--'
        chat_window_button_send ='發送'
    
        chat_window_button_say = 'Say'
    elif language =='ko':
        login_warning_message1 = '사용자 이름이 비어 있습니다!'
        login_warning_message2 = '사용자 이름이 너무 깁니다! 최대 10자'
        login_window_title = '채팅 시스템*로그인'
        login_window_button_login = '로그인'
        login_window_label_hint1 = '사용자 이름'
        login_window_label_close =  '정말 떠나시겠어요?'
        chat_window_label_userlist = '----채팅방 목록----'
        chat_window_title = '대화방--'
        chat_window_button_send ='보내다'
    
        chat_window_button_say = 'Say'
    
    elif language =='zh-cn':
        login_warning_message1 = '用户名为空！'
        login_warning_message2 = '用户名过长！最多为十个字符！'
        login_window_title = '聊天系统*登录'
        login_window_button_login = '登录'
        login_window_label_hint1 = '请输入昵称'
        login_window_label_close =  '确定要离开?'
        chat_window_label_userlist = '聊天室清单'
        chat_window_title = '聊天室--'
        chat_window_button_send ='发 送'
        chat_window_button_say = 'Say'
    elif language =='ja':
        login_warning_message1 = 'ユーザー名が空です！'
        login_warning_message2 = 'ユーザー名が長すぎます!最大10文字！'
        login_window_title = 'チャットシステム*ログイン'
        login_window_button_login = 'ログイン'
        login_window_label_hint1 = 'ユーザー名'
        login_window_label_close =  '本当に退会してもよろしいですか?'
        chat_window_label_userlist = '--チャットルーム一覧--'
        chat_window_title = 'チャットシステム--'
        chat_window_button_send ='送 信'
    
        chat_window_button_say = 'Say'
    else:
        login_warning_message1 = 'User name is empty!'
        login_warning_message2 = 'Too long, please in 10 characters.'
        login_window_title = 'ChatRoom*Login'
        login_window_button_login = 'Login'
        login_window_label_hint1 = 'Name:'
        login_window_label_close = 'Are you sure you want to exit?'
        chat_window_label_userlist = '------User list------'
        chat_window_title = 'ChatRoom--'
        chat_window_button_send = 'SEND'
        chat_window_button_say = 'Say'
    


    Login_gui_run()

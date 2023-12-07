from tkinter import *
from datetime import *
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
import json
import random

tempMsg = ''
tempAudio = 0

language_list = ['en','ja','zh-tw','zh-cn','ko','es']

import firebase_admin
from firebase_admin import credentials

j_str = {"type": "service_account",
  "project_id": "pythonfirebase-6b43c",
  "private_key_id": "d0eedb26e201720f1f24fd9487fb369265da6ca8",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCz1IqYXM4TGam8\n/NPsUbatzupN2UId//4u9pb9Cm5ljCUFCf1IlHA3e4hHFwpuCOn3iqlVnbJhw0q+\nornJuW8eOvE+bpaXS6Rplym3en84N4E/Phwb8vcda/H3naaoHTM0S/BkusX0SuMe\ngVzCcuXIqz6Oa6t67t97bck/pwkPYMofX6Oo8yNCUszCkDwVewoG86iJqIrlwbfh\n2qL7kbHfa2C87mt9/PorB9RprBsrXqNVGp9n07Csy0E6Hlu6dnm/F9JWSTYWB3xF\nmJmOKcXpYWCf5Tfel/H/VkGoL4znloDixgNoko00WV3i83ubq8qOa/JGdiTycYGX\nQgOfn7cNAgMBAAECgf8Z45b1bJzSiCzChQ9OQ8YnONv1AZjXYTyRtW5sVwoAL4EX\nZGmchfgbEjEdM1kGTy4BaxoJ+VyCbHYPiVcGxGt0ITddQjbr2zf1THLnjtKtraDP\nfWGVU6U5Gn0IwH26URuKq91YUjpqD13tRlrUUsp32TzhjiweaEwOTShQ94HnPrlU\nCglPtvmhbOdyx1ZsfAl+1q3mc9e6S29lGehCXrcm/hzO3ZMW2/5zD/UWH1DksWCV\n2dyXGbZOi04//OMMwj56M25v8p1FYT8kCLmjYiZnB4V9wYJ7yCMU9GIgZKPeHMDk\nRrRv17Vhbqnpvw2C6W9wmpvdV2tNUanO0DDGBQECgYEA2mEs2hWvXPhEpWCYhoOu\nP0oYrO0vcgv8B0SP7LIBEAbHx17IC3Tyzemgfw6QWIwa/zFlBlv1/MaMD+eiOHXW\nJCfsmfNLypEvtkUJdi22jLJ1QEynOKHfNgSQquvY0n9GjRdH/vsHw/SSxquER/GP\nvoHiblSanJGYgDT/9M4vNg0CgYEA0s9KHpsd9Q/Lvg63TLQHjqWXJC1s5j65f/RS\nkz8jrmU5HHFncRMYZp1SmAwLtnL3jEWVy1tHLOl+TBGoPspsZAk/abHKViqs4KNN\n/Ye6Py4ujSA8b9Gu2UJt6G2lZVWmk7W3eX0GKn9qJ9+t9C6yToS5byRhAqyyfomh\nNlabRQECgYEAiq8z4LvsxkoUrkIOGz79JcxUp11pyC+8OpFcJaFV82ua7A5RVJVM\nrWA1QPtqyBESBAbGdadpLMKaqG8eImUTPZrtM0fDVj2l40csnxSg3fFnbRJBEEIc\nkx2LEkD9TZDuqSOj4VZitBtaKzk5pMbP1th9iDvKhKwiASmnczyN1vECgYAJ7gew\nv1++3lqbfjf2HfjJKFWhN56MjeHQ/CIzm2LD4TK6e0EDG4InuztbvB2FH483hUOU\nC52jqO/xB1fkdUZ7w8+/28cLHgF8p1SSH6WPOk6pCR6vqbHRvAZPT3Ld/hXVmVam\nG1SCBfRrImcgPF7bwfa2HIGRTa8utK7qT1QLAQKBgQC3dDf6lwDAXquXT/1PLm8r\nhy4urSMuPVN74vpntiTUvy0OOVOW2bMyP38l00hqwkjE7ifGoV2g17HbmsNj44Xc\nrVL5gxj8E3BHcO272ExxgcdmaiJ3l7TqmyekIrSFEIEKIIivAHc92dDxs0o2fjvb\n5+u18iN+tiMt/5qLAaVTBA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-k2nly@pythonfirebase-6b43c.iam.gserviceaccount.com",
  "client_id": "101784948027192725809",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-k2nly%40pythonfirebase-6b43c.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com" 
}
with open("./key.json","w") as f:
    json.dump(j_str,f)
 
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)


# 用來存放資料
from firebase_admin import firestore
db = firestore.client()

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    global language,name
    for change in changes:
        
        if change.type.name == 'ADDED':
            content = '[ **System Info** ]: '+u'{} join the chatroom'.format(change.document.id)
        elif change.type.name == 'MODIFIED':
            data = db.collection('chatroom').document(change.document.id).get().to_dict()
            content = u'{} : {}'.format(change.document.id,data['message'])
        elif change.type.name == 'REMOVED':
            content = '[ **System Info** ]: '+u'{} leave the chatroom'.format(change.document.id)
            #Add close browser window call js function here
            
            if name.strip() == change.document.id :
                eel.close_browser()


        user_name = content.split(':')[0]
        info_txt = content.replace(user_name+':','')
        if user_name == '[ **System Info** ]':
            translator = Translator()
            join_name = info_txt.replace(' join the chatroom!','').replace(' leave the chatroom!','')
            info_txt = info_txt.replace(join_name,'')
            translation = translator.translate(info_txt, dest=language)
            info_txt = join_name+translation.text

        elif user_name.strip() != name :
            translator = Translator()
            translation = translator.translate(info_txt, dest=language)
            info_txt = translation.text

        curtime = datetime.now().strftime(ISOTIMEFORMAT)
        eel.update('['+str(curtime)+']'+' '+user_name+':'+info_txt)
        print('['+str(curtime)+']'+' '+user_name+':'+info_txt)

        #here gtts
        if (user_name.strip() != name) and (user_name != '[ **System Info** ]' ) :
            speak(info_txt,language)

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


def validate_name(name):
        flag = False 
        lst_id=[i.id for i in db.collection('chatroom').get()]
        for i in lst_id:
            if i ==name:
                flag = True

        return flag
     
# 聊天窗口
def Chat_gui_run():
    eel.init('web')
    
    def close_callback(route, websockets):
        global name
        if not websockets:
            print('Bye!')
            line = '****LEAVE****'
            student1 = db.collection('chatroom').document(name).delete()
            time.sleep(2)
            os._exit(0)

    def validate_name(name):
        flag = False 
        lst_id=[i.id for i in db.collection('chatroom').get()]
        for i in lst_id:
            if i ==name:
                flag = True

        return flag
                
    @eel.expose
    def get_message(message):
        global tempMsg,name
        tempMsg = message
        #return f'eel get_message : {tempMsg}'

        if tempMsg=='sudo_clean_all_users':
            lst_id=[i.id for i in db.collection('chatroom').get()]
            for i in lst_id:
                if i!=name:
                    db.collection('chatroom').document(i).delete()
        else:
            loc_dt =datetime.today()

            student1 = db.collection('chatroom').document(name)
            student1.set({
                'message': tempMsg,
                'time':loc_dt.strftime("%Y:%m:%d:%H:%M:%S")
            })

    def read_server():
        #col_query = db.collection(u'cities').where(u'state', u'==', u'CA')
        col_query = db.collection(u'chatroom')
        # Watch the collection query
        query_watch = col_query.on_snapshot(on_snapshot) 
 
    threading.Thread(target = read_server).start()
    
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

    port = random.randint(5000,65535) 
    eel.start('chat.html',size=(800,600),port = port,mode = 'chrome-app',close_callback=close_callback)


if __name__ ==  '__main__':
    r = sr.Recognizer()
    mic = sr.Microphone()
    #ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'         # 时间格式声明
    ISOTIMEFORMAT = '%Y-%m-%d %H:%M'

    def closeWindow():
        language_window.destroy()
        os._exit(0)

    def set_up():
        global language,nickname,name
        language = language_list[box.current()]
        name = nickname.get()
        if not name:
            tkinter.messagebox.showwarning('Warning', message='User name is empty!')
        elif len(name)>10:
            tkinter.messagebox.showwarning('Warning', message='Too long, please in 10 characters.')
        elif validate_name(name):
            tkinter.messagebox.showwarning('Warning', message='Name was used, please changed.')
        else:

            #Joel here join firebase
            loc_dt =datetime.today()
            student1 = db.collection('chatroom').document(name)
            student1.set({
                'message': 'Join the chatroom',
                'time':loc_dt.strftime("%Y:%m:%d:%H:%M:%S")
            })
            language_window.destroy()
            Chat_gui_run()
                
    language_window = Tk()
    language_window.protocol('WM_DELETE_WINDOW', closeWindow)
    language_window.title('User Setup')
    language_window.geometry('600x250')
    
    ttk.Label(language_window, text='Language', font=('Fangsong',16)).pack()

    box = ttk.Combobox(language_window, font=('Fangsong',16),values= language_list)
    box.pack()
    box.current(0)
    
    nickname = StringVar()
    ttk.Label(language_window, text='Name', font=('Fangsong',16)).pack()
    ttk.Entry(language_window, textvariable = nickname, font=('Fangsong', 16)).pack()
    """
    Label(language_window, text='Name', font=('Fangsong',12)).place(x=20, y=40, height=50, width=80)
    Entry(language_window, textvariable = nickname, font=('Fangsong', 11)).place(x=150, y=60, height=30, width=180)
    """
    
    ttk.Button(language_window, text="Confirm",command=set_up).pack()
    

    language_window.mainloop()

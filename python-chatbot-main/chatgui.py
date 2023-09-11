#encoding utf-8
import nltk, json, random, pickle
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import tkinter
from tkinter import *

from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
from datetime import datetime
fecha = datetime.now()
# preprocessamento input utente
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words



# crear bag of words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))






def calcula_pred(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def obtenerRespuesta(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result =random.choice(i['responses'])
            break
    return result

    


def inicia(msg):
    ints = calcula_pred(msg, model)
    res = obtenerRespuesta(ints, intents)
    return res

#Creating GUI with tkinter
def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "Yo: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        res = inicia(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.insert(exec(state_prediction.py))
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
base = Tk()
base.title("Dr Chatbot")
base.geometry("800x600")
base.resizable(width=TRUE, height=TRUE)
#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)
#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff', command= send )
#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)
#Place all components on the screen
scrollbar.place(x=705,y=6, height=386)
ChatLog.place(x=6,y=6, height=300, width=700)
EntryBox.place(x=128, y=401, height=90, width=500)
SendButton.place(x=6, y=401, height=90)
base.mainloop()

usuario = ''
print('Bienvenido! Para Salir, Escribir "SALIR"')

while usuario != 'SALIR':
    usuario = str(input(""))
    res = inicia(usuario)
    print('AI:' + res)
    exec(state_prediction.py)
    


"""
@author: demoven
"""

from tkinter import Tk, Label, Entry, Button, RIGHT, TOP
import avaliarString as avaliar
import pyodbc
from collections import defaultdict

def teste(a):
    flagNaoSabe = False
    flagEncontrouCerteza = False
    flagEncontrouQuase = False 
    a = a.lower()
    for item in perguntas.items():
        if(flagEncontrouCerteza):
            break
        else:
            if(flagEncontrouQuase):
                break
        for perg in item[1]:
            metodo1 = avaliar.levenshtein(a, perg)
            metodo2 = avaliar.fuzz.token_sort_ratio(a, perg)
            metodo3 = avaliar.similar(a, perg) * 100
            if(metodo2>95):
                indice = item[0]
                flagEncontrouCerteza = True
                break
            else:
                if(metodo2>75 or metodo1<3 or metodo3>65):
                    indice = item[0]
                    flagEncontrouQuase = True;
                else:
                    if((metodo2>20 and metodo2<70) or metodo1>5 or (metodo3>35 and metodo3<60)):
                        indice = item[0]
                        flagNaoSabe = True
  
    if(flagEncontrouCerteza):
        flagEncontrouCerteza = False
        res = respostas[indice]
        return str(res[0])
    else:
        if(flagEncontrouQuase or flagNaoSabe):
            flagEncontrouQuase = False
            flagNaoSabe =  False
            res = respostas[indice]
            return str(res[0])
            

def perguntar(resposta, pergunta):
    resposta.config(state="normal")
    resposta.delete(0, 'end')
    x = pergunta.get()
    res = teste(x)
    resposta.insert(0,res)
    resposta.config(state="readonly")
    listaPerguntas.append(x)
    listaRespostas.append(res)
    
def corrigir(pergunta, resposta, ajuda):
     cursor.execute('SELECT max(ID) FROM Perguntas')
     idAtualPergunta = -1
     for row in cursor:
         idAtualPergunta = row[0]
    
     cursor.execute('SELECT max(ID) FROM Respostas')
     idAtualResposta = -1
     for row in cursor:
         idAtualResposta = row[0]
         
     res = ajuda.get()
     comandoSQL = 'INSERT INTO Respostas VALUES (' + str(idAtualResposta + 1) + ', \'' + res + '\');'
     cursor.execute(comandoSQL)
     respostas[idAtualResposta + 1].append(res)
     comandoSQL = 'INSERT INTO Perguntas VALUES (' + str(idAtualPergunta + 1) + ', ' + str(idAtualResposta + 1) + ', \'' + pergunta.get() + '\', ' + '0' + ');'
     cursor.execute(comandoSQL)
     db.commit()
     perguntas[idAtualResposta + 1].append(pergunta.get())
     ajuda.delete(0, 'end')
     resposta.config(state="normal")
     resposta.delete(0, 'end')
     resposta.insert(0,"Obrigado pela ajuda! Já aprendi algo novo")
     resposta.config(state="readonly")


    
def menu():
    def verHistorico(per, res):
        def voltar():
            hist.destroy()
            menu()
            
        root.destroy()
        hist = Tk()
        hist.title('Histórico')
        i = 0
        #cntRow = 0
        for item in per:
            Label(text='Voce:').grid(row=i+i)
            pergunta = Entry(hist, width=100)
            pergunta.grid(row=i+i, column=1)
            pergunta.config(state="normal")
            pergunta.insert(0, item)
            pergunta.config(state="readonly")
            
            Label(text='Bot:').grid(row=i+i+1)
            resposta = Entry(hist, width=100)
            resposta.grid(row=i+i+1, column=1)
            resposta.config(state="normal")
            resposta.insert(0, res[i])
            resposta.config(state="readonly")
            #cntRow+=2
            i+=1
        
        Button(hist, text='Voltar', command=voltar).grid(row=i+i+1, column=1)
        hist.mainloop()
    
        
        
    root = Tk()
    root.title('ChatBot - 2017')
    Label(text='Bem-vindo ao ChatBot! Falem a vontade e ajudem-nos melhorar!', font=(None, 16)).pack(side=TOP,padx=10,pady=10)
    Label(text='Elaborado por: Francisco Paulos, Tiago Lima e Vladimir Balayan', font=(None, 8)).pack(side=TOP,padx=10,pady=10)
    Label(text='Pergunta').pack(side=TOP)
    pergunta = Entry(root, width=100)
    pergunta.pack(side=TOP,padx=10,pady=10)
    Label(text='Resposta').pack(side=TOP)
    resposta = Entry(root, width=100, state="readonly")
    resposta.pack(side=TOP,padx=10,pady=10)
    Label(text='Se a resposta estiver errada, escreva aqui').pack(side=TOP)
    ajuda = Entry(root, width=100)
    ajuda.pack(side=TOP,padx=10,pady=10)
    Button(root, text='Perguntar', command= lambda: perguntar(resposta, pergunta)).pack(side=RIGHT, padx=10, pady=5)
    Button(root, text='Corrigir', command= lambda: corrigir(pergunta, resposta, ajuda)).pack(side=RIGHT,padx=10, pady=5)
    Button(root, text='Ver Histórico', command= lambda: verHistorico(listaPerguntas, listaRespostas)).pack(side=RIGHT,padx=10, pady=5)
          
    root.mainloop()

db = pyodbc.connect('DATABASE') #put here your database!!!
cursor = db.cursor()
cursor.execute('SELECT * FROM Perguntas') 
listaPerguntas = []
listaRespostas = []
perguntas = defaultdict(list)
for row in cursor:
    perguntas[row[1]].append(row[2])

cursor.execute('SELECT * FROM Respostas') 
respostas = defaultdict(list)
for row in cursor:
    respostas[row[0]].append(row[1])

menu()

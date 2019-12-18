from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import numpy as np
import cv2
import math

def criaArquivoLetras():
    s = ""
    validos = [[32, 126], [161, 187], [697, 832]]
    for i in range(len(validos)):
        for j in range(validos[i][0], validos[i][1]+1):
            s += chr(j)
    print(len(s))
    print(s)
    f = open("courier8.txt","w+")
    f.write(s)
    f.close()

def criaImgsAsc():
    numeroImagem = 59
    img1 = cv2.imread("courrier8c.png", cv2.IMREAD_GRAYSCALE)
    for i in range(0, img1.shape[1]-8, 8):
        imgF = np.ones((10, 8)).astype(np.uint8)
        for k in range(8):
            for kk in range(10):
                imgF[kk, k] = img1[kk, i+k]
        cv2.imwrite("ascImages/img"+str(numeroImagem)+".png", imgF)
        numeroImagem += 1
    
def criaAI(img):
    altO, lrgO = img.shape
    altF, lrgF = (altO//10)*10, (lrgO//8)*8
    imgF = np.ones((altF, lrgF)).astype(np.uint8)
    for i in range(0, altF, 10):
        print("Iteração =",i,"/",altF," |  +-",i/altF,"%")
        for j in range(0, lrgF, 8):
            eMin = 0
            idImg = 1
            for k in range(1,73):
                erro = 0
                imgA = cv2.imread("ascImages/img"+str(k)+".png", cv2.IMREAD_GRAYSCALE)   
                for ii in range(10):
                    for jj in range(8):                           
                        erro += abs(int(imgA[ii,jj]) - int(img[i+ii,j+jj]))
                             
                if k == 1:
                    eMin = erro
                    
                elif erro < eMin:
                    eMin = erro
                    idImg = k

            
            imgA = cv2.imread("ascImages/img"+str(idImg)+".png", cv2.IMREAD_GRAYSCALE)
            for ii in range(10):
                for jj in range(8):
                    imgF[i+ii, j+jj] = imgA[ii,jj]

    return imgF
    

func = {'eq': -1, 'db': 0}

def janela():
    window = Tk() 
    window.title("ASC-IMAGE PYTHON")
    window.minsize(width=650, height=350)
    window.maxsize(width=650, height=350)
    window.resizable(0,0)

    lblINUTIL = Label(window, text="")     
    lblINUTIL.grid(column=0, row=0, padx=10, pady = 20)
    
    lblIE = Label(window, text="Nome Imagem de Entrada:")     
    lblIE.grid(column=0, row=1, padx=10, pady = 20)
    entradaIE = Entry(window, width=8)
    entradaIE.grid(column=1, row=1, pady = 20, ipady = 8, ipadx = 200)
    

    lblIS = Label(window, text="Nome Imagem de Saída:")     
    lblIS.grid(column=0, row=3, padx=10, pady = 0)
    entradaIS = Entry(window, width=8)
    entradaIS.grid(column=1, row=3, pady = 0, ipady = 8, ipadx = 200)

    def ativaEq():
        global func
        func['eq'] *= -1
        if func['eq'] == -1:
            btnEq["text"]="Equalizar Desativado"
        else:
            btnEq["text"]="Equalizar Ativado"

    def ativaDb():
        global func
        func['db'] = (func['db']+1)%3
        if func['db'] == 0:
            btnDb["text"]="Dobrar Desativado"
        elif func['db'] == 1:
            btnDb["text"]="Dobrar Ativado"
        else:
            btnDb["text"]="Dobrar Ativado com Redução"

    btnEq = Button(window, text="Equalizar Desativado", command=ativaEq)
    btnEq.grid(column=1, row=4, pady = 25)
    
    btnDb = Button(window, text="Dobrar Desativado", command=ativaDb)
    btnDb.grid(column=1, row=5)

    def chamaErro(titulo="Erro", msg=""):
        messagebox.showerror(titulo, msg)
    
    def preparaImagem():
        global func
        img = cv2.imread(entradaIE.get(), cv2.IMREAD_GRAYSCALE) #LE COMO ESCALA DE CINZA
        
        if str(type(img)) != "<class 'NoneType'>":
            if len(entradaIS.get()) > 5 and entradaIS.get()[-3:] in ["png", "PNG", "jpg", "JPG", "bmp", "BMP", "peg", "PEG"]:

                if func['db'] >= 1: #DOBRA O TAMANHO
                    img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))

                if func['eq'] == 1: #EQUALIZA O HISTOGRAMA
                    img = cv2.equalizeHist(img)

                img = criaAI(img)

                if func['db'] == 2: #VOLTA AO TAMANHO ORIGINAL
                    img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))

                cv2.imwrite(entradaIS.get(), img)
                
                messagebox.showinfo('','TERMINOU PROCESSAMENTO COM SUCESSO')
                
            else:
                chamaErro("Erro", "Imagem de saída inválida")
        else:
            chamaErro("Erro", "Imagem de entrada inválida")
        
    btnOk = Button(window, text="OK", command=preparaImagem) 
    btnOk.grid(column=1, row=6, pady = 25)

    window.mainloop()

janela()

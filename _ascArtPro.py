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

    imgF = cv2.resize(imgF, (img.shape[1]//2, img.shape[0]//2))
    cv2.imwrite("ascImageFinal.png", imgF)

          
img = cv2.imread("23_luke4.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))
img = cv2.equalizeHist(img)
#res = np.hstack((img,equ)) #concatena horizontalmente
#cv2.imwrite('res2.png',equ)
criaAI(img)

'''
print("PIXEL IMG1[0,0]:"
print("PIXEL IMG1[1,0]:",img1[1,0])
print("PIXEL IMG1[0,1]:",img1[0,1])
print("PIXEL IMG1[1,1]:",img1[1,1])

img = np.load("imgF.npy")
print("PIXEL IMG[0,0]:",img[0,0])

img2 = cv2.imread("descompactada.bmp", cv2.COLOR_BGR2RGB)
print("PIXEL IMG2[0,0]:",img1[0,0])
print("PIXEL IMG2[1,0]:",img1[1,0])
print("PIXEL IMG2[0,1]:",img1[0,1])
print("PIXEL IMG2[1,1]:",img1[1,1])

img1 = cv2.imread("benchmark.bmp", cv2.COLOR_BGR2RGB) #cv2.IMREAD_COLOR) cv2.COLOR_BGR2HSV) cv2.COLOR_BGR2RGB) cv2.IMREAD_GRAYSCALE)
cv2.imwrite("COD_IMAGE.bmp", image)
np.save("m.npy", m)
m = np.load("m.npy")

matriz = np.load(url)
imgF = np.ones((1, 1, 3)).astype(np.uint8)
cv2.imwrite("descompactada.bmp", imgF)
'''

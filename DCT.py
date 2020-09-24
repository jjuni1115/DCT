from PIL import Image
import numpy as np
from matplotlib import pyplot as plot
import random
import math

N=8    #dct block size
M=8
block_size=8
def dct(forward,DCT,dir):                   #dct function
    global N
    global M
    temp = np.ones([N,M], dtype=int)   #dct block size
    accum=0.0

    if dir==1:                 #forward
        for k in range(0,N):
            for x in range(0,N):
                accum = 0.0
                for y in range(0,N):
                    accum+=(math.cos((math.pi*x*(2.0*y+1))/(2.0*N))*forward[y][k])
                    #accum*=scale
                if x==0:
                    accum*=1.0/math.sqrt(N)
                else:
                    accum*=math.sqrt(2/N)
                temp[x][k]=accum

        for k in range(0,N):
            for x in range(0,N):
                accum = 0.0
                for y in range(0,N):
                    accum+=(math.cos((math.pi*x*(2*y+1))/(2*N))*temp[k][y])
                    #accum*=scale
                if x == 0:
                    accum *= 1.0/math.sqrt(N)
                else:
                    accum *= math.sqrt(2 / N)
                DCT[x][k]=accum

    elif dir==-1:                  #inverse
        for k in range(0,N):
            for x in range(0,N):
                accum=0.0
                for y in range(0,N):
                    if y==0:
                        accum+=(math.cos((math.pi*y*(2*x+1))/(2*N))*forward[y][k])*math.sqrt(1.0/N)
                    else:
                        accum+=(math.cos((math.pi*y*(2*x+1))/(2*N))*forward[y][k])*math.sqrt(2.0/N)
                temp[x][k]=accum

        for k in range(0,N):
            for x in range(0,N):
                accum=0.0
                for y in range(0,N):
                    if y==0:
                        accum+=(math.cos((math.pi*y*(2*x+1))/(2*N))*temp[k][y])*math.sqrt(1.0/N)
                    else:
                        accum+=(math.cos((math.pi*y*(2*x+1))/(2*N))*temp[k][y])*math.sqrt(2.0/N)
                DCT[x][k]=accum

def mean_square_error(pixel,newpixel):    #mean square error function
    sum=0
    mse=0.0
    for i in range(0,512):
        for j in range(0,512):
            sum+=(newpixel[i][j]-pixel[i][j])**2
    mse=sum/(512*512)
    return mse




#loading raw file
infile=open("BOAT512.raw","rb")
image=np.fromfile(infile,dtype=np.uint8,count=512*512)
pixel=Image.frombuffer('L',[512,512],image,'raw','L',0,1)
pixel=np.array(pixel,dtype=int)  #행렬에 저장
dct_pixel=np.ones([512,512],dtype=int)

#forward dct function call
for i in range(0,512,N):
    for j in range(0,512,M):
        dct(pixel[i:i+N,j:j+M],dct_pixel[i:i+N,j:j+M],1)
#dct(pixel,dct_pixel,1)
print("DCT complete")

#show image
plot.imshow(dct_pixel,cmap='gray')
plot.show()

inv_pixel=np.ones([512,512],dtype=int)

#inverse dct funtion call
for i in range(0,512,N):
    for j in range(0,512,M):
        dct(dct_pixel[i:i+N,j:j+M],inv_pixel[i:i+N,j:j+M],-1)
#dct(dct_pixel,inv_pixel,-1)
print("inverse complete")
#show image
plot.imshow(inv_pixel,cmap='gray')
plot.show()
#mse
mse=mean_square_error(pixel,inv_pixel)
print("Mean-square-error: ",mse)





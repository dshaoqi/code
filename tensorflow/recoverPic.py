import os 
import struct
import numpy as np
import cv2 as cv
dirx='/home/dsq0/mypython/tensorflow/minist_data/'

filec={'TR-L':'train-labels.idx1-ubyte','TR-M':'train-images.idx3-ubyte',\
 'TE-L':'t10k-labels.idx1-ubyte','TE-M':'t10k-images.idx3-ubyte'}

#TR-L:train label file

#effect:  read the first 28*28 in train images set and zoom in to 200*200 ,then show 
# the pic , the result should be 5
 
def getContent():
  lab='TR-M'
  for i in filec:
    if i==lab :
       f=open(dirx+filec[i])
       con=f.read(8)
       x=list(struct.unpack('i',con[0:4][::-1]))
       x.append(struct.unpack('i',con[4:8][::-1])[0])
       
       if lab=='TR-L' or lab=='TE-L':
         while 1:
          del(con)
          con=f.read(1024)
          if len(con)==0 :
              break
          for i in range(0,len(con)):
             x.append(struct.unpack('B',con[i])[0])
       else:
          con=con+f.read(8)
          x.append(struct.unpack('i',con[8:12][::-1])[0])
          x.append(struct.unpack('i',con[12:16][::-1])[0])
          del(con)
          con=f.read(28*28)
          result=np.empty([28,28],dtype='uint8')
          for i in range(0,len(con)):
               result[i/28][i%28]=struct.unpack('B',con[i])[0]
         # resultx=np.empty([200,200],dtype='uint8')
          resultx=cv.resize(result,(200,200))
          cv.imshow('result',resultx)
          cv.waitKey(0)
      # print x
       f.close()
       return x
       
       


if __name__=='__main__':
   
   f1=getContent()
   



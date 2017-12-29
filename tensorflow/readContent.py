import os 
import struct

dirx='/home/dsq0/mypython/tensorflow/minist_data/'

filec={'TR-L':'train-labels.idx1-ubyte','TR-M':'train-images.idx3-ubyte',\
 'TE-L':'t10k-labels.idx1-ubyte','TE-M':'t10k-images.idx3-ubyte'}

#TR-L:train label file
 
def getContent(lab):
  for i in filec:
    if i==lab :
       f=open(dirx+filec[i])
       con=f.read()
       x=list(struct.unpack('i',con[0:4][::-1]))
       x.append(struct.unpack('i',con[4:8][::-1])[0])
       
       if lab=='TR-L' or lab=='TE-L':
          for i in range(8,len(con)):
             x.append(struct.unpack('B',con[i])[0])
       else:
          x.append(struct.unpack('i',con[8:12][::-1])[0])
          x.append(struct.unpack('i',con[12:16][::-1])[0])
          for i in range(16,len(con)):
             x.append(struct.unpack('B',con[i])[0])
   
       print x
       f.close()
       
       


if __name__=='__main__':
   f1=getContent('TR-M')
   



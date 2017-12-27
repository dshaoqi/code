#import setEnv
import sys
pathadd=['/home/dsq0/mypython/dsq','/home/dsq0/mypython/dsq/TensorLib']
for i in pathadd:
  sys.path.append(i)
import numpy as np
from TensorLib import tensor
from TensorLib import tools
import random


MAX_TIMES=1000

def unified_k3_m2(tensor_trans,tensor_begin):
  #conteract first 3 dim tensor_trans[6,7,8] tensor_begin[3,4,5]
  #join tensor_trans[3,4,5] tensor_begin[0,1,2]
  #result= join[]+tensor_trans[0,1,2]
  result=np.empty(tensor_begin.shape)
  shape=tensor_trans.shape
  for i in range(shape[0]):
    for j in range(shape[1]):
      for k in range(shape[2]):
        for m in range(shape[3]):
          for n in range(shape[4]):
            for x in range(shape[5]):
              result[i,j,k,m,n,x]=np.sum(tensor_trans.data[i,j,k,m,n,x,:,:,:]*tensor_begin.data[m,n,x,:,:,:])

  return tensor.tensor(result)



def checkError(tensor_a,tensor_b):
    return np.linalg.norm(tensor_a.data-tensor_b.data)

def pow_approch(tensor_trans,tensor_begin,error):
    #compute the astringency result
    resultx=unified_k3_m2(tensor_trans,tensor_begin)
    #print(resultx)
    resulty=unified_k3_m2(tensor_trans,resultx)
    i=0
    while(checkError(resultx,resulty)>error and i<MAX_TIMES):
     resultx=resulty
     resulty=unified_k3_m2(tensor_trans,resulty)
     i+=1

    if i==MAX_TIMES :
      print("------------------------------------reach the MAX_TIMES,so the result may be false-----------------------------------------------")

    return resulty,i

def random_trans(tensor_trans,tensor_begin):
    #create random tensor_trans, prove astringency

    trans_shape=tensor_trans.shape
    begin_shape=tensor_begin.shape
  
    for i in range(trans_shape[8]):
      for j in range(trans_shape[7]):
        for k in range(trans_shape[6]):
          for m in range(trans_shape[5]):
            for n in range(trans_shape[4]):
              for z in range(trans_shape[3]):
                 sum=0
                 for q in range(trans_shape[2]):
                   for w in range(trans_shape[1]):
                     for e in range(trans_shape[0]):
                         x=random.uniform(0,0.1)
                         if(sum+x>=1):
                           tensor_trans.data[e,w,q,z,n,m,k,j,i]=1-sum
                           sum=1
                           break
 
                         else:
                           tensor_trans.data[e,w,q,z,n,m,k,j,i]=x
                           sum+=x
                     if sum==1:
                        break
                     
                   if sum==1:
                       break
                 if sum!=1 :
                    tensor_trans.data[e,w,q,z,n,m,k,j,i]+=1-sum
                      
    sum=0                   
    for e in range(begin_shape[0]):          
      for w in range(begin_shape[1]):          
        for q in range(begin_shape[2]):
          for z in range(begin_shape[3]):          
            for n in range(begin_shape[4]):          
              for m  in range(begin_shape[5]):          
                 x=random.uniform(0,0.01)
                 if(sum+x>=1):
                     tensor_begin.data[e,w,q,z,n,m]=1-sum
                     sum=1
                     return
                 else:
                     tensor_begin.data[e,w,q,z,n,m]=x
                     sum+=x
                      
                      
    if sum!=1:
         tensor_begin.data[e,w,q,z,n,m]+=1-sum
    return
    
        
   
   
if  __name__=='__main__' :
  #a=np.array(range(13824),dtype=np.float64).reshape([2,3,4,2,3,4,2,3,4])
  #b=np.array(range(576),dtype=np.float64).reshape([2,3,4,2,3,4])
  a=np.zeros([2,3,4,2,3,4,2,3,4])
  b=np.zeros([2,3,4,2,3,4])
  tensor_trans=tensor.tensor(a)
  tensor_begin=tensor.tensor(b)
  
  random_trans(tensor_trans,tensor_begin)

  print('tensor_tran')
  print(tensor_trans.data[:,:,:,0,0,0,0,0,0])
  print(np.sum(tensor_trans.data[:,:,:,0,0,0,0,0,0]))

  print('tensor_begin')
  print(np.sum(tensor_begin.data[:,:,:,:,:,:]))
 
  result=unified_k3_m2(tensor_trans,tensor_begin)
 # print(result.data[0,0,0,0,0,0])
  resulty,i=pow_approch(tensor_trans,tensor_begin,1e-8)  
  print(i)
  print(np.sum(resulty.data))

"""
  resulty,i=pow_approch(tensor_trans,tensor_begin,1e-9)  
  print(i)
  resulty,i=pow_approch(tensor_trans,tensor_begin,1e-10)  
  print(i)
  resulty,i=pow_approch(tensor_trans,tensor_begin,1e-11)  
  print(i)
  resulty,i=pow_approch(tensor_trans,tensor_begin,1e-12)  
  print(i)
  resulty,i=pow_approch(tensor_trans,tensor_begin,1e-13)  
  print(i)
  resulty,i=pow_approch(tensor_trans,tensor_begin,1e-14)  
  print(i)
"""
   

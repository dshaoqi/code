#import setEnv
import sys
pathadd=['/home/dsq0/mypython/dsq','/home/dsq0/mypython/dsq/TensorLib']
for i in pathadd:
  sys.path.append(i)
import numpy as np
from TensorLib import tensor
from TensorLib import tools
MAX_TIMES=1

def unified_k3_m3(tensor_trans,tensor_begin):
  #conteract first 3 dim tensor_trans[9,10,11] tensor_begin[6,7,8]
  #join tensor_trans[3,4,5,6,7,8] tensor_begin[0,1,2,3,4,5]
  #result= join[]+tensor_trans[0,1,2]
  result=np.empty(tensor_begin.shape)
  shape=tensor_trans.shape
  for i in range(shape[0]):
    for j in range(shape[1]):
      for k in range(shape[2]):
        for m in range(shape[3]):
          for n in range(shape[4]):
            for x in range(shape[5]):
              for q in range(shape[6]):
                for w in range(shape[7]):
                  for e in range(shape[8]):
                    result[i,j,k,m,n,x,q,w,e]=np.sum(tensor_trans.data[i,j,k,m,n,x,q,w,e:,:,:]*tensor_begin.data[m,n,x,q,w,e,:,:,:])

  return tensor.tensor(result)



def chechError(tensor_a,tensor_b):
    return np.linalg.norm(tensor_a.data-tensor_b.data)

def pow_approch(tensor_trans,tensor_begin,error):
    resultx=unified_k3_m3(tensor_trans,tensor_begin)
    #print(resultx)
    resulty=unified_k3_m3(tensor_trans,resultx)
    i=0
    while(checkError(resultx,resulty)>error and i<MAX_TIMES):
     resultx=resulty
     resulty=unified_k3_m3(tensor_trans,resulty)

    return resulty


if __name__=='__main__' :
  a=np.array(range(13824*2*3*4),dtype=np.float64).reshape([2,3,4,2,3,4,2,3,4,2,3,4])
  b=np.array(range(576*24),dtype=np.float64).reshape([2,3,4,2,3,4,2,3,4])
  tensor_trans=tensor.tensor(a)
  tensor_begin=tensor.tensor(b)
  #print(tensor_begin)
  print('tensor_tran')
  print(tensor_trans.data[0,0,0,0,0,0,0,0,0,:,:,:])
  print('tensor_begin')
  print(tensor_begin.data[0,0,0,0,0,0,:,:,:])
  result=unified_k3_m3(tensor_trans,tensor_begin)
  print(result.data[0,0,0,0,0,0,0,0,0])
 #error=10
  


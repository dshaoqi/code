import tensorflow as tf
import readConIMP as rc
import numpy as np
import random

img_train=rc.getContent('TR-M')
for i in range(4):
 del(img_train[0])
img_train_tensor=np.array(img_train,dtype='uint8').reshape(60000,784)

img_test=rc.getContent('TE-M')
for i in range(4):
 del(img_test[0])
img_test_tensor=np.array(img_test,dtype='uint8').reshape(10000,784)

label_train=rc.getContent('TR-L')
for i in range(2):
 del(label_train[0])
#print label_train[0]
label_train_tensor=np.zeros([60000,10],dtype='uint8')
for i in range(len(label_train)):
  label_train_tensor[i][label_train[i]]=1
#label_train_tensor=np.array(label_train,dtype='uint8').reshape(60000,10)

label_test=rc.getContent('TE-L')
for i in range(2):
 del(label_test[0])
label_test_tensor=np.zeros([10000,10],dtype='uint8')
for i in range(len(label_test)):
  label_test_tensor[i][label_test[i]]=1
#label_test_tensor=np.array(label_test,dtype='uint8').reshape(10000,10)


def randomSet(num):
   img=np.empty([num,784],dtype='uint8')
   lab=np.empty([num,10],dtype='uint8')
   x=np.array(range(60000))
   random.shuffle(x)
   for i in range(num):
     img[i,:]=img_train_tensor[x[i],:]
     lab[i,:]=label_train_tensor[x[i],:]
   return img,lab


x=tf.placeholder("float",[None,784])

w=tf.Variable(tf.zeros([784,10]))
b=tf.Variable(tf.zeros([10]))

y=tf.nn.softmax(tf.matmul(x,w)+b)

y_=tf.placeholder('float',[None,10])
cross_entropy=-tf.reduce_sum(y_*tf.log(y))

train_step=tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init=tf.initialize_all_variables()

sess=tf.Session()
sess.run(init)

for i in range(1000):
 batch_xs,batch_ys=randomSet(100)
 sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys})

#correct_prediction=tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
#accuracy=tf.reduce_mean(tf.cast(correct_prediction,'float'))

#print sess.run(accuracy,feed_dict={x:mn})

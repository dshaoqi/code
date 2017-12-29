import os 
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
#python 2.7
hello=tf.constant("hello, tensorflow")
ses=tf.Session()
print ses.run(hello)

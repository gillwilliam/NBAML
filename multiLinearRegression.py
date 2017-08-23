import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

import csv
import sys

import players

#for csv

x_features = []
features = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'TOV']

#For feature scaling
averages = [102.7/10, 22.3/10, 43.8/10, 7.8/10, 5/10, 14.4/10]

y_real = []

listofplayers = players.Players("2016")
listofplayers.loadData()

print(len(listofplayers.players))



for playerData in listofplayers.players:
    temp = []
    ind = 0
    for feature in features:
        temp.append(playerData[feature]/averages[ind])
        ind+=1
    x_features.append(temp)
    y_real.append(playerData["Salary"]/6)


#for graphing
costlist = []
iteration = []

print(x_features[0])
print(y_real[0])

#data constants
datapoint_size = len(x_features)
batch_size = len(x_features)
steps = 1000
learn_rate = 0.001




# Model linear regression y = Wx + b
x = tf.placeholder(tf.float32, [None, len(features)], name="x")
W = tf.Variable(tf.zeros([len(features),1]), name="W")
b = tf.Variable(tf.zeros([1]), name="b")
with tf.name_scope("Wx_b") as scope:
  product = tf.matmul(x,W)
  y = product + b


y_ = tf.placeholder(tf.float32, [None, 1])

# Cost function sum((y_-y)**2)
with tf.name_scope("cost") as scope:
  cost = tf.reduce_mean(tf.square(y_-y))
  cost_sum = tf.summary.scalar("cost", cost)

# Training using Gradient Descent to minimize cost
with tf.name_scope("train") as scope:
  train_step = tf.train.GradientDescentOptimizer(learn_rate).minimize(cost)

all_xs = []
all_ys = []

all_ys = y_real
all_xs = x_features

all_xs = np.array(all_xs)
all_ys = np.transpose([all_ys])

sess = tf.Session()

# Merge all the summaries and write them out to /tmp/mnist_logs
merged = tf.summary.merge_all()

init = tf.global_variables_initializer()
sess.run(init)


for i in range(steps):
  all_feed = { x: all_xs, y_: all_ys }
  sess.run(train_step, feed_dict=all_feed)
  costlist.append(float(sess.run(cost, feed_dict=all_feed)))
  iteration.append(i)

  if(i == (steps-1)):
    print("After %d iteration:" % i)
    print("W: %s" % sess.run(W))
    print("b: %f" % sess.run(b))
    print("cost: %f" % sess.run(cost, feed_dict=all_feed))

#pick reasonable number based on number of iterations
a = iteration
b = costlist
a = np.array(a)
b = np.array(b)

plt.plot(a, b, 'ro', label='Cost Curve')
plt.legend()
plt.show()
# NOTE: W should be close to actual_W1, actual_W2, and b should be close to actual_b

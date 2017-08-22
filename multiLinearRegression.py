import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

import csv
import sys

#for csv
x_1 = []
x_2 = []
y_real = []

#for graphing
costlist = []
iteration = []

f = open('data.csv', 'rt')
try:
    reader = csv.reader(f)
    for row in reader:
        x_1.append(int(row[0]))
        x_2.append(int(row[1]))
        y_real.append(int(row[2]))
finally:
    f.close()

#data constants
datapoint_size = len(x_1)
batch_size = len(x_1)
steps = 1000
learn_rate = 0.001




# Model linear regression y = Wx + b
x = tf.placeholder(tf.float32, [None, 2], name="x")
W = tf.Variable(tf.zeros([2,1]), name="W")
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
for i in range(datapoint_size):
  y = y_real[i]
  all_xs.append([x_1[i], x_2[i]])
  all_ys.append(y)

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
    print(len(costlist))
    print(len(iteration))

a = np.array(iteration)
b = np.array(costlist)

plt.plot(a, b, 'ro', label='Original data')
plt.legend()
plt.show()
# NOTE: W should be close to actual_W1, actual_W2, and b should be close to actual_b

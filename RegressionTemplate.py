# Machine Learning HW1

import matplotlib.pyplot as plt
import numpy as np
# more imports

# Parse the file and return 2 numpy arrays
def load_data_set(filename):
    # your code
    data = []
    labels = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            # feature, feature, label
            labels.append(float(parts[-1]))
            features = [float(x) for x in parts[:-1]]
            data.append(features)
            x=np.array(data)
            y=np.array(labels)
    return x, y

# Find theta using the normal equation
def normal_equation(x, y):
    # your code
    #theta = (X^T * X)^-1 * X^T * y
    theta = np.linalg.inv(x.T.dot(x)).dot(x.T).dot(y)
    return theta

# Find thetas using stochiastic gradient descent
# Don't forget to shuffle
def stochiastic_gradient_descent(x, y, learning_rate, num_iterations):
    # your code
    m,n =x.shape
    theta=np.zeros(n)
    thetas = []
    for epoch in range(num_iterations):
        #shuffle data
        indices = np.arange(m)
        np.random.shuffle(indices)
        x_shuffled = x[indices]
        y_shuffled = y[indices]
        #done shuffling
        for i in range(m):
            xi = x_shuffled[i]
            yi = y_shuffled[i]
            prediction = xi.dot(theta)
            error = prediction - yi
            gradient = xi.T.dot(error)
            theta = theta - learning_rate * gradient
        thetas.append(theta.copy())
        #debug
        print("sgd, epoch: ", epoch, "theta: ", theta)
    return thetas 

def gradient_descent(x, y, learning_rate, num_iterations):
    m, n = x.shape
    theta = np.zeros(n)
    thetas = []  # list, just like SGD

    for epoch in range(num_iterations):
        prediction = x.dot(theta)
        errors = prediction - y
        gradient = (1/m) * (x.T @ errors)
        theta = theta - learning_rate * gradient

        thetas.append(theta.copy())  # one copy per epoch
        print("GD, epoch:", epoch, "theta:", theta)

    return thetas

# Find thetas using minibatch gradient descent
# Don't forget to shuffle
def minibatch_gradient_descent(x, y, learning_rate, num_iterations, batch_size):
    # your code
    m,n=x.shape
    theta = np.zeros(n)
    thetas=[]

    for epoch in range(num_iterations):
        #shuffle data
        indices = np.arange(m)
        np.random.shuffle(indices)
        x_shuffled = x[indices]
        y_shuffled = y[indices]
        #done shuffling
        for i in range(0, m, batch_size):
            xi = x_shuffled[i:i+batch_size]
            yi = y_shuffled[i:i+batch_size]

            prediction = xi.dot(theta)
            error = prediction - yi
            gradient = (1/batch_size) * xi.T.dot(error)
            theta = theta - learning_rate * gradient
        thetas.append(theta.copy())
        print("mbgd, epoch: ", epoch, "theta: ", theta)
    return thetas

# Given an array of x and theta predict y
def predict(x, theta):
   # your code 
   y_predict = x.dot(theta)
   return y_predict

# Given an array of y and y_predict return loss
def get_loss(y, y_predict):
    # your code
    m=len(y)
    loss = (1/m) * np.sum((y-y_predict) **2)
    return loss

# Given a list of thetas one per epoch
# this creates a plot of epoch vs training error
def plot_training_errors(x, y, thetas, title): 
    losses = []
    epochs = []
    losses = []
    epoch_num = 1
    for theta in thetas:
        losses.append(get_loss(y, predict(x, theta)))
        epochs.append(epoch_num)
        epoch_num += 1
    plt.plot(epochs, losses)
    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.title(title)
    plt.show()

# Given x, y, y_predict and title,
# this creates a plot
def plot(x, y, theta, title):
    # plot
    y_predict = predict(x, theta)
    plt.scatter(x[:, 1], y)
    plt.plot(x[:, 1], y_predict)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(title)
    plt.show()

    x, y = load_data_set('regression-data.txt')
    # plot
    plt.scatter(x[:, 1], y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Scatter Plot of Data")
    plt.show()

    theta = normal_equation(x, y)
    plot(x, y, theta, "Normal Equation Best Fit")

    # You should try multiple non-zero learning rates and  multiple different (non-zero) number of iterations
    thetas = gradient_descent(x, y, 0.05, 100) 
    plot(x, y, thetas[-1], "Gradient Descent Best Fit")
    plot_training_errors(x, y, thetas, "Gradient Descent Mean Epoch vs Training Loss")

    # You should try multiple non-zero learning rates and  multiple different (non-zero) number of iterations
    thetas = stochiastic_gradient_descent(x, y, 0.05, 12) # Try different learning rates and number of iterations
    plot(x, y, thetas[-1], "Stochiastic Gradient Descent Best Fit")
    plot_training_errors(x, y, thetas, "Stochiastic Gradient Descent Mean Epoch vs Training Loss")

    # You should try multiple non-zero learning rates and  multiple different (non-zero) number of iterations
    thetas = minibatch_gradient_descent(x, y, 0.05, 12, 32)
    plot(x, y, thetas[-1], "Minibatch Gradient Descent Best Fit")
    plot_training_errors(x, y, thetas, "Minibatch Gradient Descent Mean Epoch vs Training Loss")
__author__ = 'samipc'
import random
import time

# handle input data from a user
def data():
    # deal with the input data separately
    while True:
        try:
            w = int(raw_input('Enter image width(int): '))  # take input data from the user
        except ValueError:  # now check if the input data is satisfying our desirable values (integer values)
            print 'That is not an int,try again!!'
            continue
        if w <= 0:  # be aware, we want only positive integer & greater than zero
            print 'Sorry, please enter only positive int!!'
            continue
        else:
            break

    while True:
        try:
            h = int(raw_input('Enter image height(int): '))
        except ValueError:
            print 'That is not an int,try again!!'
            continue
        if h <= 0:
            print 'Sorry, please enter only positive int!!'
            continue
        else:
            break

    return w, h

# construct  a matrix of m x n and fill it with random values (we can create an array and the faster way is to use
# numpy)
def matrix_creation(m, n):
    output_image = [[0 for i in xrange(m)] for j in xrange(n)]
    matrix = [[random.randint(0, 255) for i in xrange(m)] for j in xrange(n)]  # create a matrix of m x n
    dx_matrix = [[0 for i in xrange(m)] for j in xrange(n)]  # will be used to store the pixel values of the dx derivative (x-axis)
    dy_matrix = [[0 for i in xrange(m)] for j in xrange(n)]  # will be used to store the pixel values of the dy derivative (y-axis)
    return matrix, dx_matrix, dy_matrix, output_image


# Here, lets implement our filter
def filter2(image, outpt_image, di_dx, di_dy, m, n, t ):
    # lets compute the directional change of a pixel (intensity/color) with respect to the x-ax and the y-ax
    di_time_start = time.time()
    for r in range(1, m-1):
        for c in range(1, n-1):

            # let's say we have a mask of 3x3 and want to find the directional change of central pixel
            # |56 |45|20|
            # |20 |30|44|
            # |45 |10|23|
            #------------
            # let's compute the change of center pixel( pix[1][1] = 30)
            # the neighbors of the center pixel are defined as the east, west, north, south pixels
            # dy = north pixel - south pixel => (45-10)
            # dx = east pixel - west pixel  => (44-20)
            di_dy[c][r] = image[c][r-1] - image[c][r+1]  # (change in the y-direction (vertical direction))
            di_dx[c][r] = image[c+1][r] - image[c-1][r]  # (change in the x-direction(horizontal direction))
            magnitude_i = abs(di_dx[c][r]) + abs(di_dy[c][r])
            if magnitude_i < t:
              #  'update the pixel'
               outpt_image[c][r] = 1


    # for each row in the matrix find the max/min value and store it in a list and then find the max/min value in a list
    dx_max = max([max(l) for l in di_dx])
    dy_max = max([max(l) for l in di_dy])
    dx_min = min([min(l) for l in di_dx])
    dy_min = min([min(l) for l in di_dy])

    # compute the time taken for  processing dy,dx, max, min
    di_time_end = time.time()-di_time_start
    return dx_max, dx_min, dy_max, dy_min, di_time_end, di_dy, di_dx, outpt_image

#======== MAIN =======
threshold = 255
width, height = data()
input_image, x_di, y_di, out_image = matrix_creation(width,height)
x_max, x_min, y_max, y_min, total_time, di_dy, di_dx, out = filter2(input_image, out_image,  x_di, y_di, width, height, threshold)

print "Total Elapsed time (s): %f" % total_time
print "Max value of dx matrix: %d" % x_max
print "Min value of dx matrix: %d" % x_min
print "Max value of dy matrix: %d" % y_max
print "Min value of dy matrix: %d" % y_min

# print matrix of dx and dy

import numpy as np
print 'dx matrix = '
print np.array(di_dx)
print 'dy matrix = '
print np.array(di_dy)

print np.array(out)
############### output ############################
'''/usr/bin/python2.7 /home/me/PycharmProjects/untitled/convo_filter.py
Enter image width(int): 10
Enter image height(int): 10
Total Elapsed time (s): 0.000069
Max value of dx matrix: 215
Min value of dx matrix: -232
Max value of dy matrix: 202
Min value of dy matrix: -233
dx matrix =
[[   0    0    0    0    0    0    0    0    0    0]
 [   0  -10   79   56 -149   14   -2 -193  164    0]
 [   0  -35   39  215   99  100    6  -66 -230    0]
 [   0  -13  -83  106   82   82  -54  104  -28    0]
 [   0  -82  -49 -232   60  -52  128  101   98    0]
 [   0   -9  -80  -97  -28 -107   79   35   -9    0]
 [   0  149  -24   95    4  -79  109  -44   34    0]
 [   0 -173  -12  112  -13   -2 -104  -75   50    0]
 [   0  -94  -71   86 -184  112 -202  -90  -56    0]
 [   0    0    0    0    0    0    0    0    0    0]]
dy matrix =
[[   0    0    0    0    0    0    0    0    0    0]
 [   0 -147  118   76  -55   81 -133 -233  -11    0]
 [   0  -68  154  147  -29  -23   72  -42 -201    0]
 [   0  -85 -132   16   60  174   33    3  -53    0]
 [   0  -23   35  -18   -5  113   50  -68 -121    0]
 [   0 -124   18  -93 -120  106 -120   33  109    0]
 [   0    0  123  -70    5    6  -92   20   21    0]
 [   0 -118   72 -121   54    1 -155  108  202    0]
 [   0  100 -162  -69  119   97  -19 -134  -87    0]
 [   0    0    0    0    0    0    0    0    0    0]]'''

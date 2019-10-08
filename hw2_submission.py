#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
testingrooms = ['A','B','C']
for room in testingrooms:
    shutil.move('/Users/jmsaito/Documents/GitHub/ps2-jmsaito25/testingroom'
              + room + '/experiment_data.csv', 
              '/Users/jmsaito/Documents/GitHub/ps2-jmsaito25/rawdata/experiment_data_' + room + '.csv')


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
os.chdir('/Users/jmsaito/Documents/GitHub/ps2-jmsaito25/rawdata')
for room in testingrooms:
    filename = 'experiment_data_' + room + '.csv'
    print('Now appending ' + filename)
    temp = np.loadtxt(filename,delimiter=',')
    data = np.vstack([data,temp])

#%%
# calculate overall average accuracy and average median RT
#
acc_avg = np.mean(data[:,3])   # 91.48%
mrt_avg = np.mean(data[:,4])   # 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
subs = len(data)
word_acc = 0
word_rt = 0
face_acc = 0
face_rt = 0
num_word = 0
num_face = 0

for rows in range(subs):
    if data[rows,1] == 1: #word
        num_word = num_word + 1
        word_acc = word_acc + data[rows,3]
    elif data[rows,1] == 2: #face  
        num_face = num_face + 1
        face_acc = face_acc + data[rows,3]
        
for rows in range(subs):
    if data[rows,1] == 1: #word
        word_rt = word_rt + data[rows,4]
    elif data[rows,1] == 2: #face  
        face_rt = face_rt + data[rows,4]
        
word_acc = word_acc/num_word
word_rt = word_rt/num_word
face_acc = face_acc/num_face
face_rt = face_rt/num_face   

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#

acc_wp = np.mean(data[data[:,2]==1,3]) # 94.0%
acc_bp = np.mean(data[data[:,2]==2,3]) # 88.9%
mrt_wp = np.mean(data[data[:,2]==1,4]) # 469.6ms
mrt_bp = np.mean(data[data[:,2]==2,4]) # 485.1ms

#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#
word_wp = []
word_bp = []
face_wp = []
face_bp = []

ticker = len(data)

for x in range(ticker):
    if data[x,1]==1:
        if data[x,2]==1:
            word_wp = np.append(word_wp,data[x,4])
            print(word_wp)
        elif data[x,2]==2:
            word_bp = np.append(word_bp,data[x,4])
            print(word_bp)
    elif data[x,1]==2:
        if data[x,2]==1:
            face_wp = np.append(face_wp,data[x,4])
            print(face_wp)
        elif data[x,2]==2:
            face_bp = np.append(face_bp,data[x,4])
            print(face_bp)

word_wp_rt = np.mean(word_wp)
word_bp_rt = np.mean(word_bp)
face_wp_rt = np.mean(face_wp)
face_bp_rt = np.mean(face_bp)

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#

import scipy.stats

word_stats = scipy.stats.ttest_rel(word_wp,word_bp)
face_stats = scipy.stats.ttest_rel(face_wp,face_bp)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print('\nWORDS: {:.2f}%, {:.1f} ms'.format(100*word_acc,word_rt))
print('\nFACES: {:.2f}%, {:.1f} ms'.format(100*face_acc,face_rt))
print('\nBIAS-CONGRUENT TRIALS (Collapsed Across Stim Type): {:.2f}%, {:.1f} ms'.format(100*acc_wp,mrt_wp))
print('\nBIAS-INCONGRUENT TRIALS (Collapsed Across Stim Type): {:.2f}%, {:.1f} ms'.format(100*acc_bp,mrt_bp))
print('\nThe improved RT on bias-congruent word pairs ({:.1f} ms) compared to bias-incongruent word pairs ({:.1f} ms)\
 is statistically significant, t = {:.2f}, p < 0.01. This pattern was replicated between bias-congruent face-pairs ({:.1f} ms) \
and bias-incongruent face-pairs ({:.1f} ms) trials, t = {:.2f}, p = {:.2f}'.format(word_wp_rt,\
word_bp_rt,word_stats[0],face_wp_rt,\
face_bp_rt,face_stats[0],face_stats[1]))
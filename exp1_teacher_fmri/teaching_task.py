#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 08:46:01 2021

@author: aliciachen, nataliavelez
"""

import argparse, sys, time, json, random, copy
import numpy as np
from psychopy import gui, core, visual, event, data
from signal import signal,SIGINT,SIGTERM

# Experiment-specific modules
import teaching_game_logic as game

### LOAD PROBLEMS AND EXPERIMENT ORDER ###
# Parse subject ID and run from command line arguments
parser=argparse.ArgumentParser()
parser.add_argument('--sub', help='Subject # (int)')
parser.add_argument('--run', help='Run # (int)')

print('\n=== SETTING UP RUN ===')
print('Passing arguments...')
args=parser.parse_args()

if args.sub is not None:
    sub=int(args.sub)
else:
    print('No subject, running debug')
    sub='debug'

if args.run is not None:
    run=int(args.run)
else:
    print('No run, defaulting to first run')
    run=1

# Confirm before launching run
print('SUBJECT: %s | RUN: %i' % (str(sub), run))
input('Press Enter to confirm') # uncomment for production

# Load timing information
if isinstance(sub, int):
    in_file = 'inputs/timing/sub-%02d_task-teaching_run-%02d_timing.json' % (sub, run)
else:
    in_file = 'inputs/timing/sub-%s_task-teaching_run-%02d_timing.json' % (sub, run) # debug
print('\nLoading timing info from: %s' % in_file)
with open(in_file, 'r') as f:
    timing = json.load(f)

# Sanity check: Run length matches # of images in protocol
last_trial = timing[-1]
run_length = last_trial['ons'] + last_trial['dur']
n_images = np.ceil(run_length/2)
print('# images: %i' % n_images)
print('Run length: %02d:%02d' % (np.floor(n_images*2/60), (n_images*2) % 60))

# Set path to out file
tstamp = int(time.time())
out_file = in_file.replace('inputs/timing', 'data').replace('_timing', '_behavioral_%i' % tstamp)
data = []
print('\nSaving data to: %s' % out_file)

# Helper function: Save data
def save_data():
    with open(out_file, 'w') as out:
        json.dump(data, out)

# Set up emergency exit
def emergency_exit(signum, frame):
    print('Task interrupted! Saving data...')
    save_data()
    core.quit()
signal(SIGINT, emergency_exit)
signal(SIGTERM, emergency_exit)

### HARDWARE SETUP ###
# Set up monitor
width, height = (800, 600) # uncomment for scanning monitor
aspect = width/height
w = visual.Window(fullscr=True, size=(width, height), screen = 0, color='black')
w.mouseVisible = False # uncomment for production

# Set up keys
# keylist = ('space', 'j','k','l','semicolon', 'q') # debug
keylist = ('0', '1', '2', '3', '4', 'q') # uncomment for production
keymap = dict(zip(keylist, ((0,0,True), (0,-1,False), (1,0,False),(-1,0,False),(0,1,False),(0,0,False))))

# ### WAIT FOR SCANNER TRIGGER ###
countdown = 5
for sec in range(countdown):
    txt = "Please lie very still!\nWe will begin in:\n\n%i" % (countdown-sec) 
    still_txt = visual.TextStim(w, text=txt, pos=(0,0.1), wrapWidth=2)
    still_txt.draw()
    w.flip()
    core.wait(1)

start_txt = visual.TextStim(w, text="Waiting for scanner", pos=(0,0), wrapWidth=2)
start_txt.draw()
w.flip()
event.waitKeys(keyList=['equal'])

### INITIALIZE PROBLEMS ###
# starting points
new_state = [
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]
]
corners = [(0,0),(0,5),(5,0),(5,5)] # where to start cursor
random.shuffle(corners)

# init exp loop
problem_counter = 0
state = copy.deepcopy(new_state)
cursor = corners.pop()

### MAIN EXPERIMENT LOOP ###
print('Starting clock')
t = core.MonotonicClock() # start clock

for trial in timing:
    # is this a new problem?
    if 'problem_idx' in trial:
        if  trial['problem_idx'] > problem_counter:
            
            # if so, refresh the game state
            print('\n==== NEW PROBLEM: %i ====' % trial['problem'])
            state = copy.deepcopy(new_state)
            cursor = corners.pop()

            # and update counter
            problem_counter = trial['problem_idx']

    # hacky workaround to show off the last-selected example
    if trial['type'] == 'show':
        trial_data = game.present(w,t,trial,state,highlight)
    else:
        trial_data = game.present(w,t,trial,state,cursor)
    data.append(trial_data)
    save_data() # new: save data after each trial

    # update state and cursor after choose trials
    if trial['type'] == 'choose':

        state = trial_data['state']
        cursor = trial_data['cursor']

        last_example = trial_data['example']
        if last_example is not None:
            highlight = cursor
        else:
            highlight = None

# Save data at the end
print('All done! Saving data')
print(data)
save_data()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 08:46:01 2021

@author: aliciachen, nataliavelez
"""

import argparse, sys, time, json, random, copy
import numpy as np
from psychopy import gui, core, visual, event, data
from signal import signal,SIGINT

# Experiment-specific modules
import teaching_game_logic as game

### LOAD PROBLEMS AND EXPERIMENT ORDER ###
# Parse subject ID and run from command line arguments
parser=argparse.ArgumentParser()
parser.add_argument('--sub', help='Subject # (int)')
parser.add_argument('-scan', action='store_true',
                   help='Use this flag when running the practice task in the scanner')

print('\n=== SETTING UP RUN ===')
print('Passing arguments...')
args=parser.parse_args()

if args.sub is not None:
    sub=int(args.sub)
else:
    print('No subject, running debug')
    sub=0

# Confirm before launching run
print('SUBJECT: %s | RUN: PRACTICE' % str(sub))
# input('Press Enter to confirm') # uncomment for production

# Load timing information
in_file = 'inputs/timing/sub-debug_task-teaching_run-01_timing.json'
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
out_file = 'data/sub-%02d_task-teaching_run-practice_behavioral_%i.json' % (sub, tstamp)
data = []
print('\nSaving data to: %s' % out_file)

# Helper function: Save data
def save_data():
    with open(out_file, 'w') as out:
        json.dump(data, out)


# Set up emergency exit
def emergency_exit(signum, frame):
    print('Task interrupted! Saving data...')
    json.dump(data, open(out_file, 'w'))
    core.quit()
signal(SIGINT, emergency_exit)

### HARDWARE SETUP ###
# Set up monitor



# Start task differently, depending on whether participant is in scanner or not
instruct_prompt="Next, we'll do a practice run of the task.\n\
 Please do your best to provide a response in time!\n\n"
if args.scan:
    start_prompt="Press any key to start"
    start_key = ['0', '1', '2', '3', '4', 'equal']
    width, height = (800, 600)
    is_fullscr=True
else:
    game.laptop_keys()
    start_prompt="Press = to start"
    start_key = ['equal']
    width, height = (1024, 768)
    is_fullscr=False

game.practice_mode()
aspect = width/height
w = visual.Window(fullscr=is_fullscr, size=(width, height), screen = 0, 
    color='black', useRetina=True)
w.mouseVisible = False # uncomment for production

# # ### WAIT FOR SCANNER TRIGGER ###
# countdown = 5
# for sec in range(countdown):
#     txt = "Please lie very still!\nWe will begin in:\n\n%i" % (countdown-sec) 
#     still_txt = visual.TextStim(w, text=txt, pos=(0,0.1), wrapWidth=2)
#     still_txt.draw()
#     w.flip()
#     core.wait(1)

start_txt = visual.TextStim(w, text=instruct_prompt+start_prompt, pos=(0,0), wrapWidth=1.75)
start_txt.draw()
w.flip()
event.waitKeys(keyList=start_key)

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
    save_data() # new: save data after every trial

    # update state and cursor after choose trials
    if trial['type'] == 'choose':
        cursor = trial_data['cursor']
        state = trial_data['state']

        last_example = trial_data['example']
        if last_example is not None:
            highlight = cursor
        else:
            highlight = None

# Save data at the end
print('All done! Saving data')
print(data)
save_data()

if args.scan:
    end_text = 'Great job!\nPlease stay still until the end of the scan.\
    Feel free to rest your eyes for a while.'
else:
    end_text = 'Great job!\nPlease see the experimenter to proceed to your scan.\n\n\
    Press = to close.'

end_stim = visual.TextStim(w, text = end_text, pos=(0,0), wrapWidth=2)
end_stim.draw()
w.flip()
event.waitKeys(keyList=['equal'])

w.close()
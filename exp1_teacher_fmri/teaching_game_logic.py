#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 9 12:44:01 2021

@author: aliciachen, nataliavelez
"""
import copy, json
import numpy as np
from psychopy import gui, core, visual, event, data # Stimulus presentation

# experiment-specific modules
import teaching_stimuli as stim

# Load teaching problems
with open('inputs/problems.json') as file:
    problems = json.load(file)

# Hardware setup
keylist = ('0', '1', '2', '3', '4', 'q') # uncomment for production
keymap = dict(zip(keylist, ((0,0,True), (0,-1,False), (-1,0,False),(1,0,False),(0,1,False),(0,0,False))))

def laptop_keys():
    global keylist
    global keymap

    print('Switching to laptop key mappings...')
    keylist = ('space', 'j','k','l','semicolon', 'q')
    keymap = dict(zip(keylist, ((0,0,True), (0,-1,False), (-1,0,False),(1,0,False),(0,1,False),(0,0,False))))

# Helper function: Override key list, problems for practice task
def practice_mode():
    global problems

    print('Loading practice problems...')
    with open('inputs/practice_problems.json') as file:
        problems = json.load(file)

    print(keymap)

### CURSOR MOVEMENTS ###
# Helper function: Keep locations within map bounds
def bound_loc(c_orig):
    c = c_orig # proposed coordinate
    c = max(c, 0) # no lower than 0
    c = min(c, 5) # no higher than 5
    return c

# Helper function: Update location
def update_location(sqs,r0,c0,key):
    # Parse command
    dr,dc,flag = keymap[key]

    print('\nKEY: %s' % key)
    print('At: (%i, %i)' % (r0,c0))
    
    # Update locations
    row = bound_loc(r0+dr)
    col = bound_loc(c0+dc)

    print('Moved to: (%i, %i)' % (row, col))
    
    # Check if user tried to select goal
    reached_goal = sqs[row][col] == 1
    win_state = flag & reached_goal
    print(win_state)

    return row,col,win_state

### PRESENTATION FUNCTIONS ###
def pause(w,t,trial,state,cursor):
    pause_stim = visual.TextStim(w, text="+", pos=(0,0), height=.2)
    data = {
        'true_ons': t.getTime()
    }

    # Keep fixation cross up on screen
    while t.getTime() < trial['ons'] + trial['dur']:
        pause_stim.draw()
        w.flip()
    data['true_dur'] = t.getTime() - data['true_ons']

    # Save data
    out = copy.deepcopy(trial)
    out.update(data)
    return out

def study(w,t,trial,state,cursor):
    data = {
        'true_ons': t.getTime()
    }
    prob = problems[trial['problem']]

    # Keep fixation cross up on screen
    while t.getTime() < trial['ons'] + trial['dur']:
        # Draw teaching problem
        stim.draw_canvas(prob, state, w, True)
        stim.draw_hypotheses(prob, trial['order'], w, True)

        # Tell participants to study
        study_stim = visual.TextStim(w, text='Study problem', pos=(0, -.72))
        study_stim.draw()

        # Start countdown at the end
        t_remaining = np.ceil(trial['ons'] + trial['dur'] - t.getTime())
        if (t_remaining < 4) & (t_remaining > 0):
            sec_stim = visual.TextStim(w, text='%i'%t_remaining, pos=(0, -.88))
            sec_stim.draw()
        w.flip()

    data['true_dur'] = t.getTime() - data['true_ons']

    # Save data
    out = copy.deepcopy(trial)
    out.update(data)
    return out

def choose(w,t,trial,state,cursor):
    # unpack trial params
    r,c = cursor
    prob = problems[trial['problem']]
    sqs = np.add(prob['A'], state)

    # init data
    mvmts = [] # track all movements
    data = {
        'true_ons': t.getTime()
    }

    # init loop
    keys=[]
    selected=False
    rt_clock = core.Clock()

    # main loop
    while t.getTime() < trial['ons'] + trial['dur']:
                
        if not selected: # if there's a keypress, update cursor
            keys = event.getKeys(keyList = keylist, timeStamped=rt_clock)
            if keys:
                r,c,selected=update_location(sqs,r,c,keys[0][0])
                mvmts.append(((r,c),keys[0][1]))
            cursor_color = sqs[r][c]
        else: # stop updating after selection is made
            cursor_color=3

        # Draw stimuli
        stim.draw_cursor(r, c, cursor_color, w)
        stim.draw_canvas(prob, state, w, True)
        stim.draw_hypotheses(prob, trial['order'], w, True)

        w.flip()
    
    # Update state
    new_state=copy.deepcopy(state)
    if selected:
        new_state[r][c] = 1
        
    # save data
    data['true_dur'] = t.getTime() - data['true_ons']
    data['example'] = (r,c) if selected else None
    data['rt'] = keys[0][1] if keys else None
    data['movements'] = mvmts
    data['state'] = new_state
    data['cursor'] = (r,c)

    out = copy.deepcopy(trial)
    out.update(data)
    return out


def pre(w,t,trial,state,cursor):
    pre_stim = visual.TextStim(w, text="Here's what students would see:", pos=(0,0), wrapWidth=2)
    data = {
        'true_ons': t.getTime()
    }

    # Keep text on screen
    while t.getTime() < trial['ons'] + trial['dur']:
        pre_stim.draw()
        w.flip()
    data['true_dur'] = t.getTime() - data['true_ons']

    # Save data
    out = copy.deepcopy(trial)
    out.update(data)
    return out

def show(w,t,trial,state,highlight):
    data = {
        'true_ons': t.getTime()
    }
    prob = problems[trial['problem']]

    # Keep fixation cross up on screen
    while t.getTime() < trial['ons'] + trial['dur']:
        if highlight is not None:
            r,c=highlight
            stim.draw_cursor(r, c, 3, w)
        stim.draw_canvas(prob, state, w, False)
        stim.draw_hypotheses(prob, trial['order'], w, False)
        w.flip()

    data['true_dur'] = t.getTime() - data['true_ons']

    # Save data
    out = copy.deepcopy(trial)
    out.update(data)
    return out

def rate(w,t,trial,state,cursor):
    data = {
        'true_ons': t.getTime()
    }

    # Initialize response vars
    event.clearEvents(eventType='keyboard')
    keys = []
    rt_clock = core.Clock()

    # Get ready to draw feedback
    scale_xs = np.linspace(-.66,.66,5)
    fdbk_stim = visual.Rect(w,
    						size=(0.1,0.1),
    						lineColor='black',
    						fillColor='black',
    						pos=(0,0)) # empty fdbk stim

    # Run trial
    while t.getTime() < trial['ons'] + trial['dur']:

        if not keys:
            keys = event.getKeys(keyList = keylist, timeStamped=rt_clock)
        else:
        	idx = keylist.index(keys[0][0])
        	fdbk_stim = visual.Rect(w,
        		size=(.15, .2),
        		lineWidth=2,
        		lineColor='white',
        		fillColor=None,
        		pos=(scale_xs[idx], -.01))
        
        fdbk_stim.draw()
        stim.draw_scale(w)
        w.flip()
    print(keys)

    # Save participant's response
    data['true_dur'] = t.getTime() - data['true_ons']
    data['rating'] = keylist.index(keys[0][0]) if keys else None
    data['rt'] = keys[0][1] if keys else None

    # Save data
    out = copy.deepcopy(trial)
    out.update(data)
    return out

### PUTTING IT ALL TOGETHER ###
# big dictionary of presentation functions
fun_dict = {
    'pause': pause,
    'study': study,
    'choose': choose,
    'pre': pre,
    'show': show,
    'rate': rate,
}

# main method: call the presentation function corresponding to the current trial
def present(w,t,trial,state,cursor):
    fun = fun_dict[trial['type']]
    data = fun(w,t,trial,state,cursor)
    return data
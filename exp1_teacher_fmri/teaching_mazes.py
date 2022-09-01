#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 20:42:00 2021

@author: nataliavelez
"""
import argparse
import json, random
import numpy as np
from psychopy import gui, core, visual, event, data, monitors # Stimulus presentation
import PIL # Read image size

### SETUP ###
# Parse arguments
# We'll use different key mappings inside vs. outside the scanner
parser=argparse.ArgumentParser()
parser.add_argument('-scan', action='store_true',
                   help='Use this flag when running the practice task in the scanner')

print('\n=== SETTING UP RUN ===')
print('Passing arguments...')
args=parser.parse_args()

if args.scan:
    print('Using scanner keymap')
    keylist = ('0', '1', '2', '3', '4', 'q') # in scanner
    start_prompt = "Press any key to start"
    start_key = ['0', '1', '2', '3', '4', 'equal']
    width, height = (800, 600) # scanning monitor
    w = visual.Window(fullscr=True, size=(width, height), screen = 0, color='black') # debug

    
	
else: 
    print('Using laptop keymap')
    keylist = ('space', 'j','k','l','semicolon', 'q') # outside of scanner
    start_prompt = "Press = to start"
    start_key = ['equal']
    width, height = (1024, 768) # practice laptop
    w = visual.Window(fullscr=False, size=(width, height), screen = 0, color='black') # debug

# Set up monitor
aspect = width/height
w.mouseVisible = False # uncomment for production

# Load mazes
with open('inputs/mazes.json') as file:
    mazes = json.load(file)

# Experiment parameters
colordict = {
    'ground': [(94, 93, 95), (214, 214, 214), (238, 188, 64)],
    'cursor': (72, 160, 248)
}
keymap = dict(zip(keylist, ((0,0,True), (0,-1,False), (-1,0,False),(1,0,False),(0,1,False),(0,0,False))))

# Tile locations
x = np.linspace(-.5, .5, 6)
y = np.linspace(-.5*aspect, .5*aspect, 6)
y = np.flip(y)
xys = [(x_i, y_i) for y_i in y for x_i in x]
sq_size = (1/6)*.95

### DRAWING FUNCTIONS ###
# Helper function: Draw hand
def draw_hand():
    hand_img = 'assets/hand_diagram.png'

    # Image dimensions
    hand_w_pix, hand_h_pix = PIL.Image.open(hand_img).size
    hand_w = hand_w_pix/width
    hand_h = hand_h_pix/height

    # Draw hand
    hand_stim = visual.ImageStim(w, image=hand_img, pos = (0,-hand_h/4), interpolate='linear', size=(hand_w, hand_h))
    hand_stim.draw()

# Helper function: Draw maze
def draw_maze(m):
    sqs = m['maze']
    sqs[m['goal'][0]][m['goal'][1]] = 2

    # Tile colors
    tile_colors = [colordict['ground'][sq] for row in sqs for sq in row]

    # Make stimulus array
    maze_stim = visual.ElementArrayStim(win=w, 
                                        xys=xys, 
                                        colors = tile_colors,
                                        colorSpace='rgb255',
                                        fieldShape='sqr',
                                        nElements=36,
                                        elementMask=None,
                                        elementTex=None,
                                        sizes=(sq_size, sq_size*aspect))
    maze_stim.draw()

# Helper function: Draw cursor
def draw_cursor(r,c):
    cursor_stim = visual.Rect(w, width=sq_size*1.2, height=sq_size*aspect*1.2, pos=(x[c], y[r]),
                            fillColor=colordict['cursor'], colorSpace='rgb255',
                            interpolate=True)
    cursor_stim.draw()

# Helper function: Keep locations within map bounds
def bound_loc(c_orig):
    c = c_orig # proposed coordinate
    c = max(c, 0) # no lower than 0
    c = min(c, 5) # no higher than 5
    return c

# Helper function: Update location
def update_location(maze,r0,c0,key):
    # Parse maze
    m = maze['maze']
    goal_row, goal_col = maze['goal']

    # Parse command
    dr,dc,flag = keymap[key]

    print('\nKEY: %s' % key)
    print('At: (%i, %i)' % (r0,c0))
    
    # Update locations
    row = bound_loc(r0+dr)
    col = bound_loc(c0+dc)

    # Specific to mazes: Reject change if new square == 0
    valid_spot = m[row][col]
    if not valid_spot:
        row = r0
        col = c0

    print('Moved to: (%i, %i)' % (row, col))
    
    # Check if user tried to select goal
    reached_goal = (row == goal_row) & (col == goal_col)
    win_state = flag & reached_goal
    print(win_state)

    return row,col,win_state

### START SCAN ###
if args.scan:
    countdown = 5
    for sec in range(countdown):
        txt = "Please lie very still!\nWe will begin in:\n\n%i" % (countdown-sec) 
        still_txt = visual.TextStim(w, text=txt, pos=(0,0.1), wrapWidth=2)
        still_txt.draw()
        w.flip()
        core.wait(1)

start_txt = visual.TextStim(w, text=start_prompt, pos=(0,0), wrapWidth=2)
start_txt.draw()
w.flip()
event.waitKeys(keyList=start_key)

### INTRODUCE KEYS ###
# Write prompts
key_explanation = """In this task, you'll use a button box to move a cursor.
Each button moves the cursor in a different direction.
First, we're going to practice using the buttons!\n\n
Press any button to continue.
"""

button_check = """To begin, make sure that each of your fingers is resting on a different button.\n\n
Press any button to continue.
"""

for prompt in [key_explanation, button_check]:
    txt = visual.TextStim(w, text=prompt, pos=(0,0), wrapWidth=1.75)
    txt.draw()
    w.flip()
    event.waitKeys(keyList=keylist)

### PRACTICE USING KEYS ###
# Round 1: In order, with colors
practice_cmds = list(zip(
    keylist[:-1],
    ('ACTION', 'LEFT', 'UP', 'DOWN', 'RIGHT'),
    ('#e25a25', '#d973a9', '#f1e507', '#00a170', '#33b5e8')
))

# Round 2: Shuffled, with colors
shuffled_cmds = practice_cmds[:]
random.shuffle(shuffled_cmds)

# Round 3: Shuffled, no colors
colorless_cmds = practice_cmds[:]
colorless_cmds = [(key, prompt, '#ffffff') for key,prompt,_ in colorless_cmds]
random.shuffle(colorless_cmds)

# Putting everything together
all_cmds = practice_cmds+shuffled_cmds+colorless_cmds

for correct, prompt, color in all_cmds:
    
    # Write prompts
    prompt_txt = visual.TextStim(w, text='Please press the following key', pos=(0,.75), wrapWidth=2)
    cmd_txt = visual.TextStim(w, text=prompt, pos=(0,.5), color=color, bold=True)

    # Draw stimuli
    prompt_txt.draw()
    cmd_txt.draw()
    draw_hand()
    w.flip()

    # Wait for correct key to continue
    keys = event.waitKeys(keyList=[correct, 'equal'])
    if keys[0] == 'q': # manual exit
        core.quit()

# draw_hand()
# w.flip()

### EXPLAIN MAZES ###
maze_img = 'assets/maze_diagram.png'
maze_w_pix, maze_h_pix = PIL.Image.open(maze_img).size
maze_w = maze_w_pix/width
maze_h = maze_h_pix/height

# Draw diagam and explanatory text
maze_prompts = [("Let's apply what you've learned! In the next slides, you'll see mazes like this one.",
                 "Press ACTION to continue"),
                 ("Move your cursor towards the gold square, then press ACTION to pick up the treasure",
                 "Press ACTION to start")]

for prompts in maze_prompts:
    top_stim = visual.TextStim(w, text = prompts[0], pos=(0,maze_h/2+.1), wrapWidth=2)
    bottom_stim = visual.TextStim(w, text = prompts[1], pos=(0,-1*(maze_h/2+.1)), wrapWidth=2)
    maze_diagram_stim = visual.ImageStim(w, image=maze_img, pos = (0,0), interpolate='linear', size=(maze_w, maze_h))

    top_stim.draw()
    bottom_stim.draw()
    maze_diagram_stim.draw()
    w.flip()
    event.waitKeys(keyList=keylist[:1])

### MAIN EXPERIMENT LOOP ###
for maze in mazes:
    # initialize maze
    r,c = maze['start']
    win = False

    while not win:
        # Draw map
        draw_cursor(r,c)
        draw_maze(maze)
        w.flip()

        # Get user input
        keys = event.waitKeys(keyList=keylist)
        if keys[0] == 'q': # manually exit exp
            break
        else:
            r,c,win = update_location(maze,r,c,keys[0])
    
    if keys[0] == 'q': # manually exit exp, continued
        break
       
### END EXPERIMENT ###
# End message
end_text = 'Great job!\nYour next task will begin shortly.'
end_stim = visual.TextStim(w, text = end_text, pos=(0,0), wrapWidth=2)
end_stim.draw()
w.flip()
core.wait(5)

w.close()
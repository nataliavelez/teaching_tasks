#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 9 12:44:01 2021

@author: aliciachen, nataliavelez
"""

# Stimulus presentation
from psychopy import visual # Stimulus presentation
import numpy as np

# Key parameters
aspect = 800/600

##### AESTHETIC PARAMS #####
# Colors
colordict = {
    'canvas': [(70, 70, 70), (214, 214, 214), (72, 160, 248)],
    'cursor': [(218, 60, 37), (72, 160, 248), (218, 60, 37), (238, 188, 64)],
    'hypothesis': [(18, 57, 99), (72, 160, 248)],
    'true': (238, 188, 64)
}

# Hypothesis space params
h_y0 = .5
ltr_y0 = h_y0+.33
hypothesis_centers = [(-.75, h_y0), (-.25, h_y0), (.25, h_y0), (.75, h_y0)]
sq_size = .05

# Hypothesis square locations
hypothesis_locations = []
for loc in hypothesis_centers:

    x_low, x_high = loc[0] - 3*sq_size, loc[0] + 3*sq_size
    y_low, y_high = loc[1] - 3*sq_size*aspect, loc[1] + 3*sq_size*aspect

    x = np.linspace(x_low, x_high, 6)
    y = np.linspace(y_low, y_high, 6)
    y = np.flip(y)
    xys = [(x_i, y_i) for y_i in y for x_i in x]

    hypothesis_locations.append(xys)

# Canvas params
# Canvas params
canv_sq_size = .08
canvas_center = [0, -.25]

cx_low, cx_high = canvas_center[0] - 3*canv_sq_size, canvas_center[0] + 3*canv_sq_size
cy_low, cy_high = canvas_center[1] - 3*aspect*canv_sq_size, canvas_center[1] + 3*aspect*canv_sq_size

cx = np.linspace(cx_low, cx_high, 6)
cy = np.linspace(cy_low, cy_high, 6)
cy = np.flip(cy)
canvas_locations = [(x_i, y_i) for y_i in cy for x_i in cx]

def draw_canvas(prob, state, w, teacher_view):
    h = prob['A']

    # Hide the rest of the true hypothesis in student's view
    sqs = np.add(h, state)
    if not teacher_view:
        sqs = np.multiply(sqs, np.greater(sqs, 1))

    tile_colors = [colordict['canvas'][sq] for row in sqs for sq in row]
    canvas_stim = visual.ElementArrayStim(win=w, 
                                        xys=canvas_locations, 
                                        colors = tile_colors,
                                        colorSpace='rgb255',
                                        fieldShape='sqr',
                                        nElements=36,
                                        elementMask=None,
                                        elementTex=None,
                                        sizes=(canv_sq_size, canv_sq_size*aspect))
    canvas_stim.draw()

def draw_cursor(row, col, colorkey, w):
    color = colordict['cursor'][colorkey]
    cursor_stim = visual.Rect(w, width=canv_sq_size*1.2, height=canv_sq_size*aspect*1.2, pos=(cx[col], cy[row]),
                            fillColor=color, colorSpace='rgb255',
                            interpolate=True)
    cursor_stim.draw()

##### DRAWING PROCEDURES #####
def draw_hypotheses(prob, order, w, teacher_view):
    # Draw hypotheses
    for idx, key in enumerate(order):
        h = prob[key]
        tile_colors = [colordict['hypothesis'][sq] for row in h for sq in row]
        h_stim = visual.ElementArrayStim(win=w, 
                                        xys=hypothesis_locations[idx], 
                                        colors = tile_colors,
                                        colorSpace='rgb255',
                                        fieldShape='sqr',
                                        nElements=36,
                                        elementMask=None,
                                        elementTex=None,
                                        sizes=(sq_size, sq_size*aspect))
        h_stim.draw()

    # Add letters on top
    letters = ['A', 'B', 'C', 'D']
    letter_locs = [(-.75, ltr_y0), (-.25, ltr_y0), (.25, ltr_y0), (.75, ltr_y0)]

    for letter, loc in zip(letters, letter_locs):
        letter_stim = visual.TextStim(win=w,
                                      text=letter,
                                      pos=loc,
                                      color='white')
        letter_stim.draw()
    
    # In teacher view: Highlight true hypothesis
    if teacher_view:
        true_h = order.index('A')
        true_h_border = visual.Rect(w,
                                    size=((6*sq_size + .085), (4/3)*(6*sq_size + .085)),
                                    lineWidth=30,
                                    lineColor=colordict['true'],
                                    colorSpace='rgb255',
                                    pos=hypothesis_centers[true_h]) 
        true_h_border.draw()

def draw_scale(w):
    # prompt
    scale_prompt = visual.TextStim(win=w, text="Suppose students saw just these hints.\nHow likely are they to get it right?",
                               pos=(0, .3),
                               height=.09,
                               wrapWidth=2)
    scale_prompt.draw()

    # scale
    scale_xs = np.linspace(-.66,.66,5)
    for i,x_i in enumerate(scale_xs):
        scale_stim = visual.TextStim(win=w,text=str(i+1), pos=(x_i,0), font='Menlo', height=.13)
        scale_stim.draw()

    # endpoints
    yestext = visual.TextStim(win=w, text="No chance", pos=(-.66, -.22), height=.08)
    yestext.draw()

    notext = visual.TextStim(win=w, text="Certainly", pos=(.66, -.22), height=.08)
    notext.draw()
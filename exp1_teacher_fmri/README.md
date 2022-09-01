# Teaching fMRI task
Natalia Vélez & Alicia Chen
August 2022

In order to run this task, you only need four files:

(1) `briefing_video.mp4` was played to explain the task to participants before they practiced the controls. If you want to explain the task face-to-face, you can also use the slides in `task_explanation.key`.

(2) `laptop_practice.sh` plays a practice, maze-solving task that participants can play to get used to operating the cursor. After participants solve the mazes, they then complete a brief run of the teaching task using practice problems that do not appear in the scanner task.

Usage:
```
bash laptop_practice.sh [subject:int]
```
Example:
```
bash laptop_practice.sh 1
```

(3) `scan_practice.sh` plays the same practice task, but using the key mappings of the button box, so that participants can additionally get used to the controls while inside the scanner. This task is normally played while the anatomical scan is being acquired. 

Usage:
```
bash scan_practice.sh [subject:int]
```

(4) Finally, `scan_session.sh` iterates through all 10 runs of the scanner task. You only need to specify the participant number as an integer; this script will then automatically iterate through each run.

Usage:
```
bash scan_session.sh [subject:int]
```

This folder also contains the following helper functions and inputs:

* `assets/`: Contains images used in task instructions
* `data/`: (Empty here) Saves behavioral data, including data from the practice task
* `inputs/`: Contains mazes and practice problems used during the practice tasks, as well as stimulus timings and orders for the main scanner task.
* `task_explanation.key`: Slideshow used to brief participants 
* `teaching_game_logic.py`: Controls the game logic (e.g., moving the cursor to a new square, detecting whether the square is a valid example or not)
* `teaching_mazes.py`: Code used to run practice task (navigating through simple mazes)
* `teaching_practice.py`: Code used to run a practice run of the teaching task
* `teaching_stimuli.py`: Contains functions used to draw stimuli on the screen
* `teaching_task.py`: Runs through a single run of the teaching task by calling on the modules listed above

After completing the teacher task, participants also completed two runs of an independent functional localizer. You can find the localizer task code and instructions on how to run it here:
https://saxelab.mit.edu/use-our-efficient-false-belief-localizer

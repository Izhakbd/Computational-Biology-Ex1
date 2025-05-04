# Computational-Biology-Ex1

# Instructions:
The user interface of the code is built for all three task stages and contains selection boxes and a selection menu that allows you to switch between the different task stages 

That is, there is a single executable file - main.exe , that appears in git under the dist folder.

To run, open the terminal in the path where the executable file is located and run the command ./main.exe
# For section 1:
There is a menu where you can select the percentage of white cells out of all the cells in the automaton (i.e. the chance that a cell will be white will be higher or lower)
You can select the number of generations in the menu designated for this purpose (the suggested range is 250-750). If a number lower than 250 or higher than 750 is selected, an error message will be thrown – since according to the requirements of the exercise, the automaton must run for at least 250 generations (and I gave an upper limit of 750 because beyond that, it is too heavy)
For this section, you can select the wraparound option of course, and see how the automaton is affected by this.
At the end of each run (after 250 generations by default), a graph of the stability index of the automaton will appear.
# For section 2:
There is a checkbox called "glider mode", when clicked, the initial positions that create the gliders appear in white, and the rest of the board in black.
You can combine this checkbox with the wraparound checkbox and see the effect on the behavior of the automaton.
# For section 3:
There is a checkbox called "traffic light mode", when clicked, the initial positions that create the traffic lights appear in white, and the rest of the board in black.
Also in this section, you can combine this checkbox with the wraparound checkbox and see the effect on the behavior of the automaton.

# Very important:
clicking the "glider mode" checkbox together with the "traffic light mode" checkbox creates unexpected behavior (where the gliders mix with the traffic lights) and therefore you should avoid checking both checkboxes at the same time.

# Enjoy!

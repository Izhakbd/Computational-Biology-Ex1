import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Parameters - you can change them and the behavior of automaton will change
size = 100 # size of grid
generations = 250 # number of generation in simulation
interval = 100  # Time between updates in milliseconds

# Initialize_grid with custome white-black ratio
def initialize_grid(size, white_ratio=0.75):
    return np.random.choice([0, 1], size=(size, size), p=[1 - white_ratio, white_ratio]).astype(bool)


# Update grid and return a new grid represent the next generation according the rules
def update_grid_blocks(grid, generation, wraparound):
    new_grid = grid.copy()
    size = grid.shape[0]
    offset = 0 if generation % 2 == 1 else 1 # check if we in odd genration or even generation

    # This function return the array represnt the current block (2*2) we handle.
    def get_block(i, j):
        top_left = grid[i % size][j % size]
        top_right = grid[i % size][(j + 1) % size]
        bottom_left = grid[(i + 1) % size][j % size]
        bottom_right = grid[(i + 1) % size][(j + 1) % size]
        return np.array([top_left,top_right,bottom_left,bottom_right])

    # This function apply cells from new grid who representing certain block to new array called block.
    def apply_block(i, j, block):
        new_grid[i % size][j % size] = block[0]
        new_grid[i % size][(j + 1) % size] = block[1]
        new_grid[(i + 1) % size][j % size] = block[2]
        new_grid[(i + 1) % size][(j + 1) % size] = block[3]

    # Define the row range and column range depending if we in wraparound mode or not.
    row_range = range(offset, size - 1, 2) if not wraparound else range(offset, size, 2)
    col_range = range(offset, size - 1, 2) if not wraparound else range(offset, size, 2)

    for i in row_range:
        for j in col_range:
            block = get_block(i, j) # Get the current block
            alive = np.sum(block) # Count how many rectangle in block alive
            if alive == 2:
                continue  # Do nothing
            elif alive in {0, 1, 4}:
                block = 1 - block  # Flip all values
            elif alive == 3: 
                block_matrix = (1 - block).reshape((2, 2))
                block = np.rot90(block_matrix, 2).flatten() # Flip all values and then rotate 180
            apply_block(i, j, block) # Update the cuurent block for new_grid represent the next generation

    return new_grid



# Tkinter GUI display the grid and track the progress of the metric during the generation
class GridDisplay(tk.Tk):
    #init the grid 
    def __init__(self, size, generations, interval):
        super().__init__()
        self.title("Grid Simulation")
        self.size = size
        self.generations = generations  # Number of generations for simulation
        self.interval = interval
        self.grid_data = initialize_grid(size)
        self.rect_size = 950 // size
        self.current_generation = 0
        self.metric_values = []
        self.running = False
        self.wraparound = tk.BooleanVar(value=False)  # Wraparound attribute
        self.stability_values = []  # Stability index over time
        self.glider_mode = tk.BooleanVar(value=False)  # Glider mode 
        self.traffic_light_mode = tk.BooleanVar(value=False) #Traffic Light mode

        # Create layout frames 
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left side: canvas for the grid
        self.canvas = tk.Canvas(main_frame, width=1000, height=1000)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Right side: control panel
        control_frame = tk.Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Add widgets to the control panel
        self.generation_label = ttk.Label(control_frame, text="Generation: 0")
        self.generation_label.pack(pady=5)

        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_simulation)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_simulation)
        self.stop_button.pack(pady=5)

        self.restart_button = ttk.Button(control_frame, text="Restart", command=self.restart_simulation)
        self.restart_button.pack(pady=5)

        # Wraparound attribiute , initalize as not wraparound
        self.wrap_checkbox = ttk.Checkbutton(control_frame, text="Wraparound", variable=self.wraparound)
        self.wrap_checkbox.pack(pady=5)

        # Checkbox who turn on glidermode
        self.glider_checkbox = ttk.Checkbutton(
            control_frame, text="Glider Mode", variable=self.glider_mode, command=self.on_glider_mode_toggle
        )
        self.glider_checkbox.pack(pady=5)

       # Checkbox to turn on Traffic Light mode
        self.traffic_light_checkbox = ttk.Checkbutton(
            control_frame, text="Traffic Light Mode", variable=self.traffic_light_mode, command=self.on_traffic_light_toggle
        )
        self.traffic_light_checkbox.pack(pady=5)



        self.create_grid()


    # Initializes the grid's visuals - creating all the rectangle in the grid with the color that suits them.
    def create_grid(self):
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                color = "white" if self.grid_data[i, j] else "black" # if grid[i,j] = 1 he will be white, else, he will be black
                self.canvas.create_rectangle(
                    j * self.rect_size, i * self.rect_size,
                    (j + 1) * self.rect_size, (i + 1) * self.rect_size,
                    fill=color, outline="gray"
                )

    # Runs the simulation according to the number of generations we defined in the begining
    def run_simulation(self):
        if self.running and self.current_generation < self.generations:
            prev_grid = self.grid_data.copy()
            self.grid_data = update_grid_blocks(self.grid_data, self.current_generation + 1, self.wraparound.get())
            
            # Calculate Stability Index
            stability = np.sum(prev_grid == self.grid_data) / (self.size * self.size) * 100
            self.stability_values.append(stability)
            self.create_grid()
            self.generation_label.config(text=f"Generation: {self.current_generation}")
            self.current_generation += 1
            # Use faster interval if glider mode is enabled
            interval = 1 if self.glider_mode.get() else self.interval
            self.after(interval, self.run_simulation)
        elif self.current_generation >= self.generations:
            self.show_indicators_graph()  # Plot indicators graph at the end of simulation

    # a button for starting the run
    def start_simulation(self):
        if not self.running:
            self.running = True
            self.run_simulation()

    # a button for stopping the run
    def stop_simulation(self):
        self.running = False

    # a button for restarting the run
    def restart_simulation(self):
        self.stop_simulation()
        self.grid_data = initialize_grid(self.size)
        
        if self.glider_mode.get(): # If glider mode is on
            # Create an all-black grid
            self.grid_data = np.zeros((self.size, self.size), dtype=bool)
            self.inject_glider() # Create white gliders
        elif self.traffic_light_mode.get(): # If traffic light mode is on
            self.grid_data = np.zeros((self.size, self.size), dtype=bool)
            self.inject_traffic_light() #Create trafficlight pattern
        else:
            # Regular random initialization
            self.grid_data = initialize_grid(self.size)

        self.current_generation = 0
        self.metric_values = []
        self.stability_values = []
        self.generation_label.config(text="Generation: 0")
        self.create_grid()

    def show_indicators_graph(self):
        plt.figure()
        # show the stability index when simulation end running
        if self.stability_values:
            plt.plot(range(len(self.stability_values)), self.stability_values, linestyle='--', linewidth=1, color='orange', label="Stability Index")
        plt.title("Simulation Metrics Over Time")
        plt.xlabel("Generations")
        plt.ylabel("Percentage of cells stayed in thier color")
        plt.legend()
        plt.grid(True)
        plt.show()

    # This function located the glider on the specific location on the grid
    def inject_glider(self):
        # Clear grid
        self.grid_data = np.zeros((self.size, self.size), dtype=bool)

        # Define a glider pattern and color the glider in white (1 = white)
        # Starting position of the gliders
        
        # Locate Glider in left up corner of grid - go from top to down
        self.grid_data[1, 1] = 1
        self.grid_data[2, 2] = 1
        self.grid_data[2, 3] = 1
        self.grid_data[1, 4] = 1

        # Locate Glider in middle left side of grid - go from left to right
        self.grid_data[51, 1] = 1
        self.grid_data[52, 2] = 1
        self.grid_data[53, 2] = 1
        self.grid_data[54, 1] = 1

         # Locate Glider in middle of grid - go from left to right
        self.grid_data[51, 51] = 1
        self.grid_data[52, 52] = 1
        self.grid_data[53, 52] = 1
        self.grid_data[54, 51] = 1

    # This functoin turn the all board to black except the glider when press on glider mode button
    def on_glider_mode_toggle(self):
        if self.glider_mode.get():
            # Switch to black grid with glider
            self.grid_data = np.zeros((self.size, self.size), dtype=bool)
            self.inject_glider()
            self.current_generation = 0
            self.stability_values = []
            self.metric_values = []
            self.generation_label.config(text="Generation: 0")
            self.create_grid()
        else:
            # If unmark, restart normally
            self.restart_simulation()



    def inject_traffic_light(self):
        # מצב רמזור 1
        # This example sets up a simple blinking "traffic light" block
        center = self.size // 2
        self.grid_data[center-1:center+2, center] = 1  # Vertical "traffic light"

        # 2 מצב רמזור 
        self.grid_data[60, 1] = 1
        self.grid_data[62, 2] = 1
        self.grid_data[63, 2] = 1
        self.grid_data[64, 1] = 1

        # 3 מצב רמזור 
        self.grid_data[80, 50] = 1
        self.grid_data[81, 51] = 1
        self.grid_data[82, 51] = 1
        self.grid_data[83, 50] = 1


    def on_traffic_light_toggle(self):
        if self.traffic_light_mode.get():
            self.grid_data = np.zeros((self.size, self.size), dtype=bool)
            self.inject_traffic_light()
            self.current_generation = 0
            self.stability_values = []
            self.metric_values = []
            self.generation_label.config(text="Generation: 0")
            self.create_grid()
        else:
            # If unmark, restart normally
            self.restart_simulation()


# Run the Tkinter GUI
simulation_prgram = GridDisplay(size, generations, interval)
simulation_prgram.mainloop()
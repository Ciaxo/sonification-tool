import pandas as pd
import matplotlib.pyplot as plt
from maping import map_range, map_data
from mid import str2midi, midi2str
from midiutil import MIDIFile
import pygame
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import power

class SonificationTool:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Sonification Tool")
        
        self.fig, self.ax = plt.subplots()
        self.create_widgets()
        self.configure_grid()
        pygame.init()
        self.data = None
        self.x_data = None
        self.y_data = None
        self.z_data = None
        self.what_data = None
        self.norm_x_data = None
        self.norm_y_data = None
        self.norm_z_data = None
        self.bit_data = None

        # Default tempo
        self.tempo = 60

        # Handling application closure
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Adding a label with information
        self.info_label = tk.Label(self.master, text="The X column will be automatically used as the time column",
                           font=("Arial", 12, "bold"), fg="white", bg="#4a90e2", pady=10)

        # Place the label in the first row, spanning the entire width
        self.info_label.grid(row=0, column=0, columnspan=99, sticky="ew")

        # Setting the appropriate column as expandable so that the label occupies the entire width
        self.master.grid_columnconfigure(0, weight=1)

        # Button for loading a data file in .csv format
        self.load_button = tk.Button(self.master, text="Load file CSV", command=self.load_csv)
        self.load_button.grid(row=1, column=0)

        # Field for selecting the X-axis
        self.x_label = tk.Label(self.master, text="Select X value:")
        self.x_label.grid(row=2, column=0)
        self.x_choice = tk.StringVar()
        self.x_menu = tk.OptionMenu(self.master, self.x_choice, (), command=self.update)
        self.x_menu.grid(row=2, column=1)

        # Field for selecting the Y-axis
        self.y_label = tk.Label(self.master, text="Select Y value:")
        self.y_label.grid(row=3, column=0)
        self.y_choice = tk.StringVar()
        self.y_menu = tk.OptionMenu(self.master, self.y_choice, (), command=self.update)
        self.y_menu.grid(row=3, column=1)

        # Selection of the field responsible for the dot size
        self.z_label = tk.Label(self.master, text="Dot size:")
        self.z_label.grid(row=4, column=0)
        self.z_choice = tk.StringVar()
        self.z_menu = tk.OptionMenu(self.master, self.z_choice, (), command=self.update)
        self.z_menu.grid(row=4, column=1)

        # Checkbox for reversing data and chart along the X-axis
        self.reverse_x_var = tk.BooleanVar()
        self.reverse_x_check = tk.Checkbutton(self.master, text="Reverse X-axis", variable=self.reverse_x_var, command=self.update)
        self.reverse_x_check.grid(row=5, column=0)

        # Checkbox for reversing data and chart along the Y-axis
        self.reverse_y_var = tk.BooleanVar()
        self.reverse_y_check = tk.Checkbutton(self.master, text="Reverse Y-axis", variable=self.reverse_y_var, command=self.update)
        self.reverse_y_check.grid(row=5, column=1)

        # Selection of the normalization axis
        self.norm_axis_label = tk.Label(self.master, text="Normalize along the axis:")
        self.norm_axis_label.grid(row=6, column=0)
        self.norm_axis_choice = tk.StringVar(value="Both")
        self.norm_axis_menu = tk.OptionMenu(self.master, self.norm_axis_choice, "Both", "X", "Y", command=self.update)
        self.norm_axis_menu.grid(row=6, column=1)

        # Selection of the normalization factor
        self.power_label = tk.Label(self.master, text="Degree of freedom  (e.g., 0.5):")
        self.power_label.grid(row=7, column=0)
        self.power_entry = tk.Entry(self.master)
        self.power_entry.grid(row=7, column=1)

        # Field for selecting the axis to apply the normalization factor
        self.power_axis_label = tk.Label(self.master, text="Select the axis for the degree of freedom:")
        self.power_axis_label.grid(row=8, column=0)
        self.power_axis_choice = tk.StringVar(value="X")
        self.power_axis_menu = tk.OptionMenu(self.master, self.power_axis_choice, "X", "Y")
        self.power_axis_menu.grid(row=8, column=1)

        # OK button to update the chart after normalization
        self.update_button = tk.Button(self.master, text="OK", command=self.update)
        self.update_button.grid(row=8, column=2)

        # Field for entering "Time/Beat"
        self.bit_length_label = tk.Label(self.master, text="Time/Beat:")
        self.bit_length_label.grid(row=9, column=0)
        self.bit_length_entry = tk.Entry(self.master)
        self.bit_length_entry.grid(row=9, column=1)

        # Pitch selection
        self.pitch_choice_label = tk.Label(self.master, text="Pitch:")
        self.pitch_choice_label.grid(row=10, column=0)
        self.pitch_var = tk.StringVar(self.master)
        self.pitch_var.set("Increasing")
        self.pitch_choice_menu = tk.OptionMenu(self.master, self.pitch_var, "Increasing", "Decreasing")
        self.pitch_choice_menu.grid(row=10, column=1)

        # Velocity selection
        self.volume_choice_label = tk.Label(self.master, text="Velocity:")
        self.volume_choice_label.grid(row=11, column=0)
        self.volume_var = tk.StringVar(self.master)
        self.volume_var.set("Increasing")
        self.volume_choice_menu = tk.OptionMenu(self.master, self.volume_var, "Increasing", "Decreasing", "Constant")
        self.volume_choice_menu.grid(row=11, column=1)

        # Field for selecting the tempo
        self.tempo_label = tk.Label(self.master, text="Tempo (BPM):")
        self.tempo_label.grid(row=12, column=0)
        self.tempo_entry = tk.Entry(self.master)
        self.tempo_entry.insert(0, "60")  # Default tempo.
        self.tempo_entry.grid(row=12, column=1)

        # Field for specifying the note range
        self.note_label = tk.Label(self.master, text="Note range (e.g., C2,D2,E2):")
        self.note_label.grid(row=13, column=0)
        self.note_entry = tk.Entry(self.master)
        self.note_entry.grid(row=13, column=1)

        # Field for specifying the minimum volume
        self.volume_min_label = tk.Label(self.master, text="Minimum volume (0-127):")
        self.volume_min_label.grid(row=14, column=0)
        self.volume_min_entry = tk.Entry(self.master)
        self.volume_min_entry.grid(row=14, column=1)

        # Field for specifying the maximum volume
        self.volume_max_label = tk.Label(self.master, text="Max volume (0-127):")
        self.volume_max_label.grid(row=15, column=0)
        self.volume_max_entry = tk.Entry(self.master)
        self.volume_max_entry.grid(row=15, column=1)

        # Button to save the result
        self.save_button = tk.Button(self.master, text="Save as MIDI", command=lambda: (self.update(), self.save_midi()))
        self.save_button.grid(row=16, column=0)

        # Button to play the MIDI file
        self.play_button = tk.Button(self.master, text="Play track", command=self.play_midi)
        self.play_button.grid(row=16, column=1)

        # Chart
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=17, column=0, columnspan=3, sticky="nsew")

        root.minsize(600, 1000) # Setting the minimum window size

    def configure_grid(self):
        """Allows dynamic scaling of the window content."""
        for i in range(18):  # 18 rows
            self.master.grid_rowconfigure(i, weight=1)
        for j in range(3):  # 3 columns
            self.master.grid_columnconfigure(j, weight=1)


    def load_csv(self):
        """Loads a CSV file and updates the selection options for X-axis, Y-axis, dot size (Z), and the column for calculating the track length."""
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Opens a dialog window to select a CSV file
        if filepath:
            self.data = pd.read_csv(filepath)  # Loads data from the CSV file
            self.x_choice.set("")  # Resets axis selections
            self.y_choice.set("")
            self.z_choice.set("")
            self.x_menu["menu"].delete(0, "end")  # Removes previous options from the menu
            self.y_menu["menu"].delete(0, "end")
            self.z_menu["menu"].delete(0, "end")
            for col in self.data.columns:  # Adds CSV columns as selectable options for axes
                self.x_menu["menu"].add_command(label=col, command=lambda value=col: self.update_choice('x', value))
                self.y_menu["menu"].add_command(label=col, command=lambda value=col: self.update_choice('y', value))
                self.z_menu["menu"].add_command(label=col, command=lambda value=col: self.update_choice('z', value))

    def update_choice(self, axis, value):
        """Updates the value selection for the chosen axis and refreshes normalization."""
        if axis == 'x':
            self.x_choice.set(value)
 
        elif axis == 'y':
            self.y_choice.set(value)

        elif axis == 'z':
            self.z_choice.set(value)

        self.update()  # Refreshes data after selection change

    def update(self, _=None):
        """Calls data processing functions based on the user's current selections."""
        self.apply_axis_reversal()
        self.apply_normalization()
        self.apply_power()
        self.calculate_bit_data()
        self.update_plot()

    def apply_axis_reversal(self):
        """Reverses data on the X and Y axes if the inversion options are selected."""
        if self.data is not None and self.x_choice.get() and self.y_choice.get():
            self.x_data = self.data[self.x_choice.get()]
            self.y_data = self.data[self.y_choice.get()]

            if self.reverse_x_var.get():
                self.x_data = max(self.x_data) - self.x_data
            if self.reverse_y_var.get():
                self.y_data = max(self.y_data) - self.y_data

    def apply_normalization(self):
        """Normalizes data based on the selected axis."""
        if self.data is not None:
            norm_axis = self.norm_axis_choice.get()
            if norm_axis == "X" or norm_axis == "Both":
                self.norm_x_data = map_range(self.x_data, 0, 1)
            else:
                self.norm_x_data = self.x_data

            if norm_axis == "Y" or norm_axis == "Both":
                self.norm_y_data = map_range(self.y_data, 0, 1)
            else:
                self.norm_y_data = self.y_data

            if self.z_choice.get():
                self.z_data = self.data[self.z_choice.get()]
                self.norm_z_data = map_range(self.z_data, 0, 1)
            else:
                self.norm_z_data = None

    def apply_power(self):
        """Applies the degree of freedom to the selected axis."""
        try:
            powerr = float(self.power_entry.get()) if self.power_entry.get() else 1.0
        except ValueError:
            messagebox.showerror("Error", "The degree of freedom must be a number.")
            return

        power_axis = self.power_axis_choice.get()

        if power_axis == "X" and self.norm_x_data is not None:
            self.norm_x_data = power(self.norm_x_data, powerr)
        elif power_axis == "Y" and self.norm_y_data is not None:
            self.norm_y_data = power(self.norm_y_data, powerr)

    def calculate_bit_data(self):

        """Calculates track length data based on the "Time/Beat" value and the selected column."""
        if self.data is not None and self.bit_length_entry.get():
            try:
                bit_length = float(self.bit_length_entry.get())  # Get the 'Time/Beat' value.

                self.bit_data = self.x_data / bit_length

                self.bit_data -= min(self.bit_data)  # Shifting the minimum value to 0

            except ValueError:
                messagebox.showerror("Error", "The 'Time/Beat' value must be a number.")

    def update_plot(self):
        """Updates the chart, displaying normalized data and column names."""
        self.ax.clear()
        if self.norm_z_data is not None:
            self.ax.scatter(self.norm_x_data, self.norm_y_data, s=self.norm_z_data * 100)
        else:
            self.ax.scatter(self.norm_x_data, self.norm_y_data)
    
        # Adding columns at the bottom of the chart
        x_label = self.x_choice.get().capitalize() if self.x_choice.get() else "No data for the X-axis"
        y_label = self.y_choice.get().capitalize() if self.y_choice.get() else "No data for the Y-axis"
        z_label = self.z_choice.get().capitalize() if self.z_choice.get() else "No data for dot size"
        self.ax.set_xlabel(f"X-axis: {x_label}")
        self.ax.set_ylabel(f"Y-axis: {y_label}")
        self.ax.set_title(f"Dot size: {z_label}")

        self.canvas.draw()

    def save_midi(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load data before saving.")
            return
        
        print("Starting saving...")
        
        try:
            self.tempo = int(self.tempo_entry.get())
            if self.tempo < 1 or self.tempo > 300:
                raise ValueError("Tempo must be in the range of 1-300.")
        except ValueError:
            messagebox.showerror("Error", "Tempo must be an integer in the range of 1-300.")
            return

        norm_axis = self.norm_axis_choice.get()
        if norm_axis == "X":
            source_data = self.norm_x_data
        elif norm_axis == "Y":
            source_data = self.norm_y_data
        else:
            source_data = self.norm_x_data + self.norm_y_data

        notes_range = self.note_entry.get()
        midi_notes1 = [note.strip() for note in notes_range.split(',')]
        midi_notes = [str2midi(n) for n in midi_notes1]
        
        wynikMidi = []
        newMin, newMax = len(midi_notes) - 1, 0
        
        reverse_pitch = (self.pitch_var.get() == "Decreasing")
        print("Pitch: ", self.pitch_var.get())
        wynikMidi = map_data(source_data, newMin, newMax, reverse=reverse_pitch)
        wynikMidi = [midi_notes[n] for n in wynikMidi]
        
        minVol = int(self.volume_min_entry.get())
        maxVol = int(self.volume_max_entry.get())
        
        volumes = []
        reverse_volume = self.volume_var.get()
        print("Velocity: ", reverse_volume)
        if reverse_volume == "Constant":
            volumes = [maxVol] * len(source_data)
        else:
            volumes = map_data(source_data, minVol, maxVol, reverse=reverse_volume == "Decreasing")
        
        track = 0
        channel = 0
        time = 0
        
        MyMIDI = MIDIFile(1)
        MyMIDI.addTrackName(track, time, "Sample Track")
        MyMIDI.addTempo(track, time, self.tempo)
        
        for j in range(len(self.bit_data)):
            MyMIDI.addNote(track, channel, time=self.bit_data[j], pitch=wynikMidi[j], volume=volumes[j], duration=2)
        
        # Getting the file name from the user.
        filename = simpledialog.askstring("Save as", "Enter the file name (without extension):")
        if not filename:
            messagebox.showwarning("Canceled", "No file name provided. Save aborted.")
            return

        filepath = f"{filename}.mid"

        with open(filepath, "wb") as output_file:
            MyMIDI.writeFile(output_file)

        messagebox.showinfo("Success", f"File saved as {filepath}")

    def play_midi(self):
        """Opens a file selection window and plays the selected MIDI file."""
        file_path = filedialog.askopenfilename(
            title="Select a MIDI file",
            filetypes=[("MIDI files", "*.mid")]
        )

        if not file_path:
            return  # The user canceled the selection

        try:
            pygame.mixer.music.load(file_path)  # Loading the selected MIDI file
            pygame.mixer.music.play()  # Plays the MIDI file
        except Exception as e:
            messagebox.showerror("Error", f"Unable to play the MIDI file.\n{e}")

    def on_closing(self):
        """Function that will be called when the window is closed."""
        pygame.quit()  # Stop Pygame
        self.master.destroy()  # Zniszcz okno Tkinter
        exit()  # Completely terminates the program

if __name__ == "__main__":
    root = tk.Tk()
    app = SonificationTool(master=root)  # Creates an instance of the SonificationTool class
    root.mainloop()  # Runs the main Tkinter event loop, allowing user interaction

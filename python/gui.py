import tkinter as tk
from tkinter import ttk, messagebox
from main_controller import SchedulerSystem
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Scheduling Optimizer")
        self.root.geometry("1000x700")
        
        self.system = SchedulerSystem()
        self.create_widgets()
    
    def create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Process Input", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Process Table
        self.tree = ttk.Treeview(input_frame, columns=("PID", "Arrival", "Burst", "Priority"), show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Burst", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.grid(row=0, column=0, columnspan=4, pady=5)
        
        # Add Process Controls
        ttk.Label(input_frame, text="Arrival:").grid(row=1, column=0)
        self.arrival_entry = ttk.Entry(input_frame, width=10)
        self.arrival_entry.grid(row=1, column=1)
        
        ttk.Label(input_frame, text="Burst:").grid(row=1, column=2)
        self.burst_entry = ttk.Entry(input_frame, width=10)
        self.burst_entry.grid(row=1, column=3)
        
        ttk.Label(input_frame, text="Priority:").grid(row=1, column=4)
        self.priority_entry = ttk.Entry(input_frame, width=10)
        self.priority_entry.grid(row=1, column=5)
        
        add_btn = ttk.Button(input_frame, text="Add Process", command=self.add_process)
        add_btn.grid(row=1, column=6, padx=5)
        
        del_btn = ttk.Button(input_frame, text="Remove Selected", command=self.remove_process)
        del_btn.grid(row=1, column=7)
        
        # Time Quantum
        ttk.Label(input_frame, text="Time Quantum (RR):").grid(row=2, column=0, pady=10)
        self.quantum_entry = ttk.Entry(input_frame, width=10)
        self.quantum_entry.insert(0, "2")  # Default value
        self.quantum_entry.grid(row=2, column=1)
        
        # Action Buttons
        run_btn = ttk.Button(input_frame, text="Run Scheduler", command=self.run_scheduler)
        run_btn.grid(row=2, column=2, columnspan=2, pady=10)
        
        # Results Frame
        result_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.result_text = tk.Text(result_frame, height=10, width=80)
        self.result_text.grid(row=0, column=0)
        
        # Gantt Chart Frame
        self.gantt_frame = ttk.Frame(result_frame)
        self.gantt_frame.grid(row=1, column=0, pady=10)
    
    def add_process(self):
        try:
            pid = len(self.tree.get_children())
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get())
            
            self.tree.insert("", "end", values=(pid, arrival, burst, priority))
            
            # Clear entries
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def remove_process(self):
        selected = self.tree.selection()
        if selected:
            self.tree.delete(selected)
    
    def run_scheduler(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", "No processes added")
            return
        
        try:
            # Prepare input data
            processes = []
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                processes.append({
                    "pid": values[0],
                    "arrival_time": values[1],
                    "burst_time": values[2],
                    "priority": values[3]
                })
            
            input_data = {
                "num_processes": len(processes),
                "processes": processes,
                "time_quantum": int(self.quantum_entry.get()),
                "stats": self.system.calculate_stats(processes)
            }
            
            # Run prediction
            best_algo = self.system.predictor.predict(input_data)
            
            # Run algorithm
            results = self.system.run_algorithm(best_algo, input_data)
            
            # Display results
            self.show_results(best_algo, results)
            
            # Show Gantt chart
            self.plot_gantt(results)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_results(self, algorithm, results):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Recommended Algorithm: {algorithm.upper()}\n\n")
        self.result_text.insert(tk.END, json.dumps(results, indent=2))
    
    def plot_gantt(self, results):
        # Clear previous chart
        for widget in self.gantt_frame.winfo_children():
            widget.destroy()
        
        # Prepare data
        processes = sorted(results['processes'], key=lambda x: x['completion_time'])
        fig, ax = plt.subplots(figsize=(10, 2))
        
        for i, p in enumerate(processes):
            start = p['completion_time'] - p['turnaround_time']
            ax.barh(y=p['pid'], width=p['burst_time'], left=start, height=0.5, align='center')
            ax.text(start + p['burst_time']/2, p['pid'], f"P{p['pid']}", ha='center', va='center')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_title('Gantt Chart')
        ax.grid(True)
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.gantt_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
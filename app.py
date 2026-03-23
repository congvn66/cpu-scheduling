import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1000x600")

        self.processes = []
        self.timeline = []

        self.create_widgets()

    # ================= UI =================
    def create_widgets(self):
        # ===== TOP BAR =====
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(top_frame, text="Load CSV", command=self.load_file).pack(side="left")

        self.algo_box = ttk.Combobox(top_frame, values=["FCFS", "SJF Nonpreemtive", "SJF Preemtive", "Round Robin", "Priority Preemtive", "Priority Nonpreemtive"])
        self.algo_box.current(0)
        self.algo_box.pack(side="left", padx=10)

        tk.Label(top_frame, text="Quantum:").pack(side="left")
        self.quantum_entry = tk.Entry(top_frame, width=5)
        self.quantum_entry.pack(side="left", padx=5)

        tk.Button(top_frame, text="Run", command=self.run_algorithm).pack(side="left", padx=10)

        # ===== TABLE =====
    
        columns = ("ID", "Arrival", "Burst", "Priority", "Waiting", "Turnaround", "Response")

        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # ===== STATS =====
        self.stats_label = tk.Label(self.root, text="Stats will appear here")
        self.stats_label.pack(pady=5)

        # ===== GANTT =====
        gantt_frame = tk.Frame(self.root)
        gantt_frame.pack(fill="x", padx=10, pady=10)

        self.canvas = tk.Canvas(gantt_frame, height=150, bg="white")
        scrollbar = tk.Scrollbar(gantt_frame, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(xscrollcommand=scrollbar.set)

        self.canvas.pack(side="top", fill="x")
        scrollbar.pack(side="bottom", fill="x")

    # ================= FILE =================
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        self.processes.clear()

        try:
            with open(file_path, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pid = int(row['id'])
                    arrival = int(row['arrival'])
                    burst = int(row['burst'])
                    priority = row.get('priority')
                    priority = int(priority) if priority else None

                    # Create process from your own class
                    from process import Process
                    p = Process(id = pid, arrival = arrival, burst = burst, priority=priority)
                    self.processes.append(p)

            self.update_table()
            messagebox.showinfo("Success", "File loaded successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= RUN =================
    def run_algorithm(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Load data first")
            return

        algo = self.algo_box.get()

        try:
            if algo == "FCFS":
                from fcfs import FCFS
                scheduler = FCFS(self.clone_processes())

            elif algo == "SJF Nonpreemtive":
                from sjf_nonpreemtive import SJFNonPreemtive
                scheduler = SJFNonPreemtive(self.clone_processes())

            elif algo == "SJF Preemtive":
                from sjf_preemtive import SJFPreemtive
                scheduler = SJFPreemtive(self.clone_processes())

            elif algo == "Round Robin":
                from rr import RoundRobin
                q = int(self.quantum_entry.get())
                scheduler = RoundRobin(self.clone_processes(), q)

            elif algo == "Priority Preemtive":
                from priority_preemtive import PriorityPreemtive
                scheduler = PriorityPreemtive(self.clone_processes())

            elif algo == "Priority Nonpreemtive":
                from priority_nonpreemtive import PriorityNonPreemtive
                scheduler = PriorityNonPreemtive(self.clone_processes())
            else:
                return

            self.timeline = scheduler.run()

            self.update_table(scheduler.processes)
            self.update_stats(scheduler)
            self.draw_gantt(self.timeline)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= TABLE =================
    def update_table(self, processes=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        processes = processes if processes else self.processes

        for p in processes:
            self.tree.insert("", "end", values=(
                p.id,
                p.arrival,
                p.burst,
                p.priority if p.priority is not None else "",
                getattr(p, 'waiting', ''),
                getattr(p, 'turnaround', ''),
                getattr(p, 'response', '')
            ))

    # ================= STATS =================
    def update_stats(self, scheduler):
        text = f"Avg Waiting: {scheduler.avg_waiting():.2f} | " \
               f"Avg Turnaround: {scheduler.avg_turnaround():.2f} | " \
               f"Avg Response: {scheduler.avg_response():.2f}"

        self.stats_label.config(text=text)

    # ================= GANTT =================
    def draw_gantt(self, timeline):
        self.canvas.delete("all")

        if not timeline:
            return

        # ===== CONFIG =====
        scale = 40
        height = 40
        min_width = 25
        colors = ["#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CC99FF"]

        # ===== CANVAS SIZE =====
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        y = canvas_height // 2 - height // 2  # căn giữa theo chiều dọc

        # ===== TOTAL WIDTH =====
        last_time = timeline[-1][2]
        total_width = last_time * scale

        # ===== OFFSET (căn giữa ngang) =====
        offset = max((canvas_width - total_width) / 2, 0)

        for pid, start, end in timeline:
            width = max((end - start) * scale, min_width)

            x1 = offset + start * scale
            x2 = x1 + width

            label = "IDLE" if pid == -1 else str(pid)
            color = "lightgray" if pid == -1 else colors[pid % len(colors)]

            # rectangle
            self.canvas.create_rectangle(
                x1, y, x2, y + height,
                fill=color,
                outline="black"
            )

            # process label
            self.canvas.create_text(
                (x1 + x2) / 2, y + height / 2,
                text=label,
                font=("Arial", 10, "bold")
            )

            # time start
            self.canvas.create_text(
                x1, y + height + 15,
                text=str(start),
                font=("Arial", 9)
            )

        # time cuối
        self.canvas.create_text(
            offset + last_time * scale,
            y + height + 15,
            text=str(last_time),
            font=("Arial", 9)
        )

        # ===== SCROLL REGION =====
        self.canvas.config(
            scrollregion=(0, 0, total_width + offset * 2 + 50, canvas_height)
        )

    # ================= UTIL =================
    def clone_processes(self):
        from process import Process
        return [Process(id = p.id, arrival = p.arrival, burst=p.burst, priority=p.priority) for p in self.processes]


# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk


# ---------------- FIFO Algorithm ----------------
def fifo_page_replacement(pages, frame_count):
    frames = []
    queue_index = 0
    faults = 0
    hits = 0
    steps = []

    for page in pages:
        if page in frames:
            hits += 1
            status = "HIT"
        else:
            faults += 1
            status = "FAULT"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames[queue_index] = page
                queue_index = (queue_index + 1) % frame_count

        steps.append((page, frames.copy(), status))

    return steps, faults, hits


# ---------------- LRU Algorithm ----------------
def lru_page_replacement(pages, frame_count):
    frames = []
    recent = {}
    faults = 0
    hits = 0
    steps = []

    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "HIT"
        else:
            faults += 1
            status = "FAULT"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                # Find least recently used page
                lru_page = min(frames, key=lambda p: recent.get(p, -1))
                lru_index = frames.index(lru_page)
                frames[lru_index] = page

        recent[page] = i
        steps.append((page, frames.copy(), status))

    return steps, faults, hits


# ---------------- GUI Functions ----------------
def clear_output():
    for row in tree.get_children():
        tree.delete(row)
    result_label.config(text="")
    algo_label.config(text="Algorithm Output:")


def parse_input():
    try:
        frame_count = int(frame_entry.get().strip())
        if frame_count <= 0:
            raise ValueError

        ref_string = ref_entry.get().strip()
        pages = list(map(int, ref_string.split()))

        if len(pages) == 0:
            raise ValueError

        return pages, frame_count

    except:
        messagebox.showerror("Invalid Input", "Please enter valid frames and reference string.\nExample: 7 0 1 2 0 3")
        return None, None


def display_steps(steps, frame_count):
    clear_output()

    # Set columns dynamically based on frame count
    columns = ["Step", "Page"] + [f"Frame {i+1}" for i in range(frame_count)] + ["Status"]
    tree["columns"] = columns

    tree.heading("#0", text="")
    tree.column("#0", width=0, stretch=tk.NO)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=90)

    for i, (page, frames, status) in enumerate(steps, start=1):
        row = [i, page]

        # Fill missing frames with "-"
        frames_display = frames + ["-"] * (frame_count - len(frames))
        row.extend(frames_display)
        row.append(status)

        tree.insert("", "end", values=row)


def run_fifo():
    pages, frame_count = parse_input()
    if pages is None:
        return

    steps, faults, hits = fifo_page_replacement(pages, frame_count)
    display_steps(steps, frame_count)

    total = len(pages)
    hit_ratio = (hits / total) * 100

    algo_label.config(text="Algorithm Output: FIFO")
    result_label.config(
        text=f"Total Pages: {total} | Hits: {hits} | Faults: {faults} | Hit Ratio: {hit_ratio:.2f}%"
    )


def run_lru():
    pages, frame_count = parse_input()
    if pages is None:
        return

    steps, faults, hits = lru_page_replacement(pages, frame_count)
    display_steps(steps, frame_count)

    total = len(pages)
    hit_ratio = (hits / total) * 100

    algo_label.config(text="Algorithm Output: LRU")
    result_label.config(
        text=f"Total Pages: {total} | Hits: {hits} | Faults: {faults} | Hit Ratio: {hit_ratio:.2f}%"
    )


def run_both():
    pages, frame_count = parse_input()
    if pages is None:
        return

    fifo_steps, fifo_faults, fifo_hits = fifo_page_replacement(pages, frame_count)
    lru_steps, lru_faults, lru_hits = lru_page_replacement(pages, frame_count)

    # Show FIFO steps first
    display_steps(fifo_steps, frame_count)

    total = len(pages)
    fifo_hit_ratio = (fifo_hits / total) * 100
    lru_hit_ratio = (lru_hits / total) * 100

    better = "FIFO" if fifo_faults < lru_faults else "LRU" if lru_faults < fifo_faults else "Both Equal"

    algo_label.config(text="Algorithm Output: FIFO (Comparison Mode)")
    result_label.config(
        text=f"FIFO -> Hits: {fifo_hits}, Faults: {fifo_faults}, Hit Ratio: {fifo_hit_ratio:.2f}%  |  "
             f"LRU -> Hits: {lru_hits}, Faults: {lru_faults}, Hit Ratio: {lru_hit_ratio:.2f}%  |  "
             f"Better: {better}"
    )


# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Virtual Memory Paging Simulator (FIFO vs LRU)")
root.geometry("1000x600")
root.config(bg="#f2f2f2")

title = tk.Label(root, text="Virtual Memory Paging Simulator", font=("Arial", 20, "bold"), bg="#f2f2f2")
title.pack(pady=10)

frame_top = tk.Frame(root, bg="#f2f2f2")
frame_top.pack(pady=5)

tk.Label(frame_top, text="Number of Frames:", font=("Arial", 12), bg="#f2f2f2").grid(row=0, column=0, padx=5, pady=5)
frame_entry = tk.Entry(frame_top, font=("Arial", 12), width=10)
frame_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Reference String:", font=("Arial", 12), bg="#f2f2f2").grid(row=0, column=2, padx=5, pady=5)
ref_entry = tk.Entry(frame_top, font=("Arial", 12), width=50)
ref_entry.grid(row=0, column=3, padx=5, pady=5)

# Buttons
frame_buttons = tk.Frame(root, bg="#f2f2f2")
frame_buttons.pack(pady=10)

btn_fifo = tk.Button(frame_buttons, text="Run FIFO", font=("Arial", 12), width=12, command=run_fifo, bg="#4CAF50", fg="white")
btn_fifo.grid(row=0, column=0, padx=10)

btn_lru = tk.Button(frame_buttons, text="Run LRU", font=("Arial", 12), width=12, command=run_lru, bg="#2196F3", fg="white")
btn_lru.grid(row=0, column=1, padx=10)

btn_both = tk.Button(frame_buttons, text="Compare Both", font=("Arial", 12), width=14, command=run_both, bg="#FF9800", fg="white")
btn_both.grid(row=0, column=2, padx=10)

btn_clear = tk.Button(frame_buttons, text="Clear", font=("Arial", 12), width=12, command=clear_output, bg="#f44336", fg="white")
btn_clear.grid(row=0, column=3, padx=10)

# Output Label
algo_label = tk.Label(root, text="Algorithm Output:", font=("Arial", 14, "bold"), bg="#f2f2f2")
algo_label.pack(pady=5)

# Table
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill="both", expand=True)

tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
tree.pack(fill="both", expand=True)

tree_scroll.config(command=tree.yview)

# Result summary
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f2f2f2", fg="black")
result_label.pack(pady=10)

root.mainloop()

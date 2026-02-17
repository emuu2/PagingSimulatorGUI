import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt


# ---------------- FIFO Algorithm ----------------
def fifo_page_replacement(pages, frame_count):
    frames = []
    queue_index = 0
    faults = 0
    hits = 0
    steps = []
    log = []

    for step, page in enumerate(pages, start=1):
        if page in frames:
            hits += 1
            status = "HIT"
            log.append(f"Step {step}: Page {page} -> HIT (already in memory)")
        else:
            faults += 1
            status = "FAULT"

            if len(frames) < frame_count:
                frames.append(page)
                log.append(f"Step {step}: Page {page} -> FAULT (loaded into empty frame)")
            else:
                replaced = frames[queue_index]
                frames[queue_index] = page
                log.append(f"Step {step}: Page {page} -> FAULT (replaced {replaced} using FIFO)")
                queue_index = (queue_index + 1) % frame_count

        steps.append((page, frames.copy(), status))

    return steps, faults, hits, log


# ---------------- LRU Algorithm ----------------
def lru_page_replacement(pages, frame_count):
    frames = []
    recent = {}
    faults = 0
    hits = 0
    steps = []
    log = []

    for i, page in enumerate(pages):
        step = i + 1

        if page in frames:
            hits += 1
            status = "HIT"
            log.append(f"Step {step}: Page {page} -> HIT (already in memory)")
        else:
            faults += 1
            status = "FAULT"

            if len(frames) < frame_count:
                frames.append(page)
                log.append(f"Step {step}: Page {page} -> FAULT (loaded into empty frame)")
            else:
                lru_page = min(frames, key=lambda p: recent.get(p, -1))
                idx = frames.index(lru_page)
                frames[idx] = page
                log.append(f"Step {step}: Page {page} -> FAULT (replaced {lru_page} using LRU)")

        recent[page] = i
        steps.append((page, frames.copy(), status))

    return steps, faults, hits, log


# ---------------- OPTIMAL Algorithm ----------------
def optimal_page_replacement(pages, frame_count):
    frames = []
    faults = 0
    hits = 0
    steps = []
    log = []

    for i, page in enumerate(pages):
        step = i + 1

        if page in frames:
            hits += 1
            status = "HIT"
            log.append(f"Step {step}: Page {page} -> HIT (already in memory)")
        else:
            faults += 1
            status = "FAULT"

            if len(frames) < frame_count:
                frames.append(page)
                log.append(f"Step {step}: Page {page} -> FAULT (loaded into empty frame)")
            else:
                future = pages[i + 1:]
                farthest_index = -1
                replace_page = None

                for f in frames:
                    if f in future:
                        next_use = future.index(f)
                    else:
                        next_use = float('inf')

                    if next_use > farthest_index:
                        farthest_index = next_use
                        replace_page = f

                idx = frames.index(replace_page)
                frames[idx] = page
                log.append(f"Step {step}: Page {page} -> FAULT (replaced {replace_page} using OPTIMAL)")

        steps.append((page, frames.copy(), status))

    return steps, faults, hits, log


# ---------------- LFU Algorithm ----------------
def lfu_page_replacement(pages, frame_count):
    frames = []
    freq = {}
    time = {}
    faults = 0
    hits = 0
    steps = []
    log = []

    for i, page in enumerate(pages):
        step = i + 1

        if page in frames:
            hits += 1
            freq[page] += 1
            time[page] = i
            status = "HIT"
            log.append(f"Step {step}: Page {page} -> HIT (frequency increased)")
        else:
            faults += 1
            status = "FAULT"

            if len(frames) < frame_count:
                frames.append(page)
                freq[page] = 1
                time[page] = i
                log.append(f"Step {step}: Page {page} -> FAULT (loaded into empty frame)")
            else:
                victim = min(frames, key=lambda p: (freq[p], time[p]))
                idx = frames.index(victim)

                log.append(f"Step {step}: Page {page} -> FAULT (replaced {victim} using LFU)")

                del freq[victim]
                del time[victim]

                frames[idx] = page
                freq[page] = 1
                time[page] = i

        steps.append((page, frames.copy(), status))

    return steps, faults, hits, log


# ---------------- GUI Helper Functions ----------------
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
        messagebox.showerror("Invalid Input",
                             "Enter valid frames and reference string.\nExample: 7 0 1 2 0 3 0 4")
        return None, None


def clear_output():
    for row in tree.get_children():
        tree.delete(row)

    for row in compare_tree.get_children():
        compare_tree.delete(row)

    algo_label.config(text="Algorithm Output:")
    result_label.config(text="")
    log_text.delete("1.0", tk.END)


def display_steps(steps, frame_count):
    for row in tree.get_children():
        tree.delete(row)

    columns = ["Step", "Page"] + [f"Frame {i+1}" for i in range(frame_count)] + ["Status"]
    tree["columns"] = columns

    tree.heading("#0", text="")
    tree.column("#0", width=0, stretch=tk.NO)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=90)

    for i, (page, frames, status) in enumerate(steps, start=1):
        row = [i, page]
        frames_display = frames + ["-"] * (frame_count - len(frames))
        row.extend(frames_display)
        row.append(status)
        tree.insert("", "end", values=row)


def display_log(log_lines):
    log_text.delete("1.0", tk.END)
    for line in log_lines:
        log_text.insert(tk.END, line + "\n")


# ---------------- Run Algorithm Buttons ----------------
def run_fifo():
    pages, frame_count = parse_input()
    if pages is None:
        return

    steps, faults, hits, log = fifo_page_replacement(pages, frame_count)
    display_steps(steps, frame_count)
    display_log(log)

    total = len(pages)
    hit_ratio = (hits / total) * 100

    algo_label.config(text="Algorithm Output: FIFO")
    result_label.config(text=f"Total Pages: {total} | Hits: {hits} | Faults: {faults} | Hit Ratio: {hit_ratio:.2f}%")


def run_lru():
    pages, frame_count = parse_input()
    if pages is None:
        return

    steps, faults, hits, log = lru_page_replacement(pages, frame_count)
    display_steps(steps, frame_count)
    display_log(log)

    total = len(pages)
    hit_ratio = (hits / total) * 100

    algo_label.config(text="Algorithm Output: LRU")
    result_label.config(text=f"Total Pages: {total} | Hits: {hits} | Faults: {faults} | Hit Ratio: {hit_ratio:.2f}%")


def run_optimal():
    pages, frame_count = parse_input()
    if pages is None:
        return

    steps, faults, hits, log = optimal_page_replacement(pages, frame_count)
    display_steps(steps, frame_count)
    display_log(log)

    total = len(pages)
    hit_ratio = (hits / total) * 100

    algo_label.config(text="Algorithm Output: OPTIMAL")
    result_label.config(text=f"Total Pages: {total} | Hits: {hits} | Faults: {faults} | Hit Ratio: {hit_ratio:.2f}%")


def run_lfu():
    pages, frame_count = parse_input()
    if pages is None:
        return

    steps, faults, hits, log = lfu_page_replacement(pages, frame_count)
    display_steps(steps, frame_count)
    display_log(log)

    total = len(pages)
    hit_ratio = (hits / total) * 100

    algo_label.config(text="Algorithm Output: LFU")
    result_label.config(text=f"Total Pages: {total} | Hits: {hits} | Faults: {faults} | Hit Ratio: {hit_ratio:.2f}%")


def compare_all():
    pages, frame_count = parse_input()
    if pages is None:
        return

    fifo_steps, fifo_faults, fifo_hits, fifo_log = fifo_page_replacement(pages, frame_count)
    lru_steps, lru_faults, lru_hits, lru_log = lru_page_replacement(pages, frame_count)
    opt_steps, opt_faults, opt_hits, opt_log = optimal_page_replacement(pages, frame_count)
    lfu_steps, lfu_faults, lfu_hits, lfu_log = lfu_page_replacement(pages, frame_count)

    # Show FIFO steps in main table
    display_steps(fifo_steps, frame_count)
    display_log(fifo_log)

    total = len(pages)

    fifo_hr = (fifo_hits / total) * 100
    lru_hr = (lru_hits / total) * 100
    opt_hr = (opt_hits / total) * 100
    lfu_hr = (lfu_hits / total) * 100

    best = min(
        [("FIFO", fifo_faults), ("LRU", lru_faults), ("OPTIMAL", opt_faults), ("LFU", lfu_faults)],
        key=lambda x: x[1]
    )[0]

    algo_label.config(text="Algorithm Output: FIFO (Comparison Mode)")

    # Clear old comparison rows
    for row in compare_tree.get_children():
        compare_tree.delete(row)

    compare_tree.insert("", "end", values=("FIFO", fifo_hits, fifo_faults, f"{fifo_hr:.2f}"))
    compare_tree.insert("", "end", values=("LRU", lru_hits, lru_faults, f"{lru_hr:.2f}"))
    compare_tree.insert("", "end", values=("OPTIMAL", opt_hits, opt_faults, f"{opt_hr:.2f}"))
    compare_tree.insert("", "end", values=("LFU", lfu_hits, lfu_faults, f"{lfu_hr:.2f}"))

    result_label.config(text=f"Best Algorithm (Minimum Faults): {best}")


def show_graph():
    pages, frame_count = parse_input()
    if pages is None:
        return

    _, fifo_faults, _, _ = fifo_page_replacement(pages, frame_count)
    _, lru_faults, _, _ = lru_page_replacement(pages, frame_count)
    _, opt_faults, _, _ = optimal_page_replacement(pages, frame_count)
    _, lfu_faults, _, _ = lfu_page_replacement(pages, frame_count)

    algorithms = ["FIFO", "LRU", "OPTIMAL", "LFU"]
    faults = [fifo_faults, lru_faults, opt_faults, lfu_faults]

    plt.figure(figsize=(7, 5))
    plt.bar(algorithms, faults)
    plt.title("Page Fault Comparison")
    plt.xlabel("Algorithms")
    plt.ylabel("Number of Faults")
    plt.show()


def run_for_3_frames():
    ref_string = ref_entry.get().strip()
    if ref_string == "":
        messagebox.showerror("Error", "Enter reference string first.")
        return

    frame_entry.delete(0, tk.END)
    frame_entry.insert(0, "3")
    compare_all()


# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Virtual Memory Paging Simulator (FIFO vs LRU vs OPT vs LFU)")
root.geometry("1100x750")
root.config(bg="#f2f2f2")

title = tk.Label(root, text="Virtual Memory Paging Simulator", font=("Arial", 20, "bold"), bg="#f2f2f2")
title.pack(pady=10)

frame_top = tk.Frame(root, bg="#f2f2f2")
frame_top.pack(pady=5)

tk.Label(frame_top, text="Number of Frames:", font=("Arial", 12), bg="#f2f2f2").grid(row=0, column=0, padx=5, pady=5)
frame_entry = tk.Entry(frame_top, font=("Arial", 12), width=10)
frame_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Reference String:", font=("Arial", 12), bg="#f2f2f2").grid(row=0, column=2, padx=5, pady=5)
ref_entry = tk.Entry(frame_top, font=("Arial", 12), width=55)
ref_entry.grid(row=0, column=3, padx=5, pady=5)

# Buttons
frame_buttons = tk.Frame(root, bg="#f2f2f2")
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Run FIFO", font=("Arial", 12), width=12, command=run_fifo, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=6)
tk.Button(frame_buttons, text="Run LRU", font=("Arial", 12), width=12, command=run_lru, bg="#2196F3", fg="white").grid(row=0, column=1, padx=6)
tk.Button(frame_buttons, text="Run OPT", font=("Arial", 12), width=12, command=run_optimal, bg="#9C27B0", fg="white").grid(row=0, column=2, padx=6)
tk.Button(frame_buttons, text="Run LFU", font=("Arial", 12), width=12, command=run_lfu, bg="#795548", fg="white").grid(row=0, column=3, padx=6)

tk.Button(frame_buttons, text="Compare All", font=("Arial", 12), width=12, command=compare_all, bg="#FF9800", fg="white").grid(row=0, column=4, padx=6)
tk.Button(frame_buttons, text="Graph", font=("Arial", 12), width=10, command=show_graph, bg="#607D8B", fg="white").grid(row=0, column=5, padx=6)
tk.Button(frame_buttons, text="3 Frames Test", font=("Arial", 12), width=14, command=run_for_3_frames, bg="#3F51B5", fg="white").grid(row=0, column=6, padx=6)

tk.Button(frame_buttons, text="Clear", font=("Arial", 12), width=10, command=clear_output, bg="#f44336", fg="white").grid(row=0, column=7, padx=6)

algo_label = tk.Label(root, text="Algorithm Output:", font=("Arial", 14, "bold"), bg="#f2f2f2")
algo_label.pack(pady=5)

# Table Output
tree_frame = tk.Frame(root)
tree_frame.pack(pady=5, fill="both", expand=True)

tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
tree.pack(fill="both", expand=True)

tree_scroll.config(command=tree.yview)

# Log Panel
log_label = tk.Label(root, text="Execution Log:", font=("Arial", 13, "bold"), bg="#f2f2f2")
log_label.pack(pady=5)

log_frame = tk.Frame(root)
log_frame.pack(pady=5, fill="both")

log_scroll = ttk.Scrollbar(log_frame)
log_scroll.pack(side="right", fill="y")

log_text = tk.Text(log_frame, height=7, font=("Consolas", 10), yscrollcommand=log_scroll.set)
log_text.pack(fill="both", expand=True)

log_scroll.config(command=log_text.yview)

# Comparison Table
compare_label = tk.Label(root, text="Comparison Summary:", font=("Arial", 13, "bold"), bg="#f2f2f2")
compare_label.pack(pady=5)

compare_frame = tk.Frame(root)
compare_frame.pack(pady=5, fill="x")

compare_tree = ttk.Treeview(compare_frame, columns=("Algorithm", "Hits", "Faults", "Hit Ratio"), show="headings", height=4)
compare_tree.pack(fill="x")

compare_tree.heading("Algorithm", text="Algorithm")
compare_tree.heading("Hits", text="Hits")
compare_tree.heading("Faults", text="Faults")
compare_tree.heading("Hit Ratio", text="Hit Ratio (%)")

compare_tree.column("Algorithm", anchor="center", width=200)
compare_tree.column("Hits", anchor="center", width=150)
compare_tree.column("Faults", anchor="center", width=150)
compare_tree.column("Hit Ratio", anchor="center", width=200)

# Result Summary
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f2f2f2", fg="black")
result_label.pack(pady=10)

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import time

SAMPLE_PASSAGES = [
    "Cloud computing enables on-demand access to computing resources over the internet, including servers, storage, databases, and software.",
    "Python emphasizes code readability with its significant indentation and a simple, clean syntax that reduces development time.",
    "An operating system manages hardware and software resources and provides common services for computer programs.",
    "Networking concepts like DNS, TCP, and load balancing are essential for reliable and scalable applications in the cloud.",
    "Clear communication and consistent practice are the keys to improving your typing speed and accuracy over time.",
    "Containers package up code and its dependencies so the application runs quickly and reliably from one computing environment to another.",
    "Automation reduces manual errors and frees engineers to focus on higher-value tasks like reliability, security, and optimization."
]

class TypingTester(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Speed Tester")
        self.geometry("900x500")
        self.minsize(820, 460)

        # --- State ---
        self.duration = tk.IntVar(value=60)      # seconds
        self.running = False
        self.start_time = None
        self.time_left = 60
        self.correct_chars = 0
        self.typed_chars = 0
        self.target_text = tk.StringVar(value=random.choice(SAMPLE_PASSAGES))

        # --- Styles ---
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        # --- Layout ---
        self._build_topbar()
        self._build_target_and_input()
        self._build_stats()

        self._apply_target_text()
        self._bind_events()

    # ---------- UI ----------
    def _build_topbar(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Duration:").pack(side="left", padx=(0,6))
        for sec in (15, 30, 60):
            ttk.Radiobutton(top, text=f"{sec}s", value=sec, variable=self.duration,
                            command=self._on_change_duration).pack(side="left", padx=2)

        ttk.Button(top, text="Random Text", command=self._random_text).pack(side="left", padx=10)
        ttk.Button(top, text="Custom Text", command=self._custom_text).pack(side="left", padx=(0,10))

        self.start_btn = ttk.Button(top, text="Start", command=self.start)
        self.start_btn.pack(side="left")

        self.reset_btn = ttk.Button(top, text="Reset", command=self.reset, state="disabled")
        self.reset_btn.pack(side="left", padx=(6,0))

        # Spacer
        ttk.Label(top, text="").pack(side="left", expand=True)

        self.timer_label = ttk.Label(top, text="Time: 60.0s", font=("Segoe UI", 12, "bold"))
        self.timer_label.pack(side="right")

    def _build_target_and_input(self):
        body = ttk.Frame(self, padding=(10,0,10,10))
        body.pack(fill="both", expand=True)

        ttk.Label(body, text="Target Text:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(4,2))
        self.target = tk.Text(body, height=6, wrap="word", font=("Consolas", 12))
        self.target.config(state="disabled")
        self.target.pack(fill="both", expand=False)

        # tags for highlighting
        self.target.tag_configure("typed_ok", background="")
        self.target.tag_configure("typed_bad", background="#ffd6d6")  # light red
        self.target.tag_configure("cursor", underline=1)

        ttk.Label(body, text="Type here:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10,2))
        self.entry = tk.Text(body, height=6, wrap="word", font=("Consolas", 12))
        self.entry.config(state="disabled")
        self.entry.pack(fill="both", expand=True)

        helper = ttk.Label(body, text="Press Start, then begin typing. The test ends when time runs out or you finish the text.")
        helper.pack(anchor="w", pady=(6,0))

    def _build_stats(self):
        bar = ttk.Frame(self, padding=10)
        bar.pack(fill="x")

        self.wpm_var = tk.StringVar(value="WPM: 0.0")
        self.acc_var = tk.StringVar(value="Accuracy: 100.0%")
        self.chars_var = tk.StringVar(value="Chars (correct/typed): 0/0")

        ttk.Label(bar, textvariable=self.wpm_var, font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0,18))
        ttk.Label(bar, textvariable=self.acc_var, font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0,18))
        ttk.Label(bar, textvariable=self.chars_var, font=("Segoe UI", 11, "bold")).pack(side="left")

    # ---------- Behavior ----------
    def _apply_target_text(self):
        self.target.config(state="normal")
        self.target.delete("1.0", "end")
        self.target.insert("1.0", self.target_text.get().strip())
        self.target.config(state="disabled")

        # clear tags
        self._clear_highlights()

    def _bind_events(self):
        self.entry.bind("<KeyRelease>", self._on_type)
        self.entry.bind("<Control-BackSpace>", lambda e: "break")  # keep simple
        self.entry.bind("<Control-v>", lambda e: "break")          # disable paste during run

    def _on_change_duration(self):
        if not self.running:
            self.time_left = self.duration.get()
            self.timer_label.config(text=f"Time: {self.time_left:.1f}s")

    def _random_text(self):
        if self.running:
            return
        self.target_text.set(random.choice(SAMPLE_PASSAGES))
        self._apply_target_text()

    def _custom_text(self):
        if self.running:
            return
        txt = simpledialog.askstring("Custom Text", "Paste or type the text you want to practice with:")
        if txt:
            self.target_text.set(txt.strip())
            self._apply_target_text()

    def start(self):
        if self.running:
            return
        self.reset_metrics()
        self.entry.config(state="normal")
        self.entry.delete("1.0", "end")
        self.entry.focus_set()

        self.time_left = self.duration.get()
        self.start_time = time.time()
        self.running = True
        self.start_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

        self._tick()

    def reset(self):
        self.running = False
        self.start_btn.config(state="normal")
        self.reset_btn.config(state="disabled")
        self.entry.config(state="disabled")
        self.entry.delete("1.0", "end")
        self.reset_metrics()
        self._clear_highlights()
        self.time_left = self.duration.get()
        self.timer_label.config(text=f"Time: {self.time_left:.1f}s")

    def reset_metrics(self):
        self.correct_chars = 0
        self.typed_chars = 0
        self.wpm_var.set("WPM: 0.0")
        self.acc_var.set("Accuracy: 100.0%")
        self.chars_var.set("Chars (correct/typed): 0/0")

    def _tick(self):
        if not self.running:
            return
        elapsed = time.time() - self.start_time
        remaining = max(0.0, self.duration.get() - elapsed)
        self.timer_label.config(text=f"Time: {remaining:.1f}s")
        if remaining <= 0:
            self._finish()
            return
        self.after(50, self._tick)

    def _on_type(self, _event=None):
        if not self.running:
            return
        typed = self.entry.get("1.0", "end-1c")
        target = self.target_text.get()

        self.typed_chars = len(typed)
        self.correct_chars = 0

        # Clear previous highlights
        self._clear_highlights()

        # Compare and highlight
        bad_from = None
        for i, ch in enumerate(typed):
            if i >= len(target):
                # over-typed area is bad
                if bad_from is None:
                    bad_from = i
                continue

            if ch == target[i]:
                self.correct_chars += 1
                if bad_from is not None:
                    self._apply_bad(bad_from, i)
                    bad_from = None
            else:
                if bad_from is None:
                    bad_from = i

        # close trailing bad span
        if bad_from is not None:
            self._apply_bad(bad_from, min(len(typed), len(target)))

        # Cursor underline at current target index
        cur = min(len(typed), len(target))
        self._apply_cursor(cur)

        # Metrics
        minutes = max(1e-9, (time.time() - self.start_time) / 60.0)
        wpm = (self.correct_chars / 5.0) / minutes
        acc = (self.correct_chars / self.typed_chars * 100.0) if self.typed_chars > 0 else 100.0

        self.wpm_var.set(f"WPM: {wpm:.1f}")
        self.acc_var.set(f"Accuracy: {acc:.1f}%")
        self.chars_var.set(f"Chars (correct/typed): {self.correct_chars}/{self.typed_chars}")

        # Finish early if completed text
        if len(typed) >= len(target):
            self._finish()

    # ---------- Highlight helpers ----------
    def _clear_highlights(self):
        self.target.config(state="normal")
        self.target.tag_remove("typed_ok", "1.0", "end")
        self.target.tag_remove("typed_bad", "1.0", "end")
        self.target.tag_remove("cursor", "1.0", "end")
        self.target.config(state="disabled")

    def _idx(self, i):
        # Convert character index to Tk text index "line.char"
        # Our text is single-line with wrapping; use "1.0 + i chars"
        return f"1.0 + {i} chars"

    def _apply_bad(self, start_i, end_i):
        self.target.config(state="normal")
        self.target.tag_add("typed_bad", self._idx(start_i), self._idx(end_i))
        self.target.config(state="disabled")

    def _apply_cursor(self, i):
        self.target.config(state="normal")
        self.target.tag_add("cursor", self._idx(i), self._idx(i+1))
        self.target.config(state="disabled")

    # ---------- Finish ----------
    def _finish(self):
        if not self.running:
            return
        self.running = False
        self.entry.config(state="disabled")
        self.start_btn.config(state="normal")
        self.reset_btn.config(state="normal")

        # Final metrics already set; show a summary
        final_wpm = self.wpm_var.get()
        final_acc = self.acc_var.get()
        final_chars = self.chars_var.get()
        messagebox.showinfo("Session Complete", f"{final_wpm}\n{final_acc}\n{final_chars}")

if __name__ == "__main__":
    TypingTester().mainloop()

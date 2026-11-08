"""
Matchstick Master - Python Puzzle Game
A Tkinter desktop game with 10 one-match equation puzzles,
timer, score, sound alert and top-5 scoreboard.
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
import re

APP_TITLE = "MATCHSTICK MASTER"
TIME_PER_LEVEL = 60
SCORE_FILE = "scores.json"

# Each answer is a valid equation reachable by moving exactly one
# seven-segment matchstick from the displayed equation.
PUZZLES = [
    {"question": "7 - 1 = 2", "answer": "1+1=2", "hint": "Move one stick from the minus sign to the first digit."},
    {"question": "7 - 2 = 3", "answer": "1+2=3", "hint": "Change the first digit and the operator with one move."},
    {"question": "1 - 9 = 4", "answer": "1+3=4", "hint": "Move one stick from the minus sign to the middle digit."},
    {"question": "7 - 4 = 5", "answer": "1+4=5", "hint": "Look at the first digit and the operator."},
    {"question": "7 - 5 = 6", "answer": "1+5=6", "hint": "One stick changes the first digit; another position changes the sign."},
    {"question": "7 - 6 = 7", "answer": "1+6=7", "hint": "Look at the first digit and the operator."},
    {"question": "7 - 7 = 8", "answer": "1+7=8", "hint": "Move one stick from the minus sign to the first digit."},
    {"question": "7 - 8 = 9", "answer": "1+8=9", "hint": "Look at the first digit and the operator."},
    {"question": "1 - 2 = 9", "answer": "1+2=3", "hint": "Move one stick from the minus sign to the final digit."},
    {"question": "1 - 9 = 6", "answer": "1+5=6", "hint": "Move one stick from the minus sign to the middle digit."},
]


class MatchstickMaster:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("850x680")
        self.root.minsize(760, 620)
        self.root.configure(bg="#101827")

        self.player_name = "Player"
        self.level = 0
        self.score = 0
        self.time_left = TIME_PER_LEVEL
        self.timer_job = None
        self.level_solved = False
        self.game_finished = False
        self.hint_used = False

        self.build_ui()
        self.show_leaderboard()
        self.start_level()

    def build_ui(self):
        tk.Label(
            self.root, text=APP_TITLE, bg="#101827", fg="#38BDF8",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(18, 4))

        tk.Label(
            self.root, text="MOVE ONE MATCHSTICK • SOLVE THE EQUATION",
            bg="#101827", fg="#CBD5E1", font=("Segoe UI", 10, "bold")
        ).pack(pady=(0, 14))

        top = tk.Frame(self.root, bg="#1E293B", padx=18, pady=12)
        top.pack(fill="x", padx=35)

        tk.Label(top, text="Player:", bg="#1E293B", fg="white",
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        self.name_entry = tk.Entry(top, width=18, font=("Segoe UI", 11))
        self.name_entry.insert(0, "Player")
        self.name_entry.pack(side="left", padx=(8, 20))

        self.level_label = tk.Label(top, text="LEVEL: 1/10", bg="#1E293B",
                                    fg="#22C55E", font=("Segoe UI", 11, "bold"))
        self.level_label.pack(side="left", padx=10)

        self.score_label = tk.Label(top, text="SCORE: 0", bg="#1E293B",
                                    fg="#FACC15", font=("Segoe UI", 11, "bold"))
        self.score_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(top, text="TIME: 60", bg="#1E293B",
                                    fg="#FB7185", font=("Segoe UI", 11, "bold"))
        self.timer_label.pack(side="right", padx=8)

        card = tk.Frame(self.root, bg="#1E293B", padx=25, pady=25)
        card.pack(fill="x", padx=35, pady=22)

        tk.Label(card, text="CURRENT MATCHSTICK PUZZLE",
                 bg="#1E293B", fg="#CBD5E1",
                 font=("Segoe UI", 12, "bold")).pack(pady=(0, 14))

        self.question_label = tk.Label(
            card, text="", bg="#0F172A", fg="#FACC15",
            font=("Consolas", 34, "bold"), padx=20, pady=18
        )
        self.question_label.pack(fill="x")

        tk.Label(
            card, text="Move exactly ONE matchstick. Enter the corrected equation below.",
            bg="#1E293B", fg="#E2E8F0", font=("Segoe UI", 10)
        ).pack(pady=(14, 8))

        self.answer_entry = tk.Entry(
            card, justify="center", font=("Consolas", 20), width=18
        )
        self.answer_entry.pack(pady=5)
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())

        buttons = tk.Frame(self.root, bg="#101827")
        buttons.pack(pady=5)

        self.make_button(buttons, "CHECK ANSWER", self.check_answer,
                         "#22C55E", "#052E16").pack(side="left", padx=6)
        self.next_button = self.make_button(
            buttons, "NEXT LEVEL", self.next_level, "#38BDF8", "#082F49"
        )
        self.next_button.pack(side="left", padx=6)
        self.next_button.config(state="disabled")
        self.make_button(buttons, "HINT", self.show_hint,
                         "#A78BFA", "#2E1065").pack(side="left", padx=6)
        self.make_button(buttons, "RESTART", self.restart,
                         "#FACC15", "#422006").pack(side="left", padx=6)

        self.status_label = tk.Label(
            self.root, text="Good luck!", bg="#101827", fg="#38BDF8",
            font=("Segoe UI", 12, "bold")
        )
        self.status_label.pack(pady=12)

        board = tk.Frame(self.root, bg="#1E293B", padx=18, pady=12)
        board.pack(fill="x", padx=35, pady=(5, 15))
        tk.Label(board, text="TOP 5 SCOREBOARD", bg="#1E293B",
                 fg="#FACC15", font=("Segoe UI", 12, "bold")).pack()
        self.board_label = tk.Label(
            board, text="No scores yet.", bg="#1E293B", fg="#F8FAFC",
            font=("Consolas", 10), justify="center"
        )
        self.board_label.pack(pady=(7, 0))

        tk.Label(
            self.root, text="Python • Tkinter • JSON",
            bg="#101827", fg="#64748B", font=("Segoe UI", 9)
        ).pack(side="bottom", pady=8)

    def make_button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent, text=text, command=command, bg=bg, fg=fg,
            activebackground=bg, activeforeground=fg,
            font=("Segoe UI", 10, "bold"), relief="flat",
            padx=15, pady=10, cursor="hand2"
        )

    def start_level(self):
        self.cancel_timer()
        if self.level >= len(PUZZLES):
            self.finish_game()
            return

        self.level_solved = False
        self.hint_used = False
        self.time_left = TIME_PER_LEVEL
        puzzle = PUZZLES[self.level]

        self.level_label.config(text=f"LEVEL: {self.level + 1}/{len(PUZZLES)}")
        self.score_label.config(text=f"SCORE: {self.score}")
        self.question_label.config(text=puzzle["question"])
        self.answer_entry.delete(0, tk.END)
        self.status_label.config(text="Find the correct equation!", fg="#38BDF8")
        self.next_button.config(state="disabled")
        self.timer_label.config(text=f"TIME: {self.time_left}")
        self.tick()

    def tick(self):
        if self.level_solved or self.game_finished:
            return
        self.timer_label.config(text=f"TIME: {self.time_left}")
        if self.time_left <= 0:
            self.game_over()
            return
        self.time_left -= 1
        self.timer_job = self.root.after(1000, self.tick)

    def cancel_timer(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def play_sound(self):
        # Uses the operating system's standard alert sound; no extra package needed.
        try:
            self.root.bell()
        except tk.TclError:
            pass

    @staticmethod
    def normalize(text):
        return re.sub(r"\s+", "", text).replace("×", "*").replace("−", "-")

    def check_answer(self):
        if self.level_solved or self.game_finished:
            return
        entered = self.normalize(self.answer_entry.get())
        expected = self.normalize(PUZZLES[self.level]["answer"])

        if entered == expected:
            self.level_solved = True
            self.cancel_timer()
            self.play_sound()
            points = max(10, 100 - (TIME_PER_LEVEL - self.time_left))
            if self.hint_used:
                points = max(5, points - 20)
            self.score += points
            self.score_label.config(text=f"SCORE: {self.score}")
            self.status_label.config(
                text=f"CORRECT! +{points} POINTS", fg="#22C55E"
            )
            self.next_button.config(state="normal")
        else:
            self.play_sound()
            self.score = max(0, self.score - 5)
            self.score_label.config(text=f"SCORE: {self.score}")
            self.status_label.config(
                text="Not quite. Try another equation! (-5 points)",
                fg="#FB7185"
            )

    def show_hint(self):
        if self.level_solved or self.game_finished:
            return
        self.hint_used = True
        messagebox.showinfo("Hint", PUZZLES[self.level]["hint"])

    def next_level(self):
        if not self.level_solved:
            return
        self.level += 1
        self.start_level()

    def load_scores(self):
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []

    def save_score(self):
        scores = self.load_scores()
        scores.append({"player": self.player_name, "score": self.score})
        scores.sort(key=lambda item: item.get("score", 0), reverse=True)
        try:
            with open(SCORE_FILE, "w", encoding="utf-8") as file:
                json.dump(scores[:5], file, indent=4)
        except OSError:
            messagebox.showwarning("Scoreboard", "Could not save the score file.")

    def show_leaderboard(self):
        scores = self.load_scores()
        if not scores:
            text = "No scores yet. Complete a game to appear here!"
        else:
            text = "\n".join(
                f"{i}. {item.get('player', 'Player')} — {item.get('score', 0)} points"
                for i, item in enumerate(scores[:5], start=1)
            )
        self.board_label.config(text=text)

    def game_over(self):
        self.cancel_timer()
        self.game_finished = True
        self.status_label.config(text="TIME UP! GAME OVER", fg="#FB7185")
        self.finish_and_save()

    def finish_game(self):
        self.cancel_timer()
        self.game_finished = True
        self.status_label.config(text="ALL LEVELS COMPLETED! WELL DONE!", fg="#22C55E")
        self.finish_and_save()

    def finish_and_save(self):
        self.player_name = self.name_entry.get().strip() or "Player"
        self.save_score()
        self.show_leaderboard()
        self.next_button.config(state="disabled")
        messagebox.showinfo(
            "Game Result",
            f"Player: {self.player_name}\nFinal score: {self.score}"
        )

    def restart(self):
        self.cancel_timer()
        self.level = 0
        self.score = 0
        self.game_finished = False
        self.player_name = self.name_entry.get().strip() or "Player"
        self.start_level()


if __name__ == "__main__":
    root = tk.Tk()
    app = MatchstickMaster(root)
    root.mainloop()

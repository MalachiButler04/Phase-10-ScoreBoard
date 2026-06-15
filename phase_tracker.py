import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self, name: str):
        self.name = name
        self.score_history: list[int] = [0]

        self.score = tk.StringVar(value="0")

        self.phase_num = 1
        self.phase_pointer = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_name(self) -> str:
        return self.name

    def get_total_score(self) -> int:
        return sum(self.score_history)

    def get_score(self) -> list[int]:
        return self.score_history

    def get_current_phase(self) -> int:
        return self.phase[-1]

class PlayerTracker:
    def __init__(self):
        self.phase_rules = {
            1: "2 sets of 3",
            2: "1 set of 3 + 1 run of 4",
            3: "1 set of 4 + 1 run of 4",
            4: "1 run of 7",
            5: "1 run of 8",
            6: "1 run of 9",
            7: "2 sets of 4",
            8: "7 cards of 1 color",
            9: "1 set of 5 + 1 set of 2",
            10: "1 set of 5 + 1 set of 3",
        }

        self.phases = list(range(1, 11))
        self.BG = "#D4D4D4"

    def build_gui(self, players, root) -> None:
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10, side="left")

        pointers = []
        for i, player in enumerate(players):
            card, pointer_func = self.tracker_main(player, main_frame)
            card.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            pointers.append(pointer_func)

        button_frame = tk.Frame(root)
        button_frame.pack(side="right", fill="y")

        def next():
            for pointer in pointers:
                pointer()

        button = tk.Button(button_frame, text="Next Round >", command=next, height=5)
        button.pack(expand=True, anchor="center")

    def tracker_main(self, player: Player, parent) -> None:

        tracker = tk.Frame(
            parent,
            bg=self.BG,
            relief=tk.SUNKEN,
            borderwidth=1,
            padx=8,
            pady=8
        )

        tracker.config(width=320)
        tracker.pack_propagate(True)

        phase_label = tk.Label(
            tracker,
            text=self.phase_rules[player.phase_num],
            bg=self.BG,
            fg="#FF2800",
            font=("Georgia", 10)
        )

        name_label = tk.Label(
            tracker,
            text=f"Name: {player.name}",
            bg=self.BG,
            font=("Georgia", 12, "bold")
        )

        score_label = tk.Label(
            tracker,
            text=f"Score: {player.get_total_score()}",
            bg=self.BG,
            fg="#FF2800",
        )

        history_label = tk.Label(
            tracker,
            text=f"History: {player.get_score()}",
            bg=self.BG,
            fg="#FF2800"
        )

        name_label.pack()
        score_label.pack()
        history_label.pack(anchor="w")
        phase_label.pack(anchor="w")

        tracker_frame = tk.Frame(tracker, bg=self.BG)
        tracker_frame.pack(pady=5, fill="x")

        for phase in self.phases:
            tk.Label(
                tracker_frame,
                text=str(phase),
                width=4,
                bg="white",
                relief="sunken"
            ).pack(side=tk.LEFT, padx=2)

        pointer_frame = tk.Frame(tracker, bg=self.BG)
        pointer_frame.pack()

        def update_pointer():
            for w in pointer_frame.winfo_children():
                w.destroy()

            for active in player.phase_pointer:
                tk.Label(
                    pointer_frame,
                    text="^" if active else " ",
                    width=4,
                    bg=self.BG
                ).pack(side=tk.LEFT, padx=2)

        def next_round():
            try:
                score = int(entry.get().strip())

                if score % 5 != 0:
                    messagebox.askokcancel(title="Warning", message=f"Invalid score at: {player.name}", icon="warning")
                    return
                
                if score >= 50:
                    player.score_history.append(score)
                    score_label.config(text=f"Score: {player.get_total_score()}")
                    history_label.config(text=f"History: {player.get_score()}")
                    player.score.set(value="0")
                    entry.delete(0, tk.END)
                    return
                
                for index, value in enumerate(player.phase_pointer):
                    if value == 1:
                        player.phase_pointer[index] = 0

                        if index < len(player.phase_pointer) - 1:
                            player.phase_pointer[index + 1] = 1
                            player.phase_num += 1
                        else:
                            player.phase_pointer[0] = 1
                            player.phase_num = 1
                        break

                player.score_history.append(score)

                player.score.set(value="0")

                phase_label.config(text=self.phase_rules[player.phase_num])
                score_label.config(text=f"Score: {player.get_total_score()}")
                history_label.config(text=f"History: {player.get_score()}")

            except ValueError:
                pass
        
            update_pointer()

        update_pointer()

        entry_frame = tk.Frame(tracker, bg=self.BG)
        entry_frame.pack(side="bottom", fill="x", pady=(5, 0))

        entry_label = tk.Label(entry_frame, text="Enter Score:", bg=self.BG)
        entry_label.pack(side="left")

        entry = tk.Entry(entry_frame, textvariable=player.score)
        entry.pack(fill="x")

        return tracker, next_round


root = tk.Tk()
root.title("Phase Tracker")
root.resizable(False, False)

players = [
    Player("Fred"),
    Player("Sally")
]

tracker = PlayerTracker()
tracker.build_gui(players, root)

root.mainloop()
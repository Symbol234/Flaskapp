import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class LibrarySeatingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Seating Arrangement")

        self.data_file = "seating_data.json"
        self.named_seats = {chr(i): None for i in range(ord('A'), ord('U') + 1)}
        self.numbered_seats = {i: None for i in range(1, 44)}
        self.load_data()

        self.buttons = {}
        self.create_widgets()
        self.update_buttons()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.named_seats = data.get("named_seats", self.named_seats)
                self.numbered_seats = {int(k): v for k, v in data.get("numbered_seats", {}).items()}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump({
                'named_seats': self.named_seats,
                'numbered_seats': self.numbered_seats
            }, f, indent=2)

    def create_widgets(self):
        # Named Seats (A–U)
        tk.Label(self.root, text="Named Seats (A–U)", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=7)
        row = 1
        col = 0
        for seat in self.named_seats:
            btn = tk.Button(self.root, text=seat, width=6, height=2,
                            command=lambda s=seat: self.toggle_seat(s))
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.buttons[seat] = btn
            col += 1
            if col > 6:
                row += 1
                col = 0

        # Numbered Seats (1–43)
        tk.Label(self.root, text="Numbered Seats (1–43)", font=('Arial', 12, 'bold')).grid(row=row+1, column=0, columnspan=10)
        row += 2
        col = 0
        for seat in range(1, 44):
            btn = tk.Button(self.root, text=str(seat), width=6, height=2,
                            command=lambda s=seat: self.toggle_seat(s))
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.buttons[seat] = btn
            col += 1
            if col > 9:
                row += 1
                col = 0

    def toggle_seat(self, seat_id):
        current_name = self.named_seats.get(seat_id) if isinstance(seat_id, str) else self.numbered_seats.get(seat_id)

        if current_name:  # If the seat is already assigned, reset it
            self.reset_seat(seat_id)
        else:  # If the seat is empty, assign a name
            self.assign_seat(seat_id)

    def assign_seat(self, seat_id):
        prompt = f"Seat {seat_id} is empty. Enter name to assign:"
        name = simpledialog.askstring("Assign Seat", prompt)
        if name:
            if isinstance(seat_id, str):
                self.named_seats[seat_id] = name
            else:
                self.numbered_seats[seat_id] = name
            self.save_data()
            self.update_buttons()

    def reset_seat(self, seat_id):
        if isinstance(seat_id, str) and self.named_seats.get(seat_id):
            self.named_seats[seat_id] = None
            messagebox.showinfo("Seat Reset", f"Seat {seat_id} has been reset.")
        elif isinstance(seat_id, int) and self.numbered_seats.get(seat_id):
            self.numbered_seats[seat_id] = None
            messagebox.showinfo("Seat Reset", f"Seat {seat_id} has been reset.")
        self.save_data()
        self.update_buttons()

    def update_buttons(self):
        for seat_id, btn in self.buttons.items():
            assigned = self.named_seats.get(seat_id) if isinstance(seat_id, str) else self.numbered_seats.get(seat_id)
            btn.config(bg="red" if assigned else "lightgreen")

# --- Main Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySeatingGUI(root)  # No need for reset_seat parameter now
    root.mainloop()

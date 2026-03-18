import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

from profile_manager import (
    save_profile,
    load_profile,
    user_exists,
    save_history,
    load_history
)
from response_engine import generate_local_response
from ai_connector import generate_ai_response


BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
ACCENT_COLOR = "#38bdf8"
TEXT_COLOR = "#f8fafc"
SECONDARY_TEXT = "#cbd5e1"
INPUT_BG = "#334155"
BUTTON_BG = "#0ea5e9"
BUTTON_HOVER = "#0284c7"
USER_BUBBLE = "#2563eb"
MIS_BUBBLE = "#334155"
AVATARS_FOLDER = "avatars"


class MISApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MIS - Memory Identity Stratified")
        self.root.geometry("1150x780")
        self.root.configure(bg=BG_COLOR)

        self.profile = None
        self.username = None
        self.history = []
        self.avatar_preview_path = None
        self.avatar_image_tk = None
        self.left_avatar_tk = None

        if not os.path.exists(AVATARS_FOLDER):
            os.makedirs(AVATARS_FOLDER)

        self.show_start_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def styled_button(self, parent, text, command, width=18):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=BUTTON_BG,
            fg="white",
            activebackground=BUTTON_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            pady=10
        )

    def create_entry(self, parent, width=30):
        return tk.Entry(
            parent,
            width=width,
            bg=INPUT_BG,
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Arial", 12)
        )

    def get_avatar_path(self, username):
        return os.path.join(AVATARS_FOLDER, f"{username}.png")

    def resize_and_save_avatar(self, source_path, username):
        avatar_path = self.get_avatar_path(username)
        image = Image.open(source_path).convert("RGB")
        image = image.resize((120, 120))
        image.save(avatar_path, format="PNG")
        return avatar_path

    def load_avatar_tk(self, image_path, size=(90, 90)):
        if not image_path or not os.path.exists(image_path):
            return None
        image = Image.open(image_path).convert("RGB")
        image = image.resize(size)
        return ImageTk.PhotoImage(image)

    def choose_avatar(self):
        file_path = filedialog.askopenfilename(
            title="Alege o poza de profil",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp")]
        )

        if not file_path:
            return

        self.avatar_preview_path = file_path
        preview = self.load_avatar_tk(file_path, size=(100, 100))
        self.avatar_image_tk = preview

        self.avatar_preview_label.config(image=self.avatar_image_tk, text="")
        self.avatar_preview_label.image = self.avatar_image_tk

    def show_start_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True)

        title = tk.Label(
            container,
            text="MIS",
            font=("Arial", 30, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        title.pack(pady=(60, 10))

        subtitle = tk.Label(
            container,
            text="Memory Identity Stratified",
            font=("Arial", 14),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        )
        subtitle.pack()

        card = tk.Frame(container, bg=CARD_COLOR, padx=40, pady=40)
        card.pack(pady=50)

        tk.Label(
            card,
            text="Alege o optiune",
            font=("Arial", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(0, 20))

        self.styled_button(card, "Sign Up", self.show_signup_screen, width=20).pack(pady=10)
        self.styled_button(card, "Sign In", self.show_signin_screen, width=20).pack(pady=10)

    def show_signup_screen(self):
        self.clear_window()
        self.avatar_preview_path = None
        self.avatar_image_tk = None

        main_container = tk.Frame(self.root, bg=BG_COLOR)
        main_container.pack(fill="both", expand=True)

        # Zona scrollabila sus
        top_area = tk.Frame(main_container, bg=BG_COLOR)
        top_area.pack(fill="both", expand=True)

        canvas = tk.Canvas(top_area, bg=BG_COLOR, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(top_area, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_frame = tk.Frame(canvas, bg=BG_COLOR)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        tk.Label(
            scroll_frame,
            text="Creare cont MIS",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(20, 10))

        content = tk.Frame(scroll_frame, bg=BG_COLOR)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        left_card = tk.Frame(content, bg=CARD_COLOR, padx=20, pady=20)
        left_card.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_card = tk.Frame(content, bg=CARD_COLOR, padx=20, pady=20)
        right_card.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # STANGA
        tk.Label(
            left_card,
            text="Date cont",
            font=("Arial", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(0, 15))

        tk.Label(
            left_card,
            text="Username unic",
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            font=("Arial", 11)
        ).pack(anchor="w")
        self.signup_username = self.create_entry(left_card)
        self.signup_username.pack(fill="x", pady=(5, 15), ipady=8)

        tk.Label(
            left_card,
            text="Nume afisat",
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            font=("Arial", 11)
        ).pack(anchor="w")
        self.signup_display_name = self.create_entry(left_card)
        self.signup_display_name.pack(fill="x", pady=(5, 15), ipady=8)

        tk.Label(
            left_card,
            text="Parola",
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            font=("Arial", 11)
        ).pack(anchor="w")
        self.signup_password = self.create_entry(left_card)
        self.signup_password.config(show="*")
        self.signup_password.pack(fill="x", pady=(5, 15), ipady=8)

        tk.Label(
            left_card,
            text="Poza de profil",
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            font=("Arial", 11)
        ).pack(anchor="w")

        self.styled_button(left_card, "Alege poza", self.choose_avatar, width=16).pack(anchor="w", pady=10)

        self.avatar_preview_label = tk.Label(
            left_card,
            text="Fara poza",
            bg=INPUT_BG,
            fg=SECONDARY_TEXT,
            width=16,
            height=6
        )
        self.avatar_preview_label.pack(anchor="w", pady=10)

        tk.Label(
            left_card,
            text="Raspunsurile trebuie sa fie intre 1 si 5",
            font=("Arial", 11),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(anchor="w", pady=(10, 5))

        # DREAPTA
        tk.Label(
            right_card,
            text="Test de personalitate",
            font=("Arial", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(0, 15))

        self.question_entries = {}

        questions = [
            ("risc", "Cat de mult iti place sa iti asumi riscuri?"),
            ("social", "Cat de sociabil esti?"),
            ("organizare", "Cat de organizat esti?"),
            ("emotie", "Cat de emotional esti?"),
            ("rabdare", "Cat de rabdator esti?"),
            ("adaptare", "Cat de usor te adaptezi la schimbari?"),
            ("disciplina", "Cat de disciplinat esti?"),
            ("incredere", "Cat de multa incredere ai in tine?")
        ]

        for key, text in questions:
            tk.Label(
                right_card,
                text=text,
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT,
                font=("Arial", 10)
            ).pack(anchor="w", pady=(4, 2))

            entry = self.create_entry(right_card, width=10)
            entry.pack(anchor="w", pady=(0, 8), ipady=6)
            self.question_entries[key] = entry

        # Zona de jos fixa, pentru butoane
        bottom_bar = tk.Frame(main_container, bg=BG_COLOR)
        bottom_bar.pack(fill="x", pady=10)

        self.styled_button(bottom_bar, "Creeaza cont", self.handle_signup, width=20).pack(side="left", padx=20)
        self.styled_button(bottom_bar, "Inapoi", self.show_start_screen, width=20).pack(side="left")

    def handle_signup(self):
        username = self.signup_username.get().strip().lower()
        display_name = self.signup_display_name.get().strip()
        password = self.signup_password.get().strip()

        if not username:
            messagebox.showerror("Eroare", "Username-ul nu poate fi gol.")
            return

        if not display_name:
            messagebox.showerror("Eroare", "Numele afisat nu poate fi gol.")
            return

        if not password:
            messagebox.showerror("Eroare", "Parola nu poate fi goala.")
            return

        if user_exists(username):
            messagebox.showerror("Eroare", "Acest username exista deja.")
            return

        try:
            risc = int(self.question_entries["risc"].get().strip())
            social = int(self.question_entries["social"].get().strip())
            organizare = int(self.question_entries["organizare"].get().strip())
            emotie = int(self.question_entries["emotie"].get().strip())
            rabdare = int(self.question_entries["rabdare"].get().strip())
            adaptare = int(self.question_entries["adaptare"].get().strip())
            disciplina = int(self.question_entries["disciplina"].get().strip())
            incredere = int(self.question_entries["incredere"].get().strip())
        except ValueError:
            messagebox.showerror("Eroare", "Toate raspunsurile trebuie sa fie numere intre 1 si 5.")
            return

        values = [risc, social, organizare, emotie, rabdare, adaptare, disciplina, incredere]
        if any(v < 1 or v > 5 for v in values):
            messagebox.showerror("Eroare", "Toate valorile trebuie sa fie intre 1 si 5.")
            return

        profile = {
            "risc": "curajos" if risc >= 4 else "prudent",
            "social": "extrovertit" if social >= 4 else "rezervat",
            "organizare": "organizat" if organizare >= 4 else "spontan",
            "emotie": "emotional" if emotie >= 4 else "rational",
            "rabdare": "rabdator" if rabdare >= 4 else "nerabdator",
            "adaptare": "flexibil" if adaptare >= 4 else "constant",
            "disciplina": "disciplinat" if disciplina >= 4 else "relaxat",
            "incredere": "increzator" if incredere >= 4 else "retinut",
            "display_name": display_name,
            "username": username,
            "password": password,
            "avatar": ""
        }

        if self.avatar_preview_path:
            saved_avatar_path = self.resize_and_save_avatar(self.avatar_preview_path, username)
            profile["avatar"] = saved_avatar_path

        save_profile(username, profile)
        save_history(username, [])

        self.username = username
        self.profile = profile
        self.history = []

        messagebox.showinfo("Succes", "Cont creat cu succes.")
        self.show_chat_screen()

    def show_signin_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="Sign In",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(60, 20))

        card = tk.Frame(container, bg=CARD_COLOR, padx=35, pady=35)
        card.pack(pady=20)

        tk.Label(card, text="Username", bg=CARD_COLOR, fg=SECONDARY_TEXT, font=("Arial", 11)).pack(anchor="w")
        self.signin_username = self.create_entry(card)
        self.signin_username.pack(fill="x", pady=(6, 15), ipady=8)

        tk.Label(card, text="Parola", bg=CARD_COLOR, fg=SECONDARY_TEXT, font=("Arial", 11)).pack(anchor="w")
        self.signin_password = self.create_entry(card)
        self.signin_password.config(show="*")
        self.signin_password.pack(fill="x", pady=(6, 20), ipady=8)

        btn_frame = tk.Frame(card, bg=CARD_COLOR)
        btn_frame.pack()

        self.styled_button(btn_frame, "Intra in cont", self.handle_signin, width=16).pack(side="left", padx=8)
        self.styled_button(btn_frame, "Inapoi", self.show_start_screen, width=16).pack(side="left", padx=8)

    def handle_signin(self):
        username = self.signin_username.get().strip().lower()
        password = self.signin_password.get().strip()

        if not username:
            messagebox.showerror("Eroare", "Introdu username-ul.")
            return

        if not password:
            messagebox.showerror("Eroare", "Introdu parola.")
            return

        profile = load_profile(username)

        if profile is None:
            messagebox.showerror("Eroare", "Nu exista niciun cont cu acest username.")
            return

        if profile.get("password") != password:
            messagebox.showerror("Eroare", "Parola incorecta.")
            return

        self.username = username
        self.profile = profile
        self.history = load_history(username)

        messagebox.showinfo("Bun venit", f"Bun venit inapoi, {profile['display_name']}!")
        self.show_chat_screen()

    def show_chat_screen(self):
        self.clear_window()

        wrapper = tk.Frame(self.root, bg=BG_COLOR)
        wrapper.pack(fill="both", expand=True, padx=15, pady=15)

        left_panel = tk.Frame(wrapper, bg=CARD_COLOR, width=280, padx=15, pady=15)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        avatar_path = self.profile.get("avatar", "")
        self.left_avatar_tk = self.load_avatar_tk(avatar_path, size=(100, 100))

        if self.left_avatar_tk:
            avatar_label = tk.Label(left_panel, image=self.left_avatar_tk, bg=CARD_COLOR)
            avatar_label.pack(anchor="w", pady=(0, 12))
            avatar_label.image = self.left_avatar_tk
        else:
            tk.Label(
                left_panel,
                text="Fara poza",
                bg=INPUT_BG,
                fg=SECONDARY_TEXT,
                width=14,
                height=6
            ).pack(anchor="w", pady=(0, 12))

        tk.Label(
            left_panel,
            text=self.profile["display_name"],
            font=("Arial", 15, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(anchor="w")

        tk.Label(
            left_panel,
            text=f"@{self.profile['username']}",
            font=("Arial", 11),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(anchor="w", pady=(0, 12))

        profile_lines = [
            f"Risc: {self.profile['risc']}",
            f"Social: {self.profile['social']}",
            f"Organizare: {self.profile['organizare']}",
            f"Emotie: {self.profile['emotie']}",
            f"Rabdare: {self.profile['rabdare']}",
            f"Adaptare: {self.profile['adaptare']}",
            f"Disciplina: {self.profile['disciplina']}",
            f"Incredere: {self.profile['incredere']}",
        ]

        for line in profile_lines:
            tk.Label(
                left_panel,
                text=line,
                font=("Arial", 10),
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT,
                anchor="w",
                justify="left"
            ).pack(fill="x", pady=3)

        tk.Label(
            left_panel,
            text="Mod raspuns",
            font=("Arial", 13, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(18, 8))

        self.mode_var = tk.StringVar(value="local")
        tk.Radiobutton(
            left_panel, text="Local", variable=self.mode_var, value="local",
            bg=CARD_COLOR, fg=TEXT_COLOR, selectcolor=INPUT_BG,
            activebackground=CARD_COLOR, activeforeground=TEXT_COLOR
        ).pack(anchor="w")
        tk.Radiobutton(
            left_panel, text="AI", variable=self.mode_var, value="ai",
            bg=CARD_COLOR, fg=TEXT_COLOR, selectcolor=INPUT_BG,
            activebackground=CARD_COLOR, activeforeground=TEXT_COLOR
        ).pack(anchor="w")

        self.styled_button(left_panel, "Logout", self.show_start_screen, width=16).pack(anchor="w", pady=(25, 0))

        right_panel = tk.Frame(wrapper, bg=CARD_COLOR, padx=15, pady=15)
        right_panel.pack(side="right", fill="both", expand=True)

        tk.Label(
            right_panel,
            text="MIS Chat",
            font=("Arial", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(0, 10))

        chat_container = tk.Frame(right_panel, bg=CARD_COLOR)
        chat_container.pack(fill="both", expand=True)

        self.chat_canvas = tk.Canvas(chat_container, bg="#0b1120", highlightthickness=0)
        self.chat_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(chat_container, orient="vertical", command=self.chat_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.chat_canvas.configure(yscrollcommand=scrollbar.set)

        self.messages_frame = tk.Frame(self.chat_canvas, bg="#0b1120")
        self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")

        self.messages_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )

        bottom_frame = tk.Frame(right_panel, bg=CARD_COLOR)
        bottom_frame.pack(fill="x", pady=(10, 0))

        self.question_entry = tk.Entry(
            bottom_frame,
            font=("Arial", 12),
            bg=INPUT_BG,
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.question_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=10)
        self.question_entry.bind("<Return>", self.send_message)

        self.styled_button(bottom_frame, "Trimite", self.send_message, width=14).pack(side="right")

        if self.history:
            for item in self.history:
                self.add_bubble(item["speaker"], item["message"])
        else:
            self.add_bubble("MIS", "Salut! Bine ai venit in aplicatia MIS.")

    def add_bubble(self, speaker, message):
        outer = tk.Frame(self.messages_frame, bg="#0b1120")
        outer.pack(fill="x", pady=6, padx=10)

        is_user = speaker == "Tu"
        bubble_color = USER_BUBBLE if is_user else MIS_BUBBLE
        anchor_side = "e" if is_user else "w"

        bubble = tk.Label(
            outer,
            text=message,
            wraplength=500,
            justify="left",
            bg=bubble_color,
            fg="white",
            font=("Arial", 11),
            padx=14,
            pady=10
        )
        bubble.pack(anchor=anchor_side)

        name_label = tk.Label(
            outer,
            text=speaker,
            bg="#0b1120",
            fg=SECONDARY_TEXT,
            font=("Arial", 9, "italic")
        )
        name_label.pack(anchor=anchor_side, pady=(2, 0))

        self.root.update_idletasks()
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1.0)

    def save_current_history(self):
        if self.username is not None:
            save_history(self.username, self.history)

    def send_message(self, event=None):
        question = self.question_entry.get().strip()

        if not question:
            return

        self.add_bubble("Tu", question)
        self.history.append({"speaker": "Tu", "message": question})
        self.question_entry.delete(0, tk.END)

        mode = self.mode_var.get()

        if mode == "ai":
            try:
                answer = generate_ai_response(
                    question,
                    self.profile,
                    self.profile["display_name"],
                    self.profile["username"]
                )
            except Exception as e:
                answer = (
                    f"Eroare AI: {e}\n"
                    f"Folosesc raspuns local.\n"
                    f"{generate_local_response(question, self.profile)}"
                )
        else:
            answer = generate_local_response(question, self.profile)

        self.add_bubble("MIS", answer)
        self.history.append({"speaker": "MIS", "message": answer})
        self.save_current_history()


if __name__ == "__main__":
    root = tk.Tk()
    app = MISApp(root)
    root.mainloop()
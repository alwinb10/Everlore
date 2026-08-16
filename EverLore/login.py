import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

import os

from db import fetch_one
from dashboard import Dashboard
import theme


# ---------------- Appearance ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


REMEMBER_FILE = "remember.txt"


class LoginApp:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title("EVERLORE - Login")
        self.root.geometry("450x650")
        self.root.resizable(False, False)

        self.root.configure(fg_color=theme.BG)

        self.center_window()

        # ---------------- Main Card ----------------

        self.card = ctk.CTkFrame(
            self.root,
            width=360,
            height=570,
            fg_color=theme.CARD,
            corner_radius=25
        )

        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ---------------- Logo ----------------

        logo_path = os.path.join(
            "assets",
            "logo.png"
        )

        if os.path.exists(logo_path):

            logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(90, 90)
            )

            self.logo = ctk.CTkLabel(
                self.card,
                text="",
                image=logo_image
            )

            self.logo.pack(
                pady=(35, 10)
            )

        else:

            self.logo = ctk.CTkLabel(
                self.card,
                text="EVERLORE",
                font=("Georgia", 30, "bold")
            )

            self.logo.pack(
                pady=(45, 20)
            )


        # ---------------- Title ----------------

        ctk.CTkLabel(
            self.card,
            text="Welcome Back",
            font=theme.TITLE
        ).pack(
            pady=(10, 5)
        )


        ctk.CTkLabel(
            self.card,
            text="Login to your personal media library",
            font=theme.SUBTITLE,
            text_color=theme.SUBTEXT
        ).pack(
            pady=(0, 25)
        )


        # ---------------- Username ----------------

        self.username_entry = ctk.CTkEntry(
            self.card,
            width=280,
            height=45,
            placeholder_text="Username",
            font=theme.BODY,
            corner_radius=10
        )

        self.username_entry.pack(
            pady=10
        )


        # ---------------- Password ----------------

        self.password_entry = ctk.CTkEntry(
            self.card,
            width=280,
            height=45,
            placeholder_text="Password",
            show="*",
            font=theme.BODY,
            corner_radius=10
        )

        self.password_entry.pack(
            pady=10
        )


        # ---------------- Show Password ----------------

        self.show_password = ctk.BooleanVar()

        self.show_password_check = ctk.CTkCheckBox(
            self.card,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password,
            font=("Segoe UI", 13)
        )

        self.show_password_check.pack(
            anchor="w",
            padx=40,
            pady=5
        )


        # ---------------- Remember Me ----------------

        self.remember = ctk.BooleanVar()

        self.remember_check = ctk.CTkCheckBox(
            self.card,
            text="Remember Me",
            variable=self.remember,
            font=("Segoe UI", 13)
        )

        self.remember_check.pack(
            anchor="w",
            padx=40,
            pady=5
        )


        # ---------------- Login Button ----------------

        self.login_btn = ctk.CTkButton(
            self.card,
            text="LOGIN",
            width=280,
            height=45,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            fg_color="#FFFFFF",
            text_color="#000000",
            hover_color="#CFCFCF",
            command=self.login
        )

        self.login_btn.pack(
            pady=(25, 10)
        )


        # ---------------- Links ----------------

        ctk.CTkButton(
            self.card,
            text="Forgot Password?",
            fg_color="transparent",
            hover_color=theme.HOVER,
            font=("Segoe UI", 12),
            command=self.forgot_password
        ).pack()


        ctk.CTkButton(
            self.card,
            text="Create Account",
            fg_color="transparent",
            hover_color=theme.HOVER,
            font=("Segoe UI", 12),
            command=self.create_account
        ).pack(
            pady=5
        )


        # ---------------- Footer ----------------

        ctk.CTkLabel(
            self.card,
            text="EVERLORE • Your Personal Media Archive",
            font=("Segoe UI", 11),
            text_color=theme.SUBTEXT
        ).pack(
            pady=(20, 10)
        )


        self.load_remembered_user()


    # ==================================================

    def center_window(self):

        self.root.update_idletasks()

        width = 450
        height = 650

        x = (
            self.root.winfo_screenwidth() // 2
            - width // 2
        )

        y = (
            self.root.winfo_screenheight() // 2
            - height // 2
        )

        self.root.geometry(
            f"{width}x{height}+{x}+{y}"
        )


    # ==================================================

    def toggle_password(self):

        if self.show_password.get():

            self.password_entry.configure(
                show=""
            )

        else:

            self.password_entry.configure(
                show="*"
            )


    # ==================================================

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()


        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )

            return


        user = fetch_one(
            """
            SELECT *
            FROM users
            WHERE username=%s
            AND password=%s
            """,
            (username, password)
        )


        if user:

            if self.remember.get():

                with open(
                    REMEMBER_FILE,
                    "w"
                ) as file:

                    file.write(username)

            else:

                if os.path.exists(REMEMBER_FILE):

                    os.remove(REMEMBER_FILE)


            full_name = user["full_name"]

            self.root.destroy()

            Dashboard(full_name).run()


        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )


    # ==================================================

    def load_remembered_user(self):

        if os.path.exists(REMEMBER_FILE):

            with open(
                REMEMBER_FILE,
                "r"
            ) as file:

                username = file.read()

                self.username_entry.insert(
                    0,
                    username
                )

                self.remember.set(True)


    # ==================================================

    def forgot_password(self):

        messagebox.showinfo(
            "Forgot Password",
            "Please contact an administrator to reset your password."
        )


    # ==================================================

    def create_account(self):

        messagebox.showinfo(
            "Create Account",
            "Account creation will be added later."
        )


    # ==================================================

    def run(self):

        self.root.mainloop()



if __name__ == "__main__":

    app = LoginApp()
    app.run()

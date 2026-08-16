import customtkinter as ctk
import theme


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent, dashboard):

        super().__init__(
            parent,
            fg_color=theme.get_color("BG")
        )

        self.dashboard = dashboard

        self.create_ui()


    # ==================================================

    def create_ui(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(30,20)
        )


        ctk.CTkLabel(
            header,
            text="⚙ Settings",
            font=theme.TITLE,
            text_color=theme.get_color("TEXT")
        ).pack(
            anchor="w"
        )


        ctk.CTkLabel(
            header,
            text="Customize your EVERLORE experience",
            font=theme.SUBTITLE,
            text_color=theme.get_color("SUBTEXT")
        ).pack(
            anchor="w"
        )


        # ---------------- Account ----------------


        account_card = ctk.CTkFrame(
            self,
            fg_color=theme.get_color("CARD"),
            corner_radius=18
        )

        account_card.pack(
            fill="x",
            padx=40,
            pady=15
        )


        ctk.CTkLabel(
            account_card,
            text="👤 Account",
            font=theme.HEADING,
            text_color=theme.get_color("TEXT")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20,10)
        )


        ctk.CTkLabel(
            account_card,
            text=f"Logged in as: {self.dashboard.username}",
            font=theme.BODY,
            text_color=theme.get_color("SUBTEXT")
        ).pack(
            anchor="w",
            padx=25,
            pady=(0,20)
        )


        # ---------------- Theme ----------------


        theme_card = ctk.CTkFrame(
            self,
            fg_color=theme.get_color("CARD"),
            corner_radius=18
        )

        theme_card.pack(
            fill="x",
            padx=40,
            pady=15
        )


        ctk.CTkLabel(
            theme_card,
            text="🎨 Appearance",
            font=theme.HEADING,
            text_color=theme.get_color("TEXT")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20,15)
        )


        self.theme_option = ctk.CTkOptionMenu(
            theme_card,
            values=[
                "Dark",
                "Light"
            ],
            width=180
        )

        self.theme_option.pack(
            padx=25,
            pady=10,
            anchor="w"
        )


        ctk.CTkButton(
            theme_card,
            text="Apply Theme",
            command=self.change_theme
        ).pack(
            padx=25,
            pady=(5,20),
            anchor="w"
        )


        # ---------------- Logout ----------------


        ctk.CTkButton(
            self,
            text="🚪 Logout",
            width=180,
            command=self.dashboard.logout
        ).pack(
            pady=30
        )


    # ==================================================

    def change_theme(self):

        selected = self.theme_option.get()


        if selected == "Light":

            theme.set_theme("light")

        else:

            theme.set_theme("dark")


        self.dashboard.refresh_theme()

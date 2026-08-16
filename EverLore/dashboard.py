import customtkinter as ctk

from db import fetch_value

from pages.movies import MoviesPage
from pages.series import SeriesPage
from pages.books import BooksPage
from pages.favorites import FavoritesPage
from pages.statistics import StatisticsPage

import theme


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class Dashboard:

    def __init__(self, username="User"):

        self.username = username
        self.current_page = "home"

        # ---------------- Window ----------------

        self.root = ctk.CTk()

        self.root.title("EVERLORE")

        self.root.state("zoomed")

        self.root.configure(
            fg_color=theme.get_color("BG")
        )


        # ---------------- Sidebar ----------------

        self.sidebar_frame = ctk.CTkFrame(
            self.root,
            width=240,
            fg_color=theme.get_color("SIDEBAR"),
            corner_radius=0
        )

        self.sidebar_frame.pack(
            side="left",
            fill="y"
        )


        # ---------------- Logo ----------------

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="EVERLORE",
            font=("Georgia",30,"bold"),
            text_color=theme.get_color("TEXT")
        )

        self.logo_label.pack(
            pady=(35,60)
        )


        # ---------------- Navigation ----------------

        self.home_btn = self.create_sidebar_button(
            "🏠  Home"
        )

        self.movies_btn = self.create_sidebar_button(
            "🎬  Movies"
        )

        self.series_btn = self.create_sidebar_button(
            "📺  Series"
        )

        self.books_btn = self.create_sidebar_button(
            "📚  Books"
        )

        self.favorites_btn = self.create_sidebar_button(
            "⭐  Favorites"
        )

        self.statistics_btn = self.create_sidebar_button(
            "📊  Statistics"
        )

        self.settings_btn = self.create_sidebar_button(
            "⚙  Settings"
        )


        ctk.CTkLabel(
            self.sidebar_frame,
            text=""
        ).pack(
            expand=True
        )


        self.logout_btn = self.create_sidebar_button(
            "🚪  Logout"
        )


        # ---------------- Content ----------------

        self.content = ctk.CTkFrame(
            self.root,
            fg_color=theme.get_color("BG"),
            corner_radius=0
        )

        self.content.pack(
            fill="both",
            expand=True
        )


    # ==================================================

    def create_sidebar_button(self, text):

        button = ctk.CTkButton(
            self.sidebar_frame,
            text=text,
            width=200,
            height=45,
            anchor="w",
            fg_color="transparent",
            hover_color=theme.get_color("HOVER"),
            corner_radius=10,
            font=theme.BODY,
            text_color=theme.get_color("TEXT")
        )

        button.pack(
            pady=6,
            padx=20
        )

        return button


    # ==================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()


    # ==================================================

    def refresh_theme(self):

        """
        Refresh dashboard colors after theme change.
        """

        self.root.configure(
            fg_color=theme.get_color("BG")
        )

        self.sidebar_frame.configure(
            fg_color=theme.get_color("SIDEBAR")
        )

        self.content.configure(
            fg_color=theme.get_color("BG")
        )

        self.logo_label.configure(
            text_color=theme.get_color("TEXT")
        )


        for button in [
            self.home_btn,
            self.movies_btn,
            self.series_btn,
            self.books_btn,
            self.favorites_btn,
            self.statistics_btn,
            self.settings_btn,
            self.logout_btn
        ]:

            button.configure(
                hover_color=theme.get_color("HOVER"),
                text_color=theme.get_color("TEXT")
            )


        self.show_home()


    # ==================================================

    def show_home(self):

        self.current_page = "home"

        self.clear_content()


        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(35,20)
        )


        ctk.CTkLabel(
            header,
            text=f"Welcome back, {self.username}",
            font=theme.TITLE,
            text_color=theme.get_color("TEXT")
        ).pack(
            anchor="w"
        )


        ctk.CTkLabel(
            header,
            text="Your Personal Media Library",
            font=theme.SUBTITLE,
            text_color=theme.get_color("SUBTEXT")
        ).pack(
            anchor="w"
        )


        cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards_frame.pack(
            padx=40,
            pady=20,
            fill="x"
        )


        stats = [

            (
                "🎬 Movies",
                fetch_value(
                    "SELECT COUNT(*) FROM movies"
                )
            ),

            (
                "📺 Series",
                fetch_value(
                    "SELECT COUNT(*) FROM series"
                )
            ),

            (
                "📚 Books",
                fetch_value(
                    "SELECT COUNT(*) FROM books"
                )
            ),

            (
                "⭐ Favorites",
                fetch_value(
                    "SELECT COUNT(*) FROM movies WHERE favorite=1"
                )
                +
                fetch_value(
                    "SELECT COUNT(*) FROM series WHERE favorite=1"
                )
                +
                fetch_value(
                    "SELECT COUNT(*) FROM books WHERE favorite=1"
                )
            )

        ]


        for title,value in stats:

            card = ctk.CTkFrame(
                cards_frame,
                width=200,
                height=130,
                fg_color=theme.get_color("CARD"),
                corner_radius=18
            )

            card.pack(
                side="left",
                padx=12
            )

            card.pack_propagate(False)


            ctk.CTkLabel(
                card,
                text=str(value),
                font=theme.BIG,
                text_color=theme.get_color("TEXT")
            ).pack(
                pady=(25,5)
            )


            ctk.CTkLabel(
                card,
                text=title,
                font=theme.BODY,
                text_color=theme.get_color("SUBTEXT")
            ).pack()


        recent = ctk.CTkFrame(
            self.content,
            fg_color=theme.get_color("CARD"),
            corner_radius=18
        )

        recent.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )


        ctk.CTkLabel(
            recent,
            text="Recently Added",
            font=theme.HEADING,
            text_color=theme.get_color("TEXT")
        ).pack(
            anchor="w",
            padx=25,
            pady=25
        )


        ctk.CTkLabel(
            recent,
            text="Your recently added movies, series and books will appear here.",
            font=theme.BODY,
            text_color=theme.get_color("SUBTEXT")
        ).pack(
            anchor="w",
            padx=25
        )
    # ==================================================

    def show_movies(self):

        self.current_page = "movies"

        self.clear_content()

        MoviesPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )


    # ==================================================

    def show_series(self):

        self.current_page = "series"

        self.clear_content()

        SeriesPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )


    # ==================================================

    def show_books(self):

        self.current_page = "books"

        self.clear_content()

        BooksPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )


    # ==================================================

    def show_favorites(self):

        self.current_page = "favorites"

        self.clear_content()

        FavoritesPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )


    # ==================================================

    def show_statistics(self):

        self.current_page = "statistics"

        self.clear_content()

        StatisticsPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )


    # ==================================================

    def show_settings(self):

        self.current_page = "settings"

        self.clear_content()

        try:

            from pages.settings import SettingsPage

            SettingsPage(
                self.content,
                self
            ).pack(
                fill="both",
                expand=True
            )

        except ImportError:

            ctk.CTkLabel(
                self.content,
                text="⚙ Settings\nComing Soon",
                font=theme.TITLE,
                text_color=theme.get_color("TEXT")
            ).pack(
                pady=100
            )


    # ==================================================

    def logout(self):

        self.root.destroy()


    # ==================================================

    def run(self):

        self.home_btn.configure(
            command=self.show_home
        )

        self.movies_btn.configure(
            command=self.show_movies
        )

        self.series_btn.configure(
            command=self.show_series
        )

        self.books_btn.configure(
            command=self.show_books
        )

        self.favorites_btn.configure(
            command=self.show_favorites
        )

        self.statistics_btn.configure(
            command=self.show_statistics
        )

        self.settings_btn.configure(
            command=self.show_settings
        )

        self.logout_btn.configure(
            command=self.logout
        )


        self.show_home()


        self.root.mainloop()



# ==================================================

if __name__ == "__main__":

    Dashboard("Alwin").run()        

import customtkinter as ctk
from db import fetch_value


class StatisticsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#0D0D0D")

        self.create_ui()

    # ==================================================

    def create_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))

        ctk.CTkLabel(
            header,
            text="📊 Statistics",
            font=("Georgia", 32, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Overview of your EVERLORE library",
            font=("Segoe UI", 16),
            text_color="gray"
        ).pack(anchor="w")

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        container.pack(fill="both", expand=True, padx=40, pady=20)

        stats = [

            ("🎬 Total Movies",
             fetch_value("SELECT COUNT(*) FROM movies")),

            ("📺 Total Series",
             fetch_value("SELECT COUNT(*) FROM series")),

            ("📚 Total Books",
             fetch_value("SELECT COUNT(*) FROM books")),

            ("⭐ Total Favorites",
             fetch_value("SELECT COUNT(*) FROM movies WHERE favorite=1") +
             fetch_value("SELECT COUNT(*) FROM series WHERE favorite=1") +
             fetch_value("SELECT COUNT(*) FROM books WHERE favorite=1")),

            ("👁 Total Watchlist",
             fetch_value("SELECT COUNT(*) FROM movies WHERE watchlist=1") +
             fetch_value("SELECT COUNT(*) FROM series WHERE watchlist=1") +
             fetch_value("SELECT COUNT(*) FROM books WHERE watchlist=1")),

            ("⭐ Avg Movie Rating",
             round(fetch_value("SELECT AVG(rating) FROM movies") or 0, 1)),

            ("⭐ Avg Series Rating",
             round(fetch_value("SELECT AVG(rating) FROM series") or 0, 1)),

            ("⭐ Avg Book Rating",
             round(fetch_value("SELECT AVG(rating) FROM books") or 0, 1))
        ]

        row = None

        for i, (title, value) in enumerate(stats):

            if i % 2 == 0:
                row = ctk.CTkFrame(
                    container,
                    fg_color="transparent"
                )
                row.pack(fill="x", pady=10)

            card = ctk.CTkFrame(
                row,
                fg_color="#1A1A1A",
                corner_radius=15,
                width=350,
                height=120
            )

            card.pack(side="left", padx=10, expand=True, fill="x")
            card.pack_propagate(False)

            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Segoe UI", 30, "bold")
            ).pack(pady=(20, 5))

            ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI", 15),
                text_color="gray"
            ).pack()

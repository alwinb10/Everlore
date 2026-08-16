import customtkinter as ctk
from db import fetch_all, execute_query


class SeriesPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#0D0D0D")

        self.series = []

        self.create_ui()
        self.load_series()

    # ==================================================

    def create_ui(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(30, 10)
        )

        ctk.CTkLabel(
            header,
            text="📺 Series",
            font=("Georgia", 32, "bold")
        ).pack(anchor="w")


        ctk.CTkLabel(
            header,
            text="Your personal series collection",
            font=("Segoe UI", 16),
            text_color="gray"
        ).pack(anchor="w")


        top_bar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top_bar.pack(
            fill="x",
            padx=40,
            pady=20
        )


        self.search_entry = ctk.CTkEntry(
            top_bar,
            width=420,
            height=42,
            placeholder_text="Search series..."
        )

        self.search_entry.pack(side="left")

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_series
        )


        self.sort_var = ctk.StringVar(
            value="Title (A-Z)"
        )


        self.sort_menu = ctk.CTkOptionMenu(
            top_bar,
            values=[
                "Title (A-Z)",
                "Title (Z-A)",
                "Highest Rating",
                "Lowest Rating",
                "Newest",
                "Oldest"
            ],
            variable=self.sort_var,
            command=self.sort_series,
            width=180
        )

        self.sort_menu.pack(
            side="left",
            padx=15
        )


        self.random_btn = ctk.CTkButton(
            top_bar,
            text="🎲 Pick Random",
            width=140,
            command=self.pick_random
        )

        self.random_btn.pack(
            side="left"
        )


        self.series_container = ctk.CTkScrollableFrame(
            self,
            fg_color="#0D0D0D"
        )

        self.series_container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0,30)
        )

    # ==================================================

    def load_series(self):

        query = """
        SELECT
            series_id,
            title,
            release_year,
            final_year,
            seasons,
            episodes,
            genre,
            language,
            rating,
            favorite,
            watchlist
        FROM series
        ORDER BY title;
        """

        self.series = fetch_all(query)

        self.display_series(self.series)

    # ==================================================

    def display_series(self, series):

        for widget in self.series_container.winfo_children():
            widget.destroy()


        for item in series:

            card = ctk.CTkFrame(
                self.series_container,
                fg_color="#1A1A1A",
                corner_radius=15
            )

            card.pack(
                fill="x",
                pady=8
            )


            ctk.CTkLabel(
                card,
                text=item["title"],
                font=("Segoe UI",22,"bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(15,5)
            )


            details = (
                f'{item["release_year"] or "N/A"} - '
                f'{item["final_year"] or "N/A"}   •   '
                f'{item["seasons"] or 0} Seasons   •   '
                f'{item["episodes"] or 0} Episodes   •   '
                f'⭐ {item["rating"] or "N/A"}'
            )


            bottom = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            bottom.pack(
                fill="x",
                padx=20,
                pady=(0,15)
            )


            ctk.CTkLabel(
                bottom,
                text=details,
                font=("Segoe UI",15),
                text_color="gray"
            ).pack(
                side="left"
            )


            buttons = ctk.CTkFrame(
                bottom,
                fg_color="transparent"
            )

            buttons.pack(
                side="right"
            )


            fav_icon = "❤️" if item["favorite"] else "🤍"

            watch_icon = "👁" if item["watchlist"] else "➕"


            ctk.CTkButton(
                buttons,
                text=fav_icon,
                width=40,
                fg_color="transparent",
                hover_color="#2A2A2A",
                command=lambda s=item:self.toggle_favorite(s)
            ).pack(
                side="left",
                padx=5
            )


            ctk.CTkButton(
                buttons,
                text=watch_icon,
                width=40,
                fg_color="transparent",
                hover_color="#2A2A2A",
                command=lambda s=item:self.toggle_watchlist(s)
            ).pack(
                side="left"
            )

    # ==================================================

    def search_series(self,event=None):

        text = self.search_entry.get().lower().strip()

        series = self.series

        if text:
            series = [
                s for s in series
                if text in s["title"].lower()
            ]

        self.display_series(series)

    # ==================================================

    def sort_series(self,choice):

        series = self.series.copy()


        if choice == "Title (A-Z)":
            series.sort(
                key=lambda x:x["title"].lower()
            )


        elif choice == "Title (Z-A)":
            series.sort(
                key=lambda x:x["title"].lower(),
                reverse=True
            )


        elif choice == "Highest Rating":
            series.sort(
                key=lambda x:float(x["rating"] or 0),
                reverse=True
            )


        elif choice == "Lowest Rating":
            series.sort(
                key=lambda x:float(x["rating"] or 0)
            )


        elif choice == "Newest":
            series.sort(
                key=lambda x:int(x["release_year"] or 0),
                reverse=True
            )


        elif choice == "Oldest":
            series.sort(
                key=lambda x:int(x["release_year"] or 0)
            )


        self.display_series(series)

    # ==================================================

    def toggle_favorite(self,item):

        value = not item["favorite"]

        execute_query(
            """
            UPDATE series
            SET favorite=%s
            WHERE series_id=%s
            """,
            (
                value,
                item["series_id"]
            )
        )

        self.load_series()


    def toggle_watchlist(self,item):

        value = not item["watchlist"]

        execute_query(
            """
            UPDATE series
            SET watchlist=%s
            WHERE series_id=%s
            """,
            (
                value,
                item["series_id"]
            )
        )

        self.load_series()

    # ==================================================

    def pick_random(self):

        import random

        if not self.series:
            return


        item = random.choice(self.series)


        self.search_entry.delete(
            0,
            "end"
        )

        self.search_entry.insert(
            0,
            item["title"]
        )

        self.display_series([item])

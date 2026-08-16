import customtkinter as ctk
from db import fetch_all, execute_query


class MoviesPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#0D0D0D")

        self.movies = []

        self.create_ui()
        self.load_movies()

    # ==================================================

    def create_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 10))

        ctk.CTkLabel(
            header,
            text="🎬 Movies",
            font=("Georgia", 32, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Your personal movie collection",
            font=("Segoe UI", 16),
            text_color="gray"
        ).pack(anchor="w")


        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=40, pady=(20, 20))


        self.search_entry = ctk.CTkEntry(
            top_bar,
            width=420,
            height=42,
            placeholder_text="Search movies..."
        )

        self.search_entry.pack(side="left")
        self.search_entry.bind(
            "<KeyRelease>",
            self.search_movies
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
            command=self.sort_movies,
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

        self.random_btn.pack(side="left")


        self.movie_container = ctk.CTkScrollableFrame(
            self,
            fg_color="#0D0D0D"
        )

        self.movie_container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 30)
        )

    # ==================================================

    def load_movies(self):

        query = """
        SELECT
            movie_id,
            title,
            release_year,
            genre,
            language,
            rating,
            favorite,
            watchlist
        FROM movies
        ORDER BY title;
        """

        self.movies = fetch_all(query)

        self.display_movies(self.movies)

    # ==================================================

    def display_movies(self, movies):

        for widget in self.movie_container.winfo_children():
            widget.destroy()


        for movie in movies:

            card = ctk.CTkFrame(
                self.movie_container,
                fg_color="#1A1A1A",
                corner_radius=15
            )

            card.pack(
                fill="x",
                pady=8
            )


            ctk.CTkLabel(
                card,
                text=movie["title"],
                font=("Segoe UI", 22, "bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(15, 5)
            )


            details = (
                f'{movie["release_year"] or "N/A"}   •   '
                f'{movie["genre"] or "Unknown"}   •   '
                f'{movie["language"] or "Unknown"}   •   '
                f'⭐ {movie["rating"] or "N/A"}'
            )


            bottom = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            bottom.pack(
                fill="x",
                padx=20,
                pady=(0, 15)
            )


            ctk.CTkLabel(
                bottom,
                text=details,
                font=("Segoe UI", 15),
                text_color="gray"
            ).pack(
                side="left"
            )


            button_frame = ctk.CTkFrame(
                bottom,
                fg_color="transparent"
            )

            button_frame.pack(
                side="right"
            )


            fav_icon = (
                "❤️"
                if movie["favorite"]
                else "🤍"
            )


            watch_icon = (
                "👁"
                if movie["watchlist"]
                else "➕"
            )


            ctk.CTkButton(
                button_frame,
                text=fav_icon,
                width=40,
                fg_color="transparent",
                hover_color="#2A2A2A",
                command=lambda m=movie:
                    self.toggle_favorite(m)
            ).pack(
                side="left",
                padx=5
            )


            ctk.CTkButton(
                button_frame,
                text=watch_icon,
                width=40,
                fg_color="transparent",
                hover_color="#2A2A2A",
                command=lambda m=movie:
                    self.toggle_watchlist(m)
            ).pack(
                side="left"
            )

    # ==================================================

    def search_movies(self, event=None):

        text = self.search_entry.get().lower().strip()

        movies = self.movies

        if text:
            movies = [
                movie for movie in movies
                if text in movie["title"].lower()
            ]

        self.display_movies(movies)

    # ==================================================

    def sort_movies(self, choice):

        movies = self.movies.copy()


        if choice == "Title (A-Z)":

            movies.sort(
                key=lambda x: x["title"].lower()
            )


        elif choice == "Title (Z-A)":

            movies.sort(
                key=lambda x: x["title"].lower(),
                reverse=True
            )


        elif choice == "Highest Rating":

            movies.sort(
                key=lambda x: float(x["rating"] or 0),
                reverse=True
            )


        elif choice == "Lowest Rating":

            movies.sort(
                key=lambda x: float(x["rating"] or 0)
            )


        elif choice == "Newest":

            movies.sort(
                key=lambda x: int(x["release_year"] or 0),
                reverse=True
            )


        elif choice == "Oldest":

            movies.sort(
                key=lambda x: int(x["release_year"] or 0)
            )


        self.display_movies(movies)

    # ==================================================

    def toggle_favorite(self, movie):

        new_value = not movie["favorite"]

        execute_query(
            """
            UPDATE movies
            SET favorite=%s
            WHERE movie_id=%s
            """,
            (
                new_value,
                movie["movie_id"]
            )
        )

        self.load_movies()

    # ==================================================

    def toggle_watchlist(self, movie):

        new_value = not movie["watchlist"]

        execute_query(
            """
            UPDATE movies
            SET watchlist=%s
            WHERE movie_id=%s
            """,
            (
                new_value,
                movie["movie_id"]
            )
        )

        self.load_movies()

    # ==================================================

    def pick_random(self):

        import random

        if not self.movies:
            return


        movie = random.choice(self.movies)

        self.search_entry.delete(
            0,
            "end"
        )

        self.search_entry.insert(
            0,
            movie["title"]
        )

        self.display_movies([movie])

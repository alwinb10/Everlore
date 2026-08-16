import customtkinter as ctk
from db import fetch_all, execute_query


class FavoritesPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#0D0D0D")

        self.create_ui()
        self.load_favorites()

    # ==================================================

    def create_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))

        ctk.CTkLabel(
            header,
            text="⭐ Favorites",
            font=("Georgia", 32, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Your favourite Movies, Series and Books",
            font=("Segoe UI", 16),
            text_color="gray"
        ).pack(anchor="w")

        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color="#0D0D0D"
        )

        self.container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 30)
        )

    # ==================================================

    def load_favorites(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        self.show_section(
            "🎬 Movies",
            fetch_all(
                "SELECT movie_id,title FROM movies WHERE favorite=1 ORDER BY title"
            ),
            "movies",
            "movie_id"
        )

        self.show_section(
            "📺 Series",
            fetch_all(
                "SELECT series_id,title FROM series WHERE favorite=1 ORDER BY title"
            ),
            "series",
            "series_id"
        )

        self.show_section(
            "📚 Books",
            fetch_all(
                "SELECT book_id,title FROM books WHERE favorite=1 ORDER BY title"
            ),
            "books",
            "book_id"
        )

    # ==================================================

    def show_section(self, title, data, table, id_column):

        section = ctk.CTkFrame(
            self.container,
            fg_color="#1A1A1A",
            corner_radius=15
        )

        section.pack(fill="x", pady=12)

        ctk.CTkLabel(
            section,
            text=title,
            font=("Georgia", 22, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        if not data:

            ctk.CTkLabel(
                section,
                text="No favourites yet.",
                text_color="gray"
            ).pack(anchor="w", padx=20, pady=(0, 15))

            return

        for item in data:

            row = ctk.CTkFrame(
                section,
                fg_color="transparent"
            )

            row.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                row,
                text=item["title"],
                font=("Segoe UI", 16)
            ).pack(side="left")

            ctk.CTkButton(
                row,
                text="❤️",
                width=40,
                fg_color="transparent",
                hover_color="#2A2A2A",
                command=lambda i=item, t=table, c=id_column:
                    self.remove_favorite(i, t, c)
            ).pack(side="right")

    # ==================================================

    def remove_favorite(self, item, table, id_column):

        execute_query(
            f"UPDATE {table} SET favorite=0 WHERE {id_column}=%s",
            (item[id_column],)
        )

        self.load_favorites()

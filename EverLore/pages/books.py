import customtkinter as ctk
from db import fetch_all, execute_query


class BooksPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#0D0D0D")

        self.books = []

        self.create_ui()
        self.load_books()

    # ==================================================

    def create_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 10))

        ctk.CTkLabel(
            header,
            text="📚 Books",
            font=("Georgia", 32, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Your personal book collection",
            font=("Segoe UI", 16),
            text_color="gray"
        ).pack(anchor="w")

        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=40, pady=20)

        self.search_entry = ctk.CTkEntry(
            top_bar,
            width=420,
            height=42,
            placeholder_text="Search books..."
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self.search_books)

        self.sort_var = ctk.StringVar(value="Title (A-Z)")

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
            command=self.sort_books,
            width=180
        )
        self.sort_menu.pack(side="left", padx=15)

        self.random_btn = ctk.CTkButton(
            top_bar,
            text="🎲 Pick Random",
            width=140,
            command=self.pick_random
        )
        self.random_btn.pack(side="left")

        self.book_container = ctk.CTkScrollableFrame(
            self,
            fg_color="#0D0D0D"
        )
        self.book_container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 30)
        )

    # ==================================================

    def load_books(self):

        query = """
        SELECT
            book_id,
            title,
            author,
            publication_year,
            genre,
            pages,
            rating,
            favorite,
            watchlist
        FROM books
        ORDER BY title;
        """

        self.books = fetch_all(query)

        self.display_books(self.books)

    # ==================================================

    def display_books(self, books):

        for widget in self.book_container.winfo_children():
            widget.destroy()

        for book in books:

            card = ctk.CTkFrame(
                self.book_container,
                fg_color="#1A1A1A",
                corner_radius=15
            )
            card.pack(fill="x", pady=8)

            ctk.CTkLabel(
                card,
                text=book["title"],
                font=("Segoe UI", 22, "bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))

            details = (
                f'{book["author"] or "Unknown"}   •   '
                f'{book["publication_year"] or "N/A"}   •   '
                f'{book["genre"] or "Unknown"}   •   '
                f'{book["pages"] or 0} Pages   •   '
                f'⭐ {book["rating"] or "N/A"}'
            )

            bottom = ctk.CTkFrame(card, fg_color="transparent")
            bottom.pack(fill="x", padx=20, pady=(0, 15))

            ctk.CTkLabel(
                bottom,
                text=details,
                font=("Segoe UI", 15),
                text_color="gray"
            ).pack(side="left")

            buttons = ctk.CTkFrame(bottom, fg_color="transparent")
            buttons.pack(side="right")

            fav_icon = "❤️" if book["favorite"] else "🤍"
            watch_icon = "👁" if book["watchlist"] else "➕"

            ctk.CTkButton(
                buttons,
                text=fav_icon,
                width=40,
                fg_color="transparent",
                hover_color="#2A2A2A",
                command=lambda b=book: self.toggle_favorite(b)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                buttons,
                text=watch_icon,
                width=40,
                fg_color="transparent",
                hover_color="#2A2A2A",
                command=lambda b=book: self.toggle_watchlist(b)
            ).pack(side="left")

    # ==================================================

    def search_books(self, event=None):

        text = self.search_entry.get().lower().strip()

        books = self.books

        if text:
            books = [
                b for b in books
                if text in b["title"].lower()
            ]

        self.display_books(books)

    # ==================================================

    def sort_books(self, choice):

        books = self.books.copy()

        if choice == "Title (A-Z)":
            books.sort(key=lambda x: x["title"].lower())

        elif choice == "Title (Z-A)":
            books.sort(key=lambda x: x["title"].lower(), reverse=True)

        elif choice == "Highest Rating":
            books.sort(key=lambda x: float(x["rating"] or 0), reverse=True)

        elif choice == "Lowest Rating":
            books.sort(key=lambda x: float(x["rating"] or 0))

        elif choice == "Newest":
            books.sort(key=lambda x: int(x["publication_year"] or 0), reverse=True)

        elif choice == "Oldest":
            books.sort(key=lambda x: int(x["publication_year"] or 0))

        self.display_books(books)

    # ==================================================

    def toggle_favorite(self, book):

        execute_query(
            "UPDATE books SET favorite=%s WHERE book_id=%s",
            (not book["favorite"], book["book_id"])
        )

        self.load_books()

    # ==================================================

    def toggle_watchlist(self, book):

        execute_query(
            "UPDATE books SET watchlist=%s WHERE book_id=%s",
            (not book["watchlist"], book["book_id"])
        )

        self.load_books()

    # ==================================================

    def pick_random(self):

        import random

        if not self.books:
            return

        book = random.choice(self.books)

        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, book["title"])

        self.display_books([book])

EVERLORE

EVERLORE is a premium desktop media management application designed to organize and manage personal collections of movies, TV series, and books.

Built using Python, CustomTkinter, and MySQL, EVERLORE provides a clean, modern, and elegant interface inspired by IMDb and personal digital libraries.

Features
🎬 Movies
Add and manage movie collections
Search movies
Sort by title, rating, and release year
Mark favorites
Create a watchlist
📺 TV Series
Manage TV series collections
Search and sort series
Track favorites and watchlist
📚 Books
Organize personal book collections
Search and sort books
Manage favorites
⭐ Favorites
View all favorite movies, series, and books in one place
📊 Statistics
View library statistics:
Total movies
Total series
Total books
Favorites
Ratings overview
⚙ Settings
Account management
Dark and light theme support
Technologies Used
Python
CustomTkinter
MySQLEverLore/
mysql-connector-python
Pillow
program structure
│
├── main.py              # Application launcher
├── login.py             # User authentication
├── dashboard.py         # Main application dashboard
├── db.py                # Database connection
├── theme.py             # Theme management
├── everlore.sql         # Database backup
│
├── assets/
│   └── logo.png
│
└── pages/
    ├── movies.py
    ├── series.py
    ├── books.py
    ├── favorites.py
    ├── statistics.py
    └── settings.py
Database

EVERLORE uses MySQL to store:

User accounts
Movie collections
TV series collections
Book collections
Favorites and watchlists
Purpose

EVERLORE was created as a personal media archive project to explore desktop application development, database management, and GUI design using Python.

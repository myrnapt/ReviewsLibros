import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "myrna",
    "password": "proven",
    "database": "projecte_myrna",
}

# Función para conectar a la BD  usando las credenciales definidas arriba
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------- USERS ----------
def create_user(username: str, password: str) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass


def get_user_by_username(username: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id, username, password FROM users WHERE username = %s",
        (username,),
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# ---------- BOOKS ----------
def list_books_ordered_by_title():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT id, title, author, synopsis, year, genre, image_filename
        FROM books
        ORDER BY title ASC, author ASC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def search_books(q: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    like = f"%{q}%"
    cur.execute(
        """
        SELECT id, title, author, synopsis, year, genre, image_filename
        FROM books
        WHERE title LIKE %s OR author LIKE %s
        ORDER BY author ASC, title ASC
        """,
        (like, like),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_book(book_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT id, title, author, synopsis, year, genre, image_filename
        FROM books
        WHERE id = %s
        """,
        (book_id,),
    )
    book = cur.fetchone()
    cur.close()
    conn.close()
    return book


def set_book_image_if_missing(book_id: int, image_filename: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE books
        SET image_filename = %s
        WHERE id = %s AND (image_filename IS NULL OR image_filename = '')
        """,
        (image_filename, book_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def find_or_create_book(title: str, author: str, synopsis: str, year, genre, image_filename: str = None):
    """
    Opción B:
    - Busca por (title, author)
    - Si existe, devuelve id (y si falta imagen y la aportas, la guarda)
    - Si no existe, crea y devuelve id
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT id, image_filename FROM books WHERE title = %s AND author = %s",
        (title, author),
    )
    row = cur.fetchone()

    if row:
        book_id = row["id"]
        if image_filename and (row["image_filename"] is None or row["image_filename"] == ""):
            cur2 = conn.cursor()
            cur2.execute("UPDATE books SET image_filename = %s WHERE id = %s", (image_filename, book_id))
            conn.commit()
            cur2.close()
        cur.close()
        conn.close()
        return book_id

    cur2 = conn.cursor()
    cur2.execute(
        """
        INSERT INTO books (title, author, synopsis, year, genre, image_filename)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (title, author, synopsis, year, genre, image_filename),
    )
    conn.commit()
    book_id = cur2.lastrowid
    cur2.close()
    cur.close()
    conn.close()
    return book_id


# ---------- REVIEWS ----------
def add_review(user_id: int, book_id: int, rating: int, review_text: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO reviews (user_id, book_id, rating, review_text)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, book_id, rating, review_text),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_review(review_id: int, user_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM reviews WHERE id = %s AND user_id = %s",
        (review_id, user_id),
    )
    conn.commit()
    deleted = (cur.rowcount == 1)
    cur.close()
    conn.close()
    return deleted


def get_reviews_by_book(book_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT r.id, r.rating, r.review_text, r.created_at,
               u.username
        FROM reviews r
        JOIN users u ON u.id = r.user_id
        WHERE r.book_id = %s
        ORDER BY r.created_at DESC
        """,
        (book_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_reviews_by_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT r.id, r.rating, r.review_text, r.created_at,
               b.id AS book_id, b.title, b.author, b.image_filename AS book_image_filename
        FROM reviews r
        JOIN books b ON b.id = r.book_id
        WHERE r.user_id = %s
        ORDER BY r.created_at DESC
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_latest_reviews(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT r.id, r.rating, r.review_text, r.created_at,
               u.username,
               b.id AS book_id, b.title, b.author, b.image_filename AS book_image_filename
        FROM reviews r
        JOIN users u ON u.id = r.user_id
        JOIN books b ON b.id = r.book_id
        ORDER BY r.created_at DESC
        LIMIT %s
        """,
        (limit,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
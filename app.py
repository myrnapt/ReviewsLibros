import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

import db

app = Flask(__name__)
app.secret_key = "projecte_myrna_secret"

UPLOAD_DIR = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return {"id": user_id, "username": session.get("username")}


def save_uploaded_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return None
    safe = secure_filename(file_storage.filename)
    file_storage.save(os.path.join(UPLOAD_DIR, safe))
    return safe


@app.route("/")
def index():
    current_user = get_current_user()
    reviews = db.get_latest_reviews(10)
    return render_template("index.html", current_user=current_user, reviews=reviews, q=None)

@app.route("/search")
def search():
    current_user = get_current_user()
    search_term = request.args.get("search_term", "").strip()

    if search_term:
        books = db.search_books(search_term)
    else:
        books = db.list_books_ordered_by_title()
        for b in books:
            title = (b.get("title") or "").strip()
            b["first_letter"] = (title[0].upper() if title else "#")

    return render_template(
        "search.html",
        current_user=current_user,
        search_term=search_term,
        books=books
    )

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    current_user = get_current_user()
    book = db.get_book(book_id)
    if not book:
        return render_template("base.html", current_user=current_user, error="Libro no encontrado.")
    reviews = db.get_reviews_by_book(book_id)
    return render_template("book_detail.html", current_user=current_user, book=book, reviews=reviews)


@app.route("/register", methods=["GET", "POST"])
def register():
    current_user = get_current_user()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return render_template(
                "register.html",
                error="Todos los campos son obligatorios.",
                current_user=current_user
            )

        # Crear usuario en BD
        user_id = db.create_user(username, password)

        if not user_id:
            return render_template(
                "register.html",
                error="El usuario ya existe.",
                current_user=current_user
            )

        session["user_id"] = user_id
        session["username"] = username

        return redirect(url_for("profile"))

    return render_template("register.html", current_user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    current_user = get_current_user()
    if request.method == "GET":
        return render_template("login.html", current_user=current_user)

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = db.get_user_by_username(username)
    if not user or user["password"] != password:
        return render_template("login.html", error="Credenciales incorrectas.")

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return redirect(url_for("profile"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/profile")
def profile():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("login"))

    my_reviews = db.get_reviews_by_user(current_user["id"])
    msg = request.args.get("msg")
    error = request.args.get("error")
    return render_template("profile.html", current_user=current_user, my_reviews=my_reviews, msg=msg, error=error)


@app.route("/review/new", methods=["GET", "POST"])
def new_review():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("login"))

    all_books = db.list_books_ordered_by_title()

    if request.method == "GET":
        book_id_raw = request.args.get("book_id", "").strip()
        new_flag = request.args.get("new", "").strip()

        selected_book = None
        selected_book_id = None
        mode = "none"

        if book_id_raw.isdigit():
            selected_book_id = int(book_id_raw)
            selected_book = db.get_book(selected_book_id)
            mode = "existing" if selected_book else "none"
        elif new_flag == "1":
            mode = "new"

        return render_template(
            "new_review.html",
            current_user=current_user,
            books=all_books,
            selected_book=selected_book,
            selected_book_id=selected_book_id,
            mode=mode,
        )

    book_id_raw = request.form.get("book_id", "").strip()
    rating_raw = request.form.get("rating", "").strip()
    review_text = request.form.get("review_text", "").strip()

    if not rating_raw or not review_text:
        return render_template(
            "new_review.html",
            current_user=current_user,
            books=all_books,
            selected_book=None,
            selected_book_id=None,
            mode="none",
            error="Faltan datos obligatorios (rating y review).",
        )

    try:
        rating = int(rating_raw)
    except ValueError:
        rating = 0

    if rating < 1 or rating > 5:
        return render_template(
            "new_review.html",
            current_user=current_user,
            books=all_books,
            selected_book=None,
            selected_book_id=None,
            mode="none",
            error="Rating debe ser entre 1 y 5.",
        )

    image_file = request.files.get("image")
    image_filename = save_uploaded_image(image_file)

    # Caso A: libro existente
    if book_id_raw.isdigit():
        book_id = int(book_id_raw)

        if image_filename:
            db.set_book_image_if_missing(book_id, image_filename)

        db.add_review(current_user["id"], book_id, rating, review_text)
        return redirect(url_for("book_detail", book_id=book_id))

    # Caso B: crear nuevo libro
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    synopsis = request.form.get("synopsis", "").strip()
    year_raw = request.form.get("year", "").strip()
    genre = request.form.get("genre", "").strip()

    if not title or not author:
        return render_template(
            "new_review.html",
            current_user=current_user,
            books=all_books,
            selected_book=None,
            selected_book_id=None,
            mode="new",
            error="Para agregar libro nuevo, título y autor son obligatorios.",
        )

    year = None
    if year_raw:
        try:
            year = int(year_raw)
        except ValueError:
            return render_template(
                "new_review.html",
                current_user=current_user,
                books=all_books,
                selected_book=None,
                selected_book_id=None,
                mode="new",
                error="Año inválido.",
            )

    book_id = db.find_or_create_book(
        title=title,
        author=author,
        synopsis=(synopsis if synopsis else None),
        year=year,
        genre=(genre if genre else None),
        image_filename=image_filename,
    )

    db.add_review(current_user["id"], book_id, rating, review_text)
    return redirect(url_for("book_detail", book_id=book_id))


@app.route("/review/<int:review_id>/delete", methods=["POST"])
def delete_review(review_id):
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("login"))

    ok = db.delete_review(review_id=review_id, user_id=current_user["id"])
    if ok:
        return redirect(url_for("profile", msg="Review eliminada."))
    return redirect(url_for("profile", error="No se pudo eliminar (no existe o no es tuya)."))


@app.route("/about")
def about():
    current_user = get_current_user()
    return render_template("about.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
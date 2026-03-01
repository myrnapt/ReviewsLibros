-- 1) BORRAR Y CREAR BD (para evitar errores al re-ejecutar)
DROP DATABASE IF EXISTS projecte_myrna;
CREATE DATABASE projecte_myrna
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE projecte_myrna;

-- 2) BORRAR TABLAS SI EXISTEN (por seguridad adicional)
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;

-- ==========================================================
-- TABLA: users
-- ==========================================================
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==========================================================
-- TABLA: books
-- ==========================================================
CREATE TABLE books (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  author VARCHAR(200) NOT NULL,
  synopsis TEXT NULL,
  year INT NULL,
  genre VARCHAR(100) NULL,
  image_filename VARCHAR(255) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  -- Evitar duplicados de libro (mismo título + autor)
  UNIQUE KEY uq_books_title_author (title, author)

) ENGINE=InnoDB;

-- ==========================================================
-- TABLA: reviews
-- ==========================================================
CREATE TABLE reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,

  user_id INT NOT NULL,
  book_id INT NOT NULL,

  rating TINYINT NOT NULL,
  review_text TEXT NOT NULL,

  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  -- Restricción de rating 1..5 (MySQL 8+ / MariaDB lo acepta)
  CONSTRAINT chk_reviews_rating CHECK (rating BETWEEN 1 AND 5),

  -- Claves foráneas
  CONSTRAINT fk_reviews_user
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  CONSTRAINT fk_reviews_book
    FOREIGN KEY (book_id) REFERENCES books(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  -- Índices para consultas típicas
  KEY idx_reviews_user (user_id),
  KEY idx_reviews_book (book_id),
  KEY idx_reviews_created (created_at)
) ENGINE=InnoDB;

-- 1) Usuarios (admin + 10)
INSERT INTO users (username, password) VALUES
('admin','123456'),
('luna','123456'),
('nico','123456'),
('vera','123456'),
('eric','123456'),
('iris','123456'),
('bruno','123456'),
('noa','123456'),
('alex','123456'),
('sara','123456'),
('marc','123456');

-- ============================
-- LIBROS (10)
-- ============================

INSERT INTO books (title, author, synopsis, year, genre) VALUES
('1984','George Orwell','Distopía sobre vigilancia masiva, manipulación del lenguaje y control social absoluto.',1949,'Distopía'),
('Cien años de soledad','Gabriel García Márquez','Saga familiar ambientada en Macondo donde el tiempo y la memoria se mezclan.',1967,'Realismo mágico'),
('El señor de los anillos','J. R. R. Tolkien','Viaje épico para destruir un anillo que concentra el poder absoluto.',1954,'Fantasía'),
('Un mundo feliz','Aldous Huxley','Sociedad futurista donde la estabilidad se mantiene mediante el placer y el consumo.',1932,'Distopía'),
('La chica del tren','Paula Hawkins','Thriller psicológico sobre memoria, obsesión y desapariciones.',2015,'Thriller'),
('El nombre de la rosa','Umberto Eco','Misterio medieval ambientado en una abadía con asesinatos en serie.',1980,'Misterio'),
('Harry Potter y la piedra filosofal','J. K. Rowling','Inicio de una saga mágica sobre amistad, identidad y descubrimiento.',1997,'Fantasía'),
('El hobbit','J. R. R. Tolkien','Aventura fantástica sobre un viaje inesperado lleno de criaturas y peligros.',1937,'Fantasía'),
('El cuento de la criada','Margaret Atwood','Distopía sobre control del cuerpo femenino en una teocracia totalitaria.',1985,'Distopía'),
('El gran Gatsby','F. Scott Fitzgerald','Retrato de ambición, lujo y decadencia en los años veinte estadounidenses.',1925,'Clásico');

-- ============================
-- REVIEWS
-- ============================

-- 1984 (6 reviews)
INSERT INTO reviews (user_id, book_id, rating, review_text) VALUES
((SELECT id FROM users WHERE username='luna'), (SELECT id FROM books WHERE title='1984'), 5,
'Una novela brutalmente vigente. La sensación de vigilancia constante y manipulación del lenguaje me dejó inquieta. No es solo una historia, es una advertencia.'),
((SELECT id FROM users WHERE username='nico'), (SELECT id FROM books WHERE title='1984'), 4,
'Muy potente en ideas. Algunas partes son densas, pero el mensaje es clarísimo y muy actual.'),
((SELECT id FROM users WHERE username='vera'), (SELECT id FROM books WHERE title='1984'), 5,
'El desarrollo del mundo es impresionante. Cada capítulo añade tensión y el final es devastador.'),
((SELECT id FROM users WHERE username='eric'), (SELECT id FROM books WHERE title='1984'), 3,
'Me gustó la idea pero me costó el ritmo en algunos momentos.'),
((SELECT id FROM users WHERE username='iris'), (SELECT id FROM books WHERE title='1984'), 5,
'Impactante y necesario. De esos libros que todo el mundo debería leer al menos una vez.'),
((SELECT id FROM users WHERE username='bruno'), (SELECT id FROM books WHERE title='1984'), 4,
'Reflexión profunda sobre el poder y el control.');

-- Cien años de soledad (5 reviews)
INSERT INTO reviews (user_id, book_id, rating, review_text) VALUES
((SELECT id FROM users WHERE username='noa'), (SELECT id FROM books WHERE title='Cien años de soledad'), 5,
'Un libro que exige concentración pero que recompensa con una riqueza narrativa increíble. La construcción del universo de Macondo es fascinante y absorbente.'),
((SELECT id FROM users WHERE username='alex'), (SELECT id FROM books WHERE title='Cien años de soledad'), 4,
'Me gustó mucho aunque a veces cuesta seguir la genealogía.'),
((SELECT id FROM users WHERE username='sara'), (SELECT id FROM books WHERE title='Cien años de soledad'), 5,
'La mezcla de realidad y fantasía está perfectamente integrada. Es una obra monumental.'),
((SELECT id FROM users WHERE username='marc'), (SELECT id FROM books WHERE title='Cien años de soledad'), 4,
'Muy bien escrita, pero requiere paciencia.'),
((SELECT id FROM users WHERE username='luna'), (SELECT id FROM books WHERE title='Cien años de soledad'), 5,
'Emocional, poética y profunda.');

-- El señor de los anillos (8 reviews)
INSERT INTO reviews (user_id, book_id, rating, review_text) VALUES
((SELECT id FROM users WHERE username='nico'), (SELECT id FROM books WHERE title='El señor de los anillos'), 5,
'Épico en todos los sentidos. La construcción del mundo, los idiomas, la historia… es impresionante.'),
((SELECT id FROM users WHERE username='vera'), (SELECT id FROM books WHERE title='El señor de los anillos'), 4,
'Algunas partes descriptivas son largas, pero el viaje merece la pena.'),
((SELECT id FROM users WHERE username='eric'), (SELECT id FROM books WHERE title='El señor de los anillos'), 5,
'Una aventura inolvidable. Los personajes evolucionan de manera muy coherente.'),
((SELECT id FROM users WHERE username='iris'), (SELECT id FROM books WHERE title='El señor de los anillos'), 5,
'Lo he releído varias veces y siempre descubro algo nuevo.'),
((SELECT id FROM users WHERE username='bruno'), (SELECT id FROM books WHERE title='El señor de los anillos'), 4,
'Clásico absoluto de la fantasía.'),
((SELECT id FROM users WHERE username='noa'), (SELECT id FROM books WHERE title='El señor de los anillos'), 5,
'Te sumerge por completo en la Tierra Media.'),
((SELECT id FROM users WHERE username='alex'), (SELECT id FROM books WHERE title='El señor de los anillos'), 4,
'Gran historia de amistad y sacrificio.'),
((SELECT id FROM users WHERE username='sara'), (SELECT id FROM books WHERE title='El señor de los anillos'), 5,
'Una de las mejores sagas jamás escritas.');

-- El nombre de la rosa (4 reviews)
INSERT INTO reviews (user_id, book_id, rating, review_text) VALUES
((SELECT id FROM users WHERE username='marc'), (SELECT id FROM books WHERE title='El nombre de la rosa'), 5,
'Misterio histórico muy bien documentado. Me encantó la ambientación medieval y el enfoque filosófico.'),
((SELECT id FROM users WHERE username='luna'), (SELECT id FROM books WHERE title='El nombre de la rosa'), 4,
'Interesante mezcla de novela histórica y thriller.'),
((SELECT id FROM users WHERE username='nico'), (SELECT id FROM books WHERE title='El nombre de la rosa'), 4,
'Al principio es denso, pero luego engancha mucho.'),
((SELECT id FROM users WHERE username='vera'), (SELECT id FROM books WHERE title='El nombre de la rosa'), 5,
'Brillante combinación de intriga y reflexión.');

-- La chica del tren (3 reviews)
INSERT INTO reviews (user_id, book_id, rating, review_text) VALUES
((SELECT id FROM users WHERE username='eric'), (SELECT id FROM books WHERE title='La chica del tren'), 4,
'Thriller psicológico con giros interesantes. Me mantuvo en tensión hasta el final.'),
((SELECT id FROM users WHERE username='iris'), (SELECT id FROM books WHERE title='La chica del tren'), 3,
'Entretenido, aunque predecible en algunos puntos.'),
((SELECT id FROM users WHERE username='bruno'), (SELECT id FROM books WHERE title='La chica del tren'), 4,
'Buena construcción del suspense.');

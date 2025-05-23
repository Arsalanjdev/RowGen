![Python](https://img.shields.io/badge/python-3.12%20-blue)
![Last Commit](https://img.shields.io/github/last-commit/Arsalanjdev/RowGen)
![Issues](https://img.shields.io/github/issues/Arsalanjdev/RowGen)
![Repo Size](https://img.shields.io/github/repo-size/Arsalanjdev/RowGen)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen)](https://github.com/Arsalanjdev/RowGen/pulls)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

# RowGen: AI-Powered Fake Data Generator for SQL Databases

RowGen is a command-line tool that generates synthetic data and inserts it into your database. It uses AI to create
realistic fake data based on your database schema.

## Features

- **AI-Powered Fake Data**: Uses HuggingFace’s NLP models to generate realistic text, numbers, and structured data.
- **SQL-Compatible**: directly executes `INSERT` statements or export them into .sql files for easy database import.
- **Customizable Schemas**: Define table structures and let RowGen fill in the rest.
- **Poetry-Managed**: Clean dependency management and virtual environments.

---

## Use Case

Suppose you have a database such as the following:

#### `book_author`

| Column    | Type         | Constraints |
|-----------|--------------|-------------|
| author_id | SERIAL       | PRIMARY KEY |
| name      | VARCHAR(100) | NOT NULL    |
| email     | VARCHAR(100) | UNIQUE      |

#### `bookstore`

| Column   | Type         | Constraints |
|----------|--------------|-------------|
| store_id | SERIAL       | PRIMARY KEY |
| name     | VARCHAR(100) | NOT NULL    |
| location | VARCHAR(255) | NOT NULL    |

#### `book`

| Column           | Type           | Constraints        |
|------------------|----------------|--------------------|
| book_id          | SERIAL         | PRIMARY KEY        |
| title            | VARCHAR(200)   | NOT NULL           |
| publication_date | DATE           |                    |
| price            | NUMERIC(10, 2) | CHECK (price >= 0) |
| author_id        | INTEGER        

### Sample Generated Data

RowGen generates realistic sample data for this database, respecting foreign key relations and constraints:

| author\_id | name            | email                                                             |
|------------|-----------------|-------------------------------------------------------------------|
| 1          | Margaret Atwood | [margaret.atwood@example.com](mailto:margaret.atwood@example.com) |
| 2          | Haruki Murakami | [haruki.murakami@example.com](mailto:haruki.murakami@example.com) |
| 3          | J.K. Rowling    | [jk.rowling@example.com](mailto:jk.rowling@example.com)           |
| 4          | George Orwell   | [george.orwell@example.com](mailto:george.orwell@example.com)     |
| 5          | Agatha Christie | [agatha.christie@example.com](mailto:agatha.christie@example.com) |

| store\_id | name            | location                      |
|-----------|-----------------|-------------------------------|
| 1         | Book Haven      | 123 Main St, New York, NY     |
| 2         | Literary Corner | 456 Elm St, San Francisco, CA |
| 3         | Page Turner     | 789 Oak St, Chicago, IL       |
| 4         | Novel Nook      | 101 Pine St, Seattle, WA      |
| 5         | The Bookworm    | 202 Maple St, Boston, MA      |

| book\_id | title                                    | publication\_date | price | author\_id | store\_id |
|----------|------------------------------------------|-------------------|-------|------------|-----------|
| 1        | The Handmaid's Tale                      | 1985-08-01        | 12.99 | 1          | 1         |
| 2        | Norwegian Wood                           | 1987-09-04        | 14.5  | 2          | 2         |
| 3        | Harry Potter and the Philosopher's Stone | 1997-06-26        | 10.99 | 3          | 3         |
| 4        | 1984                                     | 1949-06-08        | 9.99  | 4          | 4         |
| 5        | Murder on the Orient Express             | 1934-01-01        | 11.25 | 5          | 5         |
| 6        | The Testaments                           | 2019-09-10        | 15.99 | 1          | 1         |
| 7        | Kafka on the Shore                       | 2002-09-12        | 13.75 | 2          | 2         |
| 8        | Harry Potter and the Chamber of Secrets  | 1998-07-02        | 11.99 | 3          | 3         |
| 9        | Animal Farm                              | 1945-08-17        | 8.5   | 4          | 4         |
| 10       | And Then There Were None                 | 1939-11-06        | 10.99 | 5          | 5         |

Notes:

- Foreign keys (author_id, store_id) are linked correctly.
- Constraints such as NOT NULL and CHECK on price are respected.
- Email addresses are linked with mailto: for easy access.

## Installation

```bash
pip install rowgen
```

### Basic Usage

```bash
rowgen --user <username> --database <dbname> [options]
```

#### Using individual options

```bash
rowgen --db-type postgresql --host localhost --port 5432 --user myuser --database mydb
```

#### Using database URL

```bash
rowgen --db-url postgresql://user:password@localhost:5432/mydb
```

### Operation Modes

#### Generate SQL File (Default)

Creates an inserts.sql file with the generated statements:

```bash
rowgen --user myuser --database mydb --rows 50
```

#### Execute Directly Against Database

```bash 
rowgen --user myuser --database mydb --execute
```

#### Custom Output File

```bash
rowgen --user myuser --database mydb --output custom_inserts.sql
```

#### API Configuration

##### Provide API Key via Command Line

```bash
rowgen --user myuser --database mydb --apikey YOUR_HUGGINGFACE_API_KEY
```

##### Save API Key in Config

If no API key is provided, RowGen will prompt you to enter one and save it in ~/.config/rowgen/conf for future use.

## Examples

Generate 100 rows for a PostgreSQL database and save to file:

```bash
rowgen --db-type postgresql --host db.example.com --user admin --database production --rows 100 --output prod_data.sql
```

Generate and immediately insert 25 rows into a MySQL database:

```bash
rowgen --db-type mysql --host localhost --user root --database test --execute
```

Use SQLite with direct execution:

```bash
rowgen --db-type sqlite --database /path/to/database.db --execute
```

## Troubleshooting

-Connection Issues: Verify your database credentials and that the server is accessible

-API Key Problems: Check that your HuggingFace API key is valid and has sufficient permissions

-Permission Errors: Ensure you have write access to the output directory when saving to file

For more information, run:

```bash
rowgen --help
```

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)
- HuggingFace API key (sign up [here](https://huggingface.co/api-keys))


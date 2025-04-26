## Start Here

- Use `source ./venv/bin/activate` when opening a new terminal.
- On fresh repos, don't forget to install the local module with `pip install -e .`.

---

## 🛠️ Development Setup

### Running Tests

```bash
pip install pytest
pytest
pytest tests/test_name.py
```

---

### Running Tests with Coverage

```bash
pip install coverage
coverage run -m pytest tests
coverage report
coverage html
```

---

### Helpful Test Flags

```bash
-x    # Exit on first failure
-k    # Run tests that match a keyword expression
-v    # Verbose output
-s    # Print stdout during test runs
```

---

## 🎨 Code Formatting and Linting

This project uses [**Black**](https://github.com/psf/black) for code formatting  
and [**Ruff**](https://github.com/astral-sh/ruff) for linting and lightweight auto-fixing.

---

### 🔧 Install & Use Tools

```bash
pip install black ruff
```

Format code with Black:

```bash
black .
black --check .
```

Lint code with Ruff:

```bash
ruff check .
ruff check . --fix
ruff check . --select E701
```

## Naming Conventions
## 📜 Python Naming Conventions

| Thing             | Style                  | Example                          |
|:------------------|:------------------------|:---------------------------------|
| **Class names**    | PascalCase (CapWords)    | `class MyAwesomeClass:`          |
| **Function names** | snake_case               | `def do_something():`            |
| **Variable names** | snake_case               | `user_name = "ed"`               |
| **Constant names** | ALL_CAPS                 | `MAX_RETRIES = 5`                |
| **Module names**   | snake_case               | `import my_module`               |
| **Package names**  | snake_case (short)       | `import mypackage`               |
| **Exception classes** | PascalCase + end with `Error` | `class DataLoadError(Exception):` |

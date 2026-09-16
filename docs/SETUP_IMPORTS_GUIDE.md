# Project Setup & Import Guide: `abyss_glancer`

This guide explains how `pyproject.toml` handles package imports across different subdirectories, eliminating the need for `sys.path` hacks or relative import issues.

---

## 🚀 Quick Setup (Development / Editable Mode)

To make every script in any folder recognize the root package without path issues, run this command **once** at the root of the project (where `pyproject.toml` is located):

```bash
pip install -e .
```

### What `pip install -e .` does:
* **`-e` (Editable Mode):** Links your source code directly to your active Python environment (`site-packages`).
* **Instant Updates:** Any changes or additions to your code, subfolders, or classes are reflected immediately without re-installing.
* **Global Access:** Allows scripts anywhere in the project to use absolute imports prefixed with `abyss_glancer`.

---

## 📦 How to Import Across Modules

Once installed in editable mode, you can import shared modules/classes from **any file in any directory** using clean, absolute paths:

```python
# Example: Importing a helper or utility class from anywhere in the project
from abyss_glancer.utils.helpers import DataParser
from abyss_glancer.core.engine import ProcessEngine

parser = DataParser()
```

---

## 📂 Expected Directory Structure

Ensure your project files are organized inside the `abyss_glancer` directory with `__init__.py` files where appropriate:

```text
abyss_glancer_project/
├── pyproject.toml
├── abyss_glancer/           <-- Main package root
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── engine.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── fecthed_data/            <-- Excluded data directory
├── parsed_data/             <-- Excluded data directory
└── test_responses/          <-- Excluded test output directory
```

---

## ⚙️ How `pyproject.toml` Works

Here is a breakdown of why this configuration file is set up this way:

### 1. Build System Setup
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```
Tells standard Python build tools (`pip`, `build`) to use `setuptools` to build and register the package.

### 2. Package Identity
```toml
[project]
name = "abyss_glancer"
version = "0.1.0"
```
Defines `abyss_glancer` as the top-level package namespace for imports.

### 3. Automatic Package Discovery & Exclusions
```toml
[tool.setuptools.packages.find]
where = ["."]
exclude = ["fecthed_data**", "test_responses*", "parsed_data*"]
```
* **`where = ["."]`**: Tells `setuptools` to scan the root folder for valid Python packages.
* **`exclude = [...]`**: Prevents data, cache, and temporary test directories from being indexed or included as importable modules.

# Contributing to POS Minimarket

Terima kasih telah berkontribusi pada project POS Minimarket! Dokumen ini berisi panduan untuk kontribusi.

## 📋 Cara Berkontribusi

### 1. Fork & Clone Repository
```bash
# Fork di GitHub, lalu clone:
git clone https://github.com/YOUR_USERNAME/minimarket.git
cd minimarket
```

### 2. Setup Development Environment
```powershell
# Windows (PowerShell)
.\setup.bat

# Atau manual:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_db.py
```

### 3. Create Feature Branch
```bash
git checkout -b feature/nama-fitur
# atau
git checkout -b fix/nama-bug
```

### 4. Development Workflow

#### **Coding Guidelines**
- Follow PEP 8 style guide untuk Python
- Gunakan type hints untuk function parameters & return values
- Tulis docstrings untuk class & function
- Keep functions small & focused (single responsibility)

#### **File Organization**
```
src/
├── auth/          # Authentication module
├── pos/           # Point of Sale module
├── products/      # Product management
└── ...
```

Setiap modul harus punya:
- `service.py` — Business logic
- `ui.py` — GUI components
- `utils.py` — Helper functions (optional)

#### **Testing**
```bash
# Run tests sebelum commit
pytest tests/ -v

# Run specific test
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=src tests/
```

**Semua PR harus include tests!**

### 5. Commit Guidelines

#### **Commit Message Format**
```
[TYPE] Brief description (max 50 chars)

BREAKING CHANGE: (if applicable)
- Details of breaking change

Body: Detailed description (wrap at 72 chars)
- Bullet points for multiple changes
- Reference issues: #123

Closes: #issue-number
```

#### **Commit Types**
- `[FEAT]` — New feature
- `[FIX]` — Bug fix
- `[DOCS]` — Documentation update
- `[TEST]` — Test additions/changes
- `[REFACTOR]` — Code refactoring (no functional change)
- `[STYLE]` — Formatting, missing semicolons, etc.
- `[CHORE]` — Build/tooling changes
- `[PERF]` — Performance improvements

#### **Examples**
```bash
# Good commits
git commit -m "[FEAT] Add login authentication with bcrypt hashing"
git commit -m "[FIX] Resolve stock decrement race condition in POS"
git commit -m "[DOCS] Update README with Telegram bot setup instructions"

# Bad commits (avoid these)
git commit -m "fix bug"
git commit -m "update"
git commit -m "wip"
```

### 6. Push & Create Pull Request
```bash
git push origin feature/nama-fitur
```

Lalu buat Pull Request di GitHub dengan:
- **Title**: Sama seperti commit message utama
- **Description**: 
  - What: Apa yang diubah
  - Why: Kenapa perubahan ini diperlukan
  - How: Bagaimana implementasinya
  - Testing: Bagaimana cara test perubahan ini
  - Screenshots: (untuk UI changes)

---

## 🧪 Testing Requirements

### **Before Submitting PR**
- [ ] All existing tests pass
- [ ] New tests added for new features
- [ ] Code coverage tidak turun
- [ ] Manual testing completed
- [ ] Documentation updated (if needed)

### **Test Checklist**
```bash
# 1. Unit tests
pytest tests/test_auth.py -v
pytest tests/test_products.py -v

# 2. Integration tests
pytest tests/test_integration.py -v

# 3. Database tests
pytest tests/test_database.py -v

# 4. Manual testing
python main.py  # Test in GUI
```

---

## 📚 Code Style

### **Python Style Guide**
```python
# Good: Type hints, docstrings, clear naming
def calculate_total(subtotal_cents: int, tax_rate: float, discount_cents: int = 0) -> int:
    """
    Calculate total amount with tax and discount.
    
    Args:
        subtotal_cents: Subtotal amount in cents
        tax_rate: Tax rate as percentage (e.g., 10.0 for 10%)
        discount_cents: Discount amount in cents (default: 0)
    
    Returns:
        Total amount in cents
    """
    tax_cents = int(subtotal_cents * tax_rate / 100)
    return subtotal_cents + tax_cents - discount_cents


# Bad: No type hints, unclear naming, no docstring
def calc(a, b, c=0):
    x = int(a * b / 100)
    return a + x - c
```

### **Import Order**
```python
# Standard library
import sys
from pathlib import Path
from datetime import datetime

# Third-party
from PySide6.QtWidgets import QWidget
from sqlalchemy import Column, Integer

# Local
import config
from src.db_manager import get_session
from src.models import User
```

### **Naming Conventions**
- **Classes**: `PascalCase` (e.g., `AuthService`, `ProductFormDialog`)
- **Functions**: `snake_case` (e.g., `calculate_total`, `get_user_by_id`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TAX_RATE`, `MAX_ATTEMPTS`)
- **Private**: prefix `_` (e.g., `_internal_helper`)

---

## 🔀 Branching Strategy

### **Branch Types**
- `main` — Production-ready code (protected)
- `develop` — Development branch (default target for PRs)
- `feature/*` — New features
- `fix/*` — Bug fixes
- `refactor/*` — Code refactoring
- `docs/*` — Documentation updates

### **Workflow**
```
main (v0.1.0)
  ↓
develop
  ├── feature/auth-module
  ├── feature/pos-transaction
  └── fix/stock-decrement-bug
```

**Merge flow**: `feature/*` → `develop` → `main` (via release)

---

## 🐛 Reporting Bugs

### **Bug Report Template**
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows 10/11
- Python: 3.10
- PySide6: 6.6.0

## Screenshots
(if applicable)

## Additional Context
Any other relevant information
```

---

## 💡 Feature Requests

### **Feature Request Template**
```markdown
## Feature Description
Clear description of the feature

## Problem It Solves
What problem does this solve?

## Proposed Solution
How should it work?

## Alternatives Considered
Other solutions you've thought about

## Additional Context
Mockups, references, etc.
```

---

## 📖 Documentation

### **When to Update Docs**
- Adding new features → Update README & relevant .md files
- Changing configuration → Update config.py comments & QUICKSTART.md
- API changes → Update DEVELOPMENT.md
- New modules → Update PROJECT_STRUCTURE.md

### **Documentation Files**
- `README.md` — User-facing documentation
- `QUICKSTART.md` — Quick setup guide
- `DEVELOPMENT.md` — Developer guide
- `MVP_CHECKLIST.md` — Implementation checklist
- `PROJECT_STRUCTURE.md` — Project overview
- `CHANGELOG.md` — Version history

---

## ✅ Pull Request Checklist

Before submitting PR, pastikan:

- [ ] Code follows style guidelines (PEP 8)
- [ ] Tests added/updated dan pass
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow convention
- [ ] No merge conflicts with target branch
- [ ] PR description is clear & complete
- [ ] Linked related issues (#123)
- [ ] Screenshots included (for UI changes)

---

## 🚀 Release Process

### **Version Numbering** (Semantic Versioning)
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.x.0): New features (backward compatible)
- **PATCH** (0.0.x): Bug fixes

### **Release Checklist**
1. Update `CHANGELOG.md`
2. Update version in `config.py`
3. Run full test suite
4. Merge to `main` branch
5. Create git tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
6. Push tag: `git push origin v0.2.0`
7. Create GitHub release with notes

---

## 🤝 Code Review Guidelines

### **As a Reviewer**
- Be constructive & respectful
- Explain *why* changes are needed
- Suggest alternatives when rejecting
- Approve if minor changes can be done in follow-up

### **Review Checklist**
- [ ] Code logic is correct
- [ ] Tests are adequate
- [ ] No security issues
- [ ] Performance is acceptable
- [ ] Documentation is clear
- [ ] UI/UX is user-friendly (for UI changes)

---

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security**: Email privately (don't open public issue)
- **General**: Check `DEVELOPMENT.md` first

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing!** 🎉

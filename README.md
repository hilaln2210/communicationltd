# Communication Ltd

אפליקציית Django לחברת תקשורת — ניהול משתמשים, התחברות וממשק אדמין.

## תכונות
- ניהול משתמשים
- התחברות/הרשמה
- ממשק אדמין Django
- SQLite (ברירת מחדל)

## טכנולוגיות
- **Python** · **Django**

## הרצה
```bash
pip install django  # או venv
python manage.py migrate
python manage.py runserver
# פתחי http://localhost:8000
```

## מבנה
```
communication_ltd/    # settings, urls
users/                # אפליקציית משתמשים (models, views, forms)
config.py
manage.py
```

## הערה
- `db.sqlite3` — לא ב-git (.gitignore)
- הרצי `migrate` לפני הפעלה ראשונה

© Hila · Django

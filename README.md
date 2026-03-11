# Communication LTD

אפליקציית Django לחברת תקשורת — ניהול לקוחות, מנויים, חבילות, ואימות משתמשים.

---

## צילומי מסך

### דף בית — לא מחובר
![Home logged out](screenshots/home_logged_out.png)

### דף בית — מחובר (לוח בקרה עם סטטיסטיקות)
![Home logged in](screenshots/home_logged_in.png)

### ניהול לקוחות — טבלה עם מנויים ופעולות
![System screen](screenshots/system_screen.png)

### חבילות מנוי
![Packages](screenshots/packages.png)

### התחברות
![Login](screenshots/login.png)

### הרשמה
![Register](screenshots/register.png)

### שכחתי סיסמה
![Forgot Password](screenshots/forgot_password.png)

---

## תכונות

### ניהול לקוחות
- **הוספת לקוח** — שם, טלפון, אימייל (נשמר למודל)
- **מחיקת לקוח** — עם בדיקת בעלות (לא ניתן למחוק לקוח של משתמש אחר)
- **טבלת לקוחות** — Bootstrap table עם שם, טלפון, אימייל, מנוי פעיל, ופעולות

### חבילות ומנויים
- **3 חבילות מובנות** — בסיסי (₪50), מתקדם (₪100), פרמיום (₪150)
- **הרשמה לחבילה** — ניתן להרשים לקוח לחבילה ישירות מדף החבילות
- **מעקב מנויים** — תאריך התחלה ותפוגה, הצגת מנוי פעיל בטבלת הלקוחות

### אימות ואבטחה
- **התחברות / הרשמה / התנתקות**
- **שינוי סיסמה** — לוגין נדרש
- **איפוס סיסמה** — באמצעות טוקן בתפוגת שעה אחת (תוקן חלון תפוגה!)
- **ולידציה** — דרישות אבטחה לסיסמה (אורך, ספרות, אותיות, תו מיוחד)
- **CSRF protection** על כל הטפסים

### ממשק
- **Bootstrap 5** + **Bootstrap Icons** בכל הממשק
- **עברית RTL** מלא
- **לוח בקרה** — סטטיסטיקות (לקוחות, מנויים פעילים, חבילות)
- **Hero section** — לדף הבית לא-מחובר עם כפתורי כניסה/הרשמה
- **Footer** בכל הדפים

---

## תיקוני באגים שבוצעו

| בעיה | תיקון |
|------|-------|
| `email` בטופס לקוח לא נשמר למודל | הוסף שדה `email` ל-`Customer` + migration |
| טוקן איפוס סיסמה אף פעם לא פג תוקף | הוסף `token_created_at`, בדיקת שעה ב-`reset_password` |
| `Package` ו-`Subscription` קיימים בלי שימוש | נוספו views: `packages_view`, `subscribe_customer` |
| `system_screen` — רשימת `<ul>` בסיסית | שודרג לטבלת Bootstrap עם מנויים ופעולות |
| `home.html` — רק "ברוך הבא" | לוח בקרה עם סטטיסטיקות + hero section |
| `CustomerForm.save(user=...)` לא שימש לכלום | נותר `commit=False` + `customer.user = request.user` ב-view |

---

## מבנה הפרויקט

```
communication_ltd/    # הגדרות Django (settings, urls, wsgi)
users/
  ├── models.py       # User, Customer, Package, Subscription
  ├── views.py        # home, system_screen, customer_delete, packages_view, subscribe_customer, ...
  ├── forms.py        # CustomerForm (עם email), UserRegistrationForm, ...
  ├── urls.py         # כל נתיבי URL
  ├── migrations/     # כולל migration לנתוני חבילות ראשוניות
  └── templates/
      ├── base.html             # navbar עם Bootstrap Icons + footer
      ├── home.html             # לוח בקרה / hero section
      └── users/
          ├── system_screen.html    # טבלת לקוחות עם פעולות
          ├── packages.html         # כרטיסי חבילות
          ├── subscribe_confirm.html
          ├── login.html
          ├── register.html
          └── ...
manage.py
```

---

## נתיבי URL

| נתיב | תיאור | הרשאה |
|------|-------|-------|
| `/` | דף בית / לוח בקרה | פתוח |
| `/users/login/` | התחברות | פתוח |
| `/users/register/` | הרשמה | פתוח |
| `/users/logout/` | התנתקות | מחובר |
| `/users/change-password/` | שינוי סיסמה | מחובר |
| `/users/forgot-password/` | שכחתי סיסמה | פתוח |
| `/users/system/` | ניהול לקוחות | מחובר |
| `/users/system/delete/<pk>/` | מחיקת לקוח | מחובר + בעלות |
| `/users/packages/` | חבילות מנוי | מחובר |
| `/users/subscribe/<customer_pk>/<package_pk>/` | הרשמה לחבילה | מחובר + בעלות |
| `/admin/` | ממשק ניהול Django | Staff |

---

## הרצה

```bash
# 1. צור סביבה וירטואלית
python3 -m venv venv
source venv/bin/activate

# 2. התקן תלויות
pip install django

# 3. הגדר מסד נתונים (כולל נתוני חבילות ראשוניות)
python manage.py migrate

# 4. (אופציונלי) צור superuser
python manage.py createsuperuser

# 5. הפעל שרת
python manage.py runserver

# פתח http://localhost:8000
```

---

© Hila · Django Telecom Management Project

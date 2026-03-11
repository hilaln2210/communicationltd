from django.db import migrations


def create_initial_packages(apps, schema_editor):
    Package = apps.get_model('users', 'Package')
    packages = [
        {
            'name': 'בסיסי',
            'description': 'אינטרנט בסיסי עד 100 מגה לשנייה. מתאים לגלישה יומיומית, מיילים ורשתות חברתיות.',
            'price': '50.00',
        },
        {
            'name': 'מתקדם',
            'description': 'אינטרנט מהיר עד 500 מגה לשנייה + ערוצי טלוויזיה בסיסיים. מתאים למשפחות.',
            'price': '100.00',
        },
        {
            'name': 'פרמיום',
            'description': 'כל מה שיש: אינטרנט גיגה-ביט + כל ערוצי הטלוויזיה + קו סלולרי ללא הגבלה.',
            'price': '150.00',
        },
    ]
    for p in packages:
        Package.objects.get_or_create(name=p['name'], defaults={
            'description': p['description'],
            'price': p['price'],
        })


def remove_initial_packages(apps, schema_editor):
    Package = apps.get_model('users', 'Package')
    Package.objects.filter(name__in=['בסיסי', 'מתקדם', 'פרמיום']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customer_email_user_token_created_at'),
    ]

    operations = [
        migrations.RunPython(create_initial_packages, remove_initial_packages),
    ]

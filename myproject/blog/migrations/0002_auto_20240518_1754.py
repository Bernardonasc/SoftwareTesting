from django.db import migrations

def add_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    categories = [
        'Artificial Intelligence',
        'Machine Learning',
        'Data Science',
        'Web Development',
        'Mobile Development',
        'Cyber Security',
        'Cloud Computing',
        'DevOps',
        'Blockchain',
        'Other'
    ]
    for category in categories:
        Category.objects.create(name=category)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_categories),
    ]

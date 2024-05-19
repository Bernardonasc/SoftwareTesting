from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    categories = [
        'Blockchain', 'Artificial Intelligence', 'Cloud Computing', 'Data Science', 
        'Cyber Security', 'Mobile Development', 'Web Development', 'DevOps', 
        'Internet of Things', 'Game Development'
    ]
    for name in categories:
        Category.objects.create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]

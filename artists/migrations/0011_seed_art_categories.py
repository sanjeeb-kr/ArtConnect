from django.db import migrations


def update_art_categories(apps, schema_editor):
    ArtistType = apps.get_model('artists', 'ArtistType')
    Post = apps.get_model('artists', 'Post')
    ArtistProfile = apps.get_model('accounts', 'ArtistProfile')

    mapping = {
        'Poet': 'Poetry',
        'Singer': 'Music & Songs',
        'Musician': 'Music & Songs',
        'Painter': 'Painting & Fine Art',
        'Dancer': 'Dance & Performance',
        'Writer': 'Literature & Writing',
        'Photographer': 'Photography',
        'Actor': 'Film & Acting',
        'Designer': 'Design & Illustration',
        'Illustrator': 'Design & Illustration',
        'Other': 'Other Art',
    }

    for old_name, new_name in mapping.items():
        old_cat = ArtistType.objects.filter(name=old_name).first()
        if old_cat:
            new_cat, _ = ArtistType.objects.get_or_create(name=new_name)
            if old_cat.id != new_cat.id:
                Post.objects.filter(category=old_cat).update(category=new_cat)
                ArtistProfile.objects.filter(artist_type=old_cat).update(artist_type=new_cat)
                old_cat.delete()

    art_categories = [
        'Poetry',
        'Music & Songs',
        'Painting & Fine Art',
        'Dance & Performance',
        'Literature & Writing',
        'Photography',
        'Film & Acting',
        'Design & Illustration',
        'Digital Art',
        'Other Art'
    ]
    for cat in art_categories:
        ArtistType.objects.get_or_create(name=cat)


def reverse_update(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0010_auto_fix_all_cloudinary_media'),
    ]

    operations = [
        migrations.RunPython(update_art_categories, reverse_code=reverse_update),
    ]

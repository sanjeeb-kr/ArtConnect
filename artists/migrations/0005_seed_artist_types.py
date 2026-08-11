from django.db import migrations


def seed_artist_types(apps, schema_editor):
    ArtistType = apps.get_model('artists', 'ArtistType')
    types = [
        'Photographer',
        'Painter',
        'Musician',
        'Singer',
        'Dancer',
        'Poet',
        'Writer',
        'Actor',
        'Designer',
        'Illustrator',
        'Other'
    ]
    for type_name in types:
        ArtistType.objects.get_or_create(name=type_name)


def reverse_seed_artist_types(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0004_post_thumbnail_delete_service'),
    ]

    operations = [
        migrations.RunPython(seed_artist_types, reverse_code=reverse_seed_artist_types),
    ]

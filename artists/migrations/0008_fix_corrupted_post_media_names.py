from django.db import migrations


def clean_media_names(apps, schema_editor):
    Post = apps.get_model('artists', 'Post')
    real_extensions = ['.avif', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf', '.mp3', '.wav']
    for post in Post.objects.all():
        if post.media and post.media.name:
            name = post.media.name
            if name.lower().endswith('.mp4'):
                for ext in real_extensions:
                    if ext in name[:-4].lower():
                        post.media.name = name[:-4]
                        post.save(update_fields=['media'])
                        break


def reverse_clean(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0007_fix_existing_post_media_names'),
    ]

    operations = [
        migrations.RunPython(clean_media_names, reverse_code=reverse_clean),
    ]

from django.db import migrations


def fix_media_extensions(apps, schema_editor):
    Post = apps.get_model('artists', 'Post')
    known_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.webm', '.ogg', '.mov', '.avi', '.mp3', '.wav', '.pdf']
    for post in Post.objects.all():
        if post.media and post.media.name:
            media_name = post.media.name.lower()
            if not any(media_name.endswith(ext) for ext in known_extensions):
                # Append .mp4 extension to old video uploads saved without extension
                post.media.name = f"{post.media.name}.mp4"
                post.save(update_fields=['media'])


def reverse_fix(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0006_alter_post_media_alter_post_thumbnail'),
    ]

    operations = [
        migrations.RunPython(fix_media_extensions, reverse_code=reverse_fix),
    ]

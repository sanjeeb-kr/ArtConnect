from django.db import migrations


def fix_all_posts(apps, schema_editor):
    Post = apps.get_model('artists', 'Post')
    for post in Post.objects.all():
        if post.media and post.media.name:
            name = post.media.name
            # If name ends with .mp4 but contains an image extension before it
            for img_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif']:
                if img_ext in name.lower() and name.lower().endswith('.mp4'):
                    post.media.name = name[:-4]
                    post.save(update_fields=['media'])
                    break


def reverse_fix(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0008_fix_corrupted_post_media_names'),
    ]

    operations = [
        migrations.RunPython(fix_all_posts, reverse_code=reverse_fix),
    ]

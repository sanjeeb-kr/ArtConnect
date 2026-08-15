import urllib.request
from django.db import migrations


def fix_cloudinary_media(apps, schema_editor):
    Post = apps.get_model('artists', 'Post')
    for post in Post.objects.all():
        if post.media and post.media.name and post.media.name.endswith('.mp4'):
            clean_name = post.media.name[:-4]
            # Test if Cloudinary image URL returns 200 OK
            img_url = f"https://res.cloudinary.com/dboflizh/image/upload/v1/{clean_name.lstrip('/')}"
            try:
                req = urllib.request.Request(img_url, method='HEAD')
                resp = urllib.request.urlopen(req, timeout=5)
                if resp.status == 200:
                    # It's actually an image! Remove false .mp4 extension
                    post.media.name = clean_name
                    post.save(update_fields=['media'])
            except Exception:
                pass


def reverse_fix(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0009_fix_all_corrupted_media'),
    ]

    operations = [
        migrations.RunPython(fix_cloudinary_media, reverse_code=reverse_fix),
    ]

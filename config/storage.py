import os
from cloudinary_storage.storage import MediaCloudinaryStorage


class AutoCloudinaryStorage(MediaCloudinaryStorage):
    """
    Custom Cloudinary storage class that dynamically determines the Cloudinary
    resource_type ('image', 'video', or 'raw') based on the uploaded file's extension.
    This prevents 500 errors when uploading MP4 videos, MP3 audio, or PDF documents.
    """
    def _get_resource_type(self, name):
        ext = os.path.splitext(name)[1].lower()
        if ext in ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', '.mp3', '.wav', '.aac', '.flac', '.m4a']:
            return 'video'
        elif ext in ['.pdf', '.doc', '.docx', '.zip', '.txt']:
            return 'raw'
        return 'image'

import os
from django.core.files.uploadedfile import UploadedFile
from cloudinary_storage.storage import MediaCloudinaryStorage


class AutoCloudinaryStorage(MediaCloudinaryStorage):
    """
    Custom Cloudinary storage class that dynamically determines the Cloudinary
    resource_type ('image', 'video', or 'raw') based on the uploaded file's extension,
    and ensures the file extension is preserved in stored public_id so Cloudinary URLs
    generate with correct /video/upload/ or /raw/upload/ endpoints instead of 404 errors.
    """
    def _get_resource_type(self, name):
        ext = os.path.splitext(name)[1].lower()
        if ext in ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', '.mp3', '.wav', '.aac', '.flac', '.m4a']:
            return 'video'
        elif ext in ['.pdf', '.doc', '.docx', '.zip', '.txt']:
            return 'raw'
        return 'image'

    def _save(self, name, content):
        original_ext = os.path.splitext(name)[1].lower()
        normalised_name = self._normalise_name(name)
        prefixed_name = self._prepend_prefix(normalised_name)
        uploaded_file = UploadedFile(content, prefixed_name)
        response = self._upload(prefixed_name, uploaded_file)
        
        public_id = response.get('public_id', '')
        
        # If original extension exists and Cloudinary public_id stripped it, append extension
        if original_ext and not public_id.lower().endswith(original_ext):
            # Strip prefix if response['public_id'] already includes prefix
            prefix = self._get_prefix().lstrip('/')
            prefix = self._normalize_path(prefix)
            if prefix and public_id.startswith(prefix):
                public_id = public_id[len(prefix):]
            public_id = f"{public_id}{original_ext}"

        return public_id

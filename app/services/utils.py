"""
Utility functions
"""

import os
from django.core.files.storage import default_storage
from django.conf import settings


def handle_video_upload(video_file) -> str:
    """
    Handle video file upload and return the file path.

    :param video_file: The uploaded video file.
    :return: Path where the video is stored.
    """
    # Save the file using Django's default file storage system
    file_name = video_file.name
    file_path = default_storage.save(os.path.join("videos", file_name), video_file)

    # Return the path where the video is stored
    return os.path.join(settings.MEDIA_URL, file_path)

from django.core.exceptions import ValidationError
from urllib.parse import urlparse

def validate_youtube_url(value):
    parsed_url = urlparse(value)
    if (parsed_url.netloc != 'youtube.com' and parsed_url.netloc
            != 'www.youtube.com'):
        raise ValidationError(f"Invalid URL: {value}. Only "
                              f"YouTube links are allowed.")

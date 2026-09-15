import re
from django.core.exceptions import ValidationError


def validate_mobile_number(value):
    """
    Validates mobile numbers for registration and profile editing.
    Allows optional country code (+91, +1, etc.), spaces, or hyphens,
    and enforces 10 to 15 valid digits without repeating dummy sequences like 0000000000.
    """
    if not value or not value.strip():
        return
    
    cleaned = value.strip()
    # Strip spaces, hyphens, dots, and parentheses
    stripped_digits = re.sub(r'[\s\-\(\)\.]', '', cleaned)

    # Must contain only digits and optional leading '+'
    if not re.match(r'^\+?[0-9]{10,15}$', stripped_digits):
        raise ValidationError(
            "Please enter a valid 10 to 15 digit mobile number (e.g., +91 9876543210 or 9876543210)."
        )

    # Extract pure digits
    digits_only = re.sub(r'\D', '', stripped_digits)

    # Disallow repeating single-digit sequences (e.g., 0000000000, 1111111111)
    if len(set(digits_only)) == 1:
        raise ValidationError("Please enter a valid mobile number.")

import re
from django.core.exceptions import ValidationError

class ExternalLinkValidator:
    def __init__(self, allowed_domains=None):
        if allowed_domains is None:
            allowed_domains = ["youtube.com"]
        self.allowed_domains = allowed_domains

    def __call__(self, value):
        # Ensure the value is a string
        if not isinstance(value, str):
            raise ValidationError("Invalid URL format.")

        # Extract domain from the URL
        domain_match = re.search(r"https?://(?:www\.)?([^/]+)", value)
        if not domain_match:
            raise ValidationError("Invalid URL format.")

        domain = domain_match.group(1)

        # Check if the domain is allowed
        if not any(allowed_domain in domain for allowed_domain in self.allowed_domains):
            raise ValidationError(
                f"Links to {domain} are not allowed. Only links to {', '.join(self.allowed_domains)} are permitted."
            )

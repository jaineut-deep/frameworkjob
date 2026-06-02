import re
from rest_framework.serializers import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        regular = re.compile(r'https://www.youtube.com')
        tmp_val = dict(value).get(self.field)
        if not bool(re.search(regular, tmp_val, flags=re.IGNORECASE)):
            raise ValidationError("Link is not acceptable")

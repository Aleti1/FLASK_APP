#!/usr/bin/env python3

class Length(object):
    def __init__(self, min = -1, max = -1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = """Field must be between '{}' and '{}' characters long.""".format( min, max )
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            raise ValidationError(self.message)

length = Length
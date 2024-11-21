from datetime import timedelta
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def date_add(value, days):
    """Add days to a date."""
    try:
        # Sanani datetime ob'ektiga aylantirish
        value = datetime.strptime(value, "%d.%m.%Y")
        # Sanaga 10 kun qo'shish
        new_date = value + timedelta(days=int(days))
        return new_date.strftime("%d.%m.%Y")  # Yangi sanani string formatida qaytarish
    except (ValueError, TypeError):
        return value

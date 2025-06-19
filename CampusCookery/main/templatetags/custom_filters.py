from django import template

register = template.Library()

@register.filter(name='stars')
def stars(value):
    # Returns rating as stars
    if value is None:
        return '☆' * 5

    rating = round(value)

    print(rating)
    return '☆' * (5 - rating) + '★' * rating

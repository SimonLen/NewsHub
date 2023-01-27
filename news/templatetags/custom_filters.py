from django import template


register = template.Library()


@register.filter()
def censor(value, word):
    if isinstance(value, str):
        censored = word[0].lower() + '*' * (len(word) - 1)
        value = value.replace(word.lower(), censored)
        censored = censored.capitalize()
        value = value.replace(word.capitalize(), censored)
        return value
    else:
        raise TypeError('expected str')

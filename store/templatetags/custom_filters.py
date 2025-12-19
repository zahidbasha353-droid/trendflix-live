from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Value-vaiyum arg-aiyum multiply pannum"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_discount(cost, selling):
    """Discount percentage calculate pannum"""
    try:
        cost = float(cost)
        selling = float(selling)
        if cost > 0:
            discount = ((cost - selling) / cost) * 100
            return int(discount)
    except (ValueError, TypeError):
        pass
    return 0
from django import template

register = template.Library()

@register.filter
def currency(value, arg=None):
    """Price-ah correct-aana decimal format-la (e.g., 1,250.00) maathum"""
    try:
        return "{:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return value

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_discount(cost, selling):
    try:
        cost = float(cost)
        selling = float(selling)
        if cost > 0:
            discount = ((cost - selling) / cost) * 100
            return int(discount)
    except (ValueError, TypeError):
        pass
    return 0
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

# EXCHANGE RATES (Neenga future la update pannikalam)
RATES = {
    'INR': 1,
    'USD': 0.012,  # 1 INR = 0.012 USD (approx)
    'EUR': 0.011   # 1 INR = 0.011 EUR (approx)
}

SYMBOLS = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€'
}

@register.filter
def currency(amount, request):
    # Get selected currency from session (Default INR)
    code = request.session.get('currency', 'INR')
    
    try:
        amount = float(amount)
        converted_amount = amount * RATES[code]
        symbol = SYMBOLS[code]
        
        # Formatting
        if code == 'INR':
            return f"{symbol}{intcomma(int(converted_amount))}"
        else:
            return f"{symbol}{converted_amount:.2f}"
    except (ValueError, TypeError):
        return f"₹{amount}"
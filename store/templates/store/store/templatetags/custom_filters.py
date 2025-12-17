from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

# EXCHANGE RATES (Approximate - You can update this later)
RATES = {
    'INR': 1,
    'USD': 0.012,   # US Dollar
    'EUR': 0.011,   # Euro (Germany, France, etc.)
    'GBP': 0.0095,  # British Pound (UK)
    'AED': 0.044,   # Dubai/UAE Dirham
    'SAR': 0.045,   # Saudi Riyal
    'CAD': 0.016,   # Canadian Dollar
    'AUD': 0.018,   # Australian Dollar
}

SYMBOLS = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'AED': 'AED ',
    'SAR': 'SAR ',
    'CAD': 'C$',
    'AUD': 'A$',
}

@register.filter
def currency(amount, request):
    # Default is INR if not set
    code = request.session.get('currency', 'INR')
    
    try:
        amount = float(amount)
        converted_amount = amount * RATES.get(code, 1)
        symbol = SYMBOLS.get(code, '₹')
        
        # Formatting Logic
        if code == 'INR':
            return f"{symbol}{intcomma(int(converted_amount))}"
        else:
            return f"{symbol}{converted_amount:.2f}"
    except (ValueError, TypeError):
        return f"₹{amount}"
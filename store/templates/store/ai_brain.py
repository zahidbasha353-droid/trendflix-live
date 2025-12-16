from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import Product, OrderItem

# 🧠 THE GOD MODE ALGORITHM
def run_ai_optimization():
    print("🤖 AI BRAIN: Waking up...")
    
    # Time window: Look at last 7 days
    last_week = timezone.now() - timedelta(days=7)
    products = Product.objects.all()
    
    report = []

    for product in products:
        # 1. GATHER DATA
        sales_data = OrderItem.objects.filter(product=product, order__created_at__gte=last_week).aggregate(total_sold=Sum('quantity'))
        total_sold = sales_data['total_sold'] or 0
        views = product.view_count
        
        # 2. TRENDING LOGIC (If sold > 5 units this week)
        if total_sold >= 5:
            product.is_trending = True
            tag = "🔥 Trending"
        else:
            product.is_trending = False
            tag = "💤 Normal"

        # 3. BESTSELLER PREDICTION (Conversion Rate)
        conversion_rate = (total_sold / views) * 100 if views > 0 else 0
        if conversion_rate > 5 and total_sold > 10:
            product.is_bestseller = True
            tag += " | 🏆 Bestseller"
        
        # 4. AUTO-PRICING (The Money Maker) 💸
        old_price = float(product.selling_price)
        new_price = old_price
        
        if product.ai_pricing_active:
            # High Demand -> Price UP
            if total_sold > 10:
                new_price = old_price * 1.05
                action = "📈 Price UP (High Demand)"
            # No Sales, High Views -> Price DOWN
            elif total_sold == 0 and views > 50:
                new_price = old_price * 0.95
                action = "📉 Price DOWN (Clearance)"
            else:
                action = "No Change"
            
            product.selling_price = round(new_price)
        else:
            action = "AI Pricing Disabled"
        
        product.save()
        report.append(f"{product.name}: Sold {total_sold} | {tag} | {action}")

    print("🤖 AI BRAIN: Optimization Complete!")
    return report
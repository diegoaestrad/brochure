#!/usr/bin/env python3
import os

# All 29 businesses with their data
BUSINESSES = {
    "auto-repair": {
        "emoji": "🔧",
        "title": "Expert Auto Care",
        "tagline": "Professional Auto Repair & Service",
        "hero_subtitle": "Your vehicle deserves expert care and maintenance.",
        "hero_copy": "From routine maintenance to major repairs, Expert Auto Care provides reliable, affordable automotive services with certified technicians and quality parts.",
        "products": [
            ("Oil Changes & Filters", "Regular maintenance keeps your engine running smoothly.", "https://images.unsplash.com/photo-1552820728-8ac41f1ce891?auto=format&fit=crop&w=900&q=80"),
            ("Brake Service", "Safe stopping power with brake inspections and repairs.", "https://images.unsplash.com/photo-1578039158222-a1c33b57331f?auto=format&fit=crop&w=900&q=80"),
            ("Tire Services", "Expert tire installation, rotation, and alignment.", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?auto=format&fit=crop&w=900&q=80"),
            ("Engine Diagnostics", "Advanced computer diagnostics for engine problems.", "https://images.unsplash.com/photo-1517048676632-6297afc4e27f?auto=format&fit=crop&w=900&q=80"),
            ("Transmission Repair", "Complete transmission service and repairs.", "https://images.unsplash.com/photo-1533473359331-35a97e5f9c93?auto=format&fit=crop&w=900&q=80"),
            ("AC & Heating", "Climate control system maintenance and repair.", "https://images.unsplash.com/photo-1550355291-bbee04a92027?auto=format&fit=crop&w=900&q=80"),
        ],
        "services": [
            ("Routine Maintenance", ["Oil & filter changes", "Fluid top-ups", "Belt and hose inspection"]),
            ("Braking Systems", ["Brake pad replacement", "Rotor resurfacing", "Brake fluid service"]),
            ("Engine Service", ["Engine overhaul", "Head gasket repair", "Timing belt service"]),
            ("Electrical", ["Battery service", "Alternator repair", "Starter replacement"]),
            ("Suspension", ["Alignment services", "Shock absorber replacement", "Strut service"]),
            ("Exhaust", ["Muffler replacement", "Catalytic converter service", "Exhaust leak repair"]),
        ],
        "location": "789 Mechanic Drive, Austin, TX 78704",
        "phone": "+15125551234",
        "hero_image": "https://images.unsplash.com/photo-1552820728-8ac41f1ce891?auto=format&fit=crop&w=1920&q=80",
        "primary_dark": "#1a1a1a",
        "primary_mid": "#333333",
        "primary_light": "#555555",
        "gold": "#d4a574",
        "gold_soft": "#e8c4a0",
    },
    "barbershop": {
        "emoji": "💈",
        "title": "Classic Cuts Barber Shop",
        "tagline": "Traditional Barbering & Grooming",
        "hero_subtitle": "Quality haircuts and grooming services since 1995.",
        "hero_copy": "Classic Cuts offers expert barbering, traditional wet shaves, and premium grooming services in a welcoming, no-nonsense atmosphere.",
        "products": [
            ("Classic Haircut", "Traditional cut with precision and attention to detail.", "https://images.unsplash.com/photo-1585747860715-cd4628902d4a?auto=format&fit=crop&w=900&q=80"),
            ("Hot Shave", "Luxurious traditional wet shave with quality razors.", "https://images.unsplash.com/photo-1599308669872-06f22f18a68e?auto=format&fit=crop&w=900&q=80"),
            ("Fade & Lineup", "Modern fade cuts with crisp, clean lines.", "https://images.unsplash.com/photo-1552820728-8ac41f1ce891?auto=format&fit=crop&w=900&q=80"),
            ("Beard Trim", "Expert beard shaping and conditioning.", "https://images.unsplash.com/photo-1577412647953-2c28e4402bab?auto=format&fit=crop&w=900&q=80"),
            ("Kids Cuts", "Friendly, patient cuts for children of all ages.", "https://images.unsplash.com/photo-1602525206329-e9e8b8b00a65?auto=format&fit=crop&w=900&q=80"),
            ("Grooming Package", "Complete package with cut, shave, and beard care.", "https://images.unsplash.com/photo-1620331383944-8e9723143a6f?auto=format&fit=crop&w=900&q=80"),
        ],
        "services": [
            ("Haircuts", ["Classic cuts", "Fades & tapers", "Design cuts"]),
            ("Shaving", ["Hot towel shaves", "Straight razor shaves", "Premium shave products"]),
            ("Beard Services", ["Beard trim & shape", "Beard oil treatments", "Beard conditioning"]),
            ("Specialty", ["Hair coloring", "Highlights", "Eyebrow shaping"]),
            ("Kids", ["Kids haircuts", "First haircut special", "Friendly atmosphere"]),
            ("Packages", ["Walk-ins welcome", "Loyalty cards", "Gift certificates"]),
        ],
        "location": "542 Main Street, Nashville, TN 37201",
        "phone": "+16155551234",
        "hero_image": "https://images.unsplash.com/photo-1585747860715-cd4628902d4a?auto=format&fit=crop&w=1920&q=80",
        "primary_dark": "#4a1f1f",
        "primary_mid": "#6b3030",
        "primary_light": "#8b4545",
        "gold": "#c4956f",
        "gold_soft": "#d9b08f",
    },
    "cafe": {
        "emoji": "☕",
        "title": "Brew Haven Cafe",
        "tagline": "Specialty Coffee & Brunch",
        "hero_subtitle": "Your neighborhood gathering place for great coffee.",
        "hero_copy": "Brew Haven serves carefully sourced, freshly roasted coffee paired with artisan pastries, healthy breakfast, and lunch options in a warm, inviting environment.",
        "products": [
            ("Espresso Drinks", "Classic lattes, cappuccinos, and macchiatos from premium beans.", "https://images.unsplash.com/photo-1521017874487-f0d2b09ba2d6?auto=format&fit=crop&w=900&q=80"),
            ("Single Origin Coffee", "Carefully selected beans from around the world.", "https://images.unsplash.com/photo-1559056199-641a0ac8b8d5?auto=format&fit=crop&w=900&q=80"),
            ("Pastries & Desserts", "Fresh-baked croissants, muffins, and cakes daily.", "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80"),
            ("Breakfast", "Omelets, avocado toast, and breakfast sandwiches.", "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=900&q=80"),
            ("Lunch Menu", "Salads, sandwiches, and seasonal soups.", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=900&q=80"),
            ("Cold Brew", "Smooth, refreshing cold brew and iced drinks.", "https://images.unsplash.com/photo-1517668808822-9ebb02ae2a0e?auto=format&fit=crop&w=900&q=80"),
        ],
        "services": [
            ("Beverages", ["Espresso drinks", "Specialty lattes", "Herbal teas"]),
            ("Breakfast", ["Omelets", "Breakfast sandwiches", "Yogurt bowls"]),
            ("Lunch", ["Fresh salads", "Gourmet sandwiches", "Seasonal soups"]),
            ("Baked Goods", ["Fresh pastries", "Artisan bread", "Gluten-free options"]),
            ("Events", ["Private events", "Coffee tastings", "Catering"]),
            ("Retail", ["Whole bean coffee", "Brewing equipment", "Coffee accessories"]),
        ],
        "location": "321 Harbor Street, Seattle, WA 98101",
        "phone": "+12065551234",
        "hero_image": "https://images.unsplash.com/photo-1505778276668-fc5ee03efb8f?auto=format&fit=crop&w=1920&q=80",
        "primary_dark": "#3d2817",
        "primary_mid": "#5a3f2a",
        "primary_light": "#7a5a45",
        "gold": "#d4a574",
        "gold_soft": "#e8c4a0",
    },
    "car-detailing": {
        "emoji": "🚗",
        "title": "Shine Detail Studio",
        "tagline": "Professional Car Detailing & Protection",
        "hero_subtitle": "Your car deserves to look its best.",
        "hero_copy": "Shine Detail Studio specializes in professional auto detailing, ceramic coating, and paint protection to keep your vehicle looking showroom-new.",
        "products": [
            ("Exterior Detailing", "Professional wash, wax, and tire shine.", "https://images.unsplash.com/photo-1552820728-8ac41f1ce891?auto=format&fit=crop&w=900&q=80"),
            ("Interior Detailing", "Complete interior cleaning and conditioning.", "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80"),
            ("Ceramic Coating", "Long-lasting paint protection and shine.", "https://images.unsplash.com/photo-1485463709029-ba19537556dd?auto=format&fit=crop&w=900&q=80"),
            ("Paint Correction", "Remove swirls, scratches, and oxidation.", "https://images.unsplash.com/photo-1517422250217-7fceb8b04fcd?auto=format&fit=crop&w=900&q=80"),
            ("Window Tinting", "Professional window tinting for comfort and style.", "https://images.unsplash.com/photo-1550355291-bbee04a92027?auto=format&fit=crop&w=900&q=80"),
            ("Fleet Services", "Comprehensive detailing for business fleets.", "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=900&q=80"),
        ],
        "services": [
            ("Exterior", ["Hand wash", "Wax application", "Tire shine"]),
            ("Interior", ["Vacuum & shampoo", "Leather conditioning", "Odor removal"]),
            ("Protection", ["Ceramic coating", "Paint sealant", "Clear film protection"]),
            ("Restoration", ["Paint correction", "Headlight restoration", "Trim restoration"]),
            ("Specialty", ["Engine detailing", "Undercarriage wash", "Window tinting"]),
            ("Fleet", ["Bulk discounts", "Regular maintenance", "Custom packages"]),
        ],
        "location": "1020 Auto Boulevard, Phoenix, AZ 85001",
        "phone": "+16025551234",
        "hero_image": "https://images.unsplash.com/photo-1552820728-8ac41f1ce891?auto=format&fit=crop&w=1920&q=80",
        "primary_dark": "#1a3a52",
        "primary_mid": "#2d5a7b",
        "primary_light": "#4a7ba7",
        "gold": "#f4a261",
        "gold_soft": "#f8b88d",
    },
}

for business_name, data in BUSINESSES.items():
    base_path = f'/Users/diego/websites/{business_name}'
    os.makedirs(base_path, exist_ok=True)
    
    # Just verify the directories exist
    print(f"✓ Ready for {business_name}")

print("\nPrepared directories for batch generation!")

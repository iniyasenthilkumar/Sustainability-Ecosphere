import datetime

def get_daily_tip():
    """
    Returns a curated eco tip of the day, changing daily.
    """
    tips = [
        {
            "tip": "Switch to LED bulbs. They use 75% less energy and last 25 times longer than incandescent lighting.",
            "category": "Energy"
        },
        {
            "tip": "Shorten your shower by just 2 minutes to save up to 10 gallons (approx. 38 liters) of water.",
            "category": "Water"
        },
        {
            "tip": "Unplug electronics when not in use. 'Phantom loads' can account for up to 10% of your electricity bill.",
            "category": "Energy"
        },
        {
            "tip": "Use a reusable water bottle. It takes 3 times more water to make a plastic bottle than to fill it.",
            "category": "Waste"
        },
        {
            "tip": "Compost food scraps. Food waste decomposing in landfills creates methane, a gas 28x more potent than CO2.",
            "category": "Waste"
        },
        {
            "tip": "Grow native flora. Native plants require significantly less water, pesticide, and support local ecosystems.",
            "category": "Ecosystem"
        },
        {
            "tip": "Wash laundry in cold water. Nearly 75-90% of a washing machine's energy goes to heating the water.",
            "category": "Energy"
        },
        {
            "tip": "Plant trees! A single mature tree can absorb approximately 22 kg of carbon dioxide annually.",
            "category": "Trees"
        },
        {
            "tip": "Say no to plastic packaging. Buy in bulk or choose items with minimal, biodegradable packaging.",
            "category": "Waste"
        },
        {
            "tip": "Practice active transportation. Walk, bike, or use public transit whenever possible to reduce vehicle emissions.",
            "category": "Transport"
        },
        {
            "tip": "Set your thermostat 1-2 degrees Celsius lower in winter and higher in summer to save heating/cooling energy.",
            "category": "Energy"
        },
        {
            "tip": "Fix leaky faucets immediately. A dripping tap can waste more than 11,000 liters of water a year.",
            "category": "Water"
        }
    ]
    
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return tips[day_of_year % len(tips)]

def calculate_carbon_footprint(transport_km, transport_type, electricity_kwh, waste_kg, recycling_rate):
    """
    Calculates carbon emissions in kg CO2e per month.
    
    Factors:
    - Transport (per km):
        * Petrol/Diesel Car: 0.17 kg CO2/km
        * Hybrid Car: 0.10 kg CO2/km
        * Electric Car: 0.05 kg CO2/km
        * Public Transit: 0.04 kg CO2/km
        * Walk/Cycle: 0 kg CO2/km
    - Electricity:
        * 0.82 kg CO2 per kWh (Grid average)
    - Waste (per kg):
        * Landfill waste: 1.2 kg CO2 per kg
        * Recycled waste: 0.2 kg CO2 per kg
    """
    
    # 1. Transport Emissions
    transport_factors = {
        'car_fossil': 0.17,
        'car_hybrid': 0.10,
        'car_electric': 0.05,
        'public': 0.04,
        'walk_bike': 0.00
    }
    factor = transport_factors.get(transport_type, 0.17)
    # Convert weekly travel distance to monthly travel (4.33 weeks in a month)
    monthly_km = float(transport_km) * 4.33
    transport_emissions = monthly_km * factor
    
    # 2. Electricity Emissions
    energy_emissions = float(electricity_kwh) * 0.82
    
    # 3. Waste Emissions
    # Splitting waste by recycling rate
    rate = float(recycling_rate) / 100.0
    monthly_waste = float(waste_kg) * 4.33
    recycled_portion = monthly_waste * rate
    landfill_portion = monthly_waste * (1 - rate)
    
    waste_emissions = (landfill_portion * 1.2) + (recycled_portion * 0.2)
    
    # Total
    total_emissions = transport_emissions + energy_emissions + waste_emissions
    
    return {
        'transport': round(transport_emissions, 2),
        'energy': round(energy_emissions, 2),
        'waste': round(waste_emissions, 2),
        'total': round(total_emissions, 2)
    }

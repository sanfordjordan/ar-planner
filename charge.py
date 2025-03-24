from typing import List

from Objects.legObject import Leg

def calcTorchBatteries(legs: List[Leg]):
    HEAD_TORCH_BATTERY_LIFE = 6  # hours
    BIKE_TORCH_BATTERY_LIFE = 6  # hours

    head_torch_life = HEAD_TORCH_BATTERY_LIFE
    bike_torch_life = BIKE_TORCH_BATTERY_LIFE
    spare_head_batteries = 0
    bike_torch_charge_legs = []
    
    for i, leg in enumerate(legs):
        legnum = leg.number
        if leg.discipline == 'TA': continue
        night_hours = leg.weather['is_day'].value_counts().get(0, 0)
        if night_hours == 0: continue
        
        # Head torch usage
        head_torch_life -= night_hours
        if head_torch_life <= 0:
            batteries_needed = ((-head_torch_life) // HEAD_TORCH_BATTERY_LIFE) + 1
            spare_head_batteries += batteries_needed
            head_torch_life += batteries_needed * HEAD_TORCH_BATTERY_LIFE
            leg.batteries = batteries_needed

        # Bike torch usage
        if leg.discipline == 'Bike':
            bike_torch_life -= night_hours

            next_bike_leg = None
            for future_leg in legs[i+1:]:
                if future_leg.discipline == 'Bike':
                    next_bike_leg = future_leg
                    break

            if next_bike_leg:
                next_bike_night_hours = next_bike_leg.weather['is_day'].value_counts().get(0, 0)
                if bike_torch_life < next_bike_night_hours and bike_torch_life < 0.75 * BIKE_TORCH_BATTERY_LIFE:
                        bike_torch_charge_legs.append(legs[i+2].number)
            
    print(bike_torch_charge_legs)
    
    return {
        'spare_head_batteries': spare_head_batteries,
        'spare_bike_batteries': bike_torch_charge_legs
    }
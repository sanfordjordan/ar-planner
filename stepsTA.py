from typing import List
from Objects.clothingObject import Clothing

from Objects.legObject import Leg

def calcAllTASteps(legs: List[Leg]) -> list:
    for i, leg in enumerate(legs):
        if leg.discipline == 'TA': 
            leg.steps = calcTASteps(legs[i-1], leg, legs[i+1])
    print(legs[1].steps)

def calcTASteps(prev_leg: Leg, currentTA: Leg, next_leg: Leg) -> list:
    def formatClothingChange(prefix: str, items: list) -> str:
        if not items:
            return ""
        item_names = [item[0] for item in items]
        items_str = ", ".join(item_names)
        return f"{prefix}: {items_str}"
    
    offClothes, onClothes = compareClothing(prev_leg.clothing, next_leg.clothing)

    steps = []
    if prev_leg.discipline == 'Kayak':
        steps.append('Pack up kayak and paddling gear')
        steps.append(formatClothingChange('OFF', offClothes))
        steps.append(formatClothingChange('ON', onClothes))
        steps.append('Wet stuff in garbage bag')
    elif prev_leg.discipline == 'Bike':
        steps.append('Pack up bike in box')


    if currentTA.sleepDuring:
        steps.append('Set up tent and sleeping gear')

    if next_leg.discipline == 'Bike':
        steps.append('Assemble bike')
    if next_leg.discipline == 'Kayak':
        steps.append('Set up kayak')

    if prev_leg.discipline != 'Kayak':
        steps.append(formatClothingChange('OFF', offClothes))
        steps.append(formatClothingChange('ON', onClothes))

    return steps

def compareClothing(prev_clothing: Clothing, next_clothing: Clothing) -> tuple:
    # Helper function to flatten and label items by category
    def flatten_clothing(clothing):
        items = []
        for category in ['head', 'body', 'hand', 'legs', 'feet']:
            for item in getattr(clothing, category):
                items.append((item, category))
        return set(items)

    prev_items = flatten_clothing(prev_clothing)
    next_items = flatten_clothing(next_clothing)

    # Items to remove (ON in prev but not in next)
    to_remove = prev_items - next_items
    # Items to add (ON in next but not in prev)
    to_add = next_items - prev_items

    # Sort removals and additions by category for clean order
    to_remove_sorted = sorted(to_remove, key=lambda x: x[1])
    to_add_sorted = sorted(to_add, key=lambda x: x[1])

    return to_remove_sorted, to_add_sorted
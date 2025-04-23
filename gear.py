from typing import List, Optional, Set, Tuple
from Objects.gearObject import Gear
from Objects.gearRules import GEAR_RULES
from Objects.legObject import Leg
from clothes import isHat, isHelmet
from utils import getThing



def apppendGear2(legs: List[Leg], gear: List[Gear]):
    activity_legs = [leg for leg in legs if leg.discipline != 'TA']

    for gear_item in gear:
        if gear_item.name in GEAR_RULES:
            relevant_legs = [
                leg.number for leg in activity_legs 
                if GEAR_RULES[gear_item.name](leg)
            ]
            print(relevant_legs)
            if relevant_legs:
                gear_item.legs = relevant_legs
                gear_item.journey = plan_item(gear_item, legs)
                print(gear_item.name, gear_item.journey)
    
    print(gear[2].journey)

def appendGear(leg: Leg):
    gear = []
    for hikeGear in calcHikingGear(leg): gear.append(hikeGear)
    for kayakGear in calcKayakGear(leg): gear.append(kayakGear)
    for bikeGear in calcBikeGear(leg): gear.append(bikeGear)
    if leg.batteries > 0: gear.append(f"{leg.batteries} batteries")
    leg.gear = gear
  
  
def calcHikingGear(leg: Leg):
    hikeGear = []
    if leg.discipline != 'Hike': return []
    if leg.elevation > 500: hikeGear.append('hiking poles')
    return hikeGear

def calcKayakGear(leg: Leg):
    kayakGear = ['kayak paddles', 'kayak seats', 'kayak handle', 'dry bags', 'throw rope']
    if leg.discipline != 'Kayak': return []
    #if night, glowsticks
    return kayakGear

def calcBikeGear(leg: Leg):
    bikeGear = ['bike torch', 'map board']
    if leg.discipline != 'Bike': return []
    return bikeGear

def appendTAGear(legs: List[Leg]):
    """Determines the gear needed in TA"""
    gearTA = []
    
    for index, leg in enumerate(legs):
        if leg.discipline != 'TA': continue

        if leg.sleepDuring == True:
            gearTA.extend(["tent", "sleeping bag"])

        nextLeg = legs[index+1]
        if nextLeg.chargeBikeTorch: gearTA.append('bike torch charger')

        prevLeg= legs[index-1]
        if prevLeg.discipline == "Kayak":
            gearTA.extend(["towel", "empty garbage bag"])
        leg.gear = gearTA

class ItemPlan:
    def __init__(self, item_location, score):
        # item_location is an array of length num_legs, each element describes where the item is during that leg
        # e.g. ['carry', 'Box A', 'carry', 'Box B', 'carry', ...]
        self.item_location = item_location
        self.score = score
    def __str__(self) -> str:
        return f"Plan(score={self.score:.2f}, locations={self.item_location})"

    def __repr__(self) -> str:
        return self.__str__()

def plan_item(gear: Gear, legs: List[Leg]) -> List[ItemPlan]:
    """
    Main function to plan where an item should be throughout the race
    """
    # Filter out TA legs, keeping only activity legs
    activity_legs = [leg for leg in legs if leg.discipline != 'TA']
    
    item_plans = []
    for item_num in range(gear.amount):
        possible_plans = generate_possible_plans(gear, activity_legs, item_num)
        best_plan = min(possible_plans, key=lambda x: x.score)
        item_plans.append(best_plan)
    
    best_plan = min(item_plans, key=lambda x: x.score)
    return best_plan.item_location
    
def generate_possible_plans(gear: Gear, legs: List[Leg], item_num: int) -> List[ItemPlan]:
    """Generate all possible valid plans for this copy of the item"""
    activity_legs = [leg for leg in legs if leg.discipline != 'TA']
    num_legs = len(activity_legs)
    required_legs = gear.legs
    all_segment_paths = []
    
    # Get paths from start to first required leg
    all_segment_paths.append(find_path(1, required_legs[0], legs))
    
    # Get paths between consecutive required legs
    for i in range(len(required_legs) - 1):
        all_segment_paths.append(find_path(required_legs[i], required_legs[i + 1], legs))

    possible_plans = []
    
    def combine_segments(current_plan: List[Tuple[str, int, int]], segment_index: int):
        if segment_index == len(all_segment_paths):
            # Create plan array and fill with path actions
            item_location = ['none'] * num_legs
            for action, start, _ in current_plan:
                item_location[start - 1] = action
                
            # Ensure required legs are marked as 'use'
            for leg in required_legs:
                item_location[leg - 1] = 'use'
            
            possible_plans.append(ItemPlan(
                item_location=item_location,
                score=score_plan(item_location, activity_legs)
            ))
            return
        
        # Try each path for this segment
        for path in all_segment_paths[segment_index]:
            combine_segments(current_plan + path, segment_index + 1)
    
    combine_segments([], 0)
    return possible_plans

def find_path(start: int, end: int, legs: List[Leg]) -> List[List[Tuple[str, int, int]]]:
    """Find all possible paths between two required legs using DFS"""
    all_paths = []
    def dfs(current_leg: int, current_path: List[Tuple[str, int, int]], current_box: Optional[str] = None):
        if current_leg == end:
            all_paths.append(current_path.copy())
            return
            
        # Get boxes available at this leg
        current_boxes = legs[current_leg - 1].boxes.boxesArray
        next_boxes = legs[current_leg].boxes.boxesArray  # Boxes available at next leg

        if current_box:
            # If item is in a box, we can only continue if that box is available now
            if current_box in current_boxes:
                if current_box in next_boxes:
                    # Can keep it in the same box if available next leg
                    box_path = current_path + [(current_box, current_leg, current_leg + 1)]
                    dfs(current_leg + 1, box_path, current_box)
                # Can take it out and carry
                carry_path = current_path + [('carry', current_leg, current_leg + 1)]
                dfs(current_leg + 1, carry_path, None)
            else:
                # Box not available, can't access item
                return
        else:
            # Item is being carried, can either keep carrying or put in a box
            carry_path = current_path + [('carry', current_leg, current_leg + 1)]
            dfs(current_leg + 1, carry_path, None)
            
            # Can put in any available box
            for box in current_boxes:
                if box in next_boxes:  # Only if box will be available next leg
                    box_path = current_path + [(box, current_leg, current_leg + 1)]
                    dfs(current_leg + 1, box_path, box)
    
    dfs(start, [], None)
    return all_paths


def score_plan(plan: List[str], legs: List[Leg]) -> float:
    """Score a complete plan based on box usage and carrying penalties"""
    score = 0
    
    for leg_num, location in enumerate(plan):
        if location == 'bike': score += 2
        elif location == 'paddle': score += 3
        elif location not in ['use', 'carry']:  # Regular boxes
            score += 1
        
        elif location == 'carry' and leg_num < len(legs):
            leg = legs[leg_num]
            if leg.discipline != 'TA':
                multiplier = {
                    'Kayak': 1,
                    'Bike': 2,
                    'Hike': 4
                }.get(leg.discipline, 0)
                score += multiplier * float(leg.avgTime)
    
    return score
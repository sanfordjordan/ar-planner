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
        best_plan = select_best_plan(possible_plans, activity_legs)
        item_plans.append(best_plan)
    
    best_plan = min(item_plans, key=lambda x: x.score)
    return best_plan.item_location
    
def generate_possible_plans(gear: Gear, legs: List[Leg], item_num: int) -> List[ItemPlan]:
    """Generate all possible valid plans for this copy of the item"""
    activity_legs = [leg for leg in legs if leg.discipline != 'TA']
    num_legs = len(activity_legs)
    required_legs = gear.legs
    
    # Generate paths between consecutive required legs
    all_segment_paths = []
    
    # First, generate paths from leg 1 to first required leg
    first_required_leg = required_legs[0]
    initial_paths = find_path(1, first_required_leg, legs, required_legs)
    all_segment_paths.append(initial_paths)
    
    # Then generate paths between consecutive required legs
    for i in range(len(required_legs) - 1):
        start_leg = required_legs[i]
        end_leg = required_legs[i + 1]
        segment_paths = find_path(start_leg, end_leg, legs, required_legs)
        all_segment_paths.append(segment_paths)
    # Generate all possible combinations of path segments
    possible_plans = []
    
    def combine_segments(current_plan: List[Tuple[str, int, int]], segment_index: int):
        """Recursively combine path segments into complete plans"""
        # If we've used all segments, we have a complete plan
        if segment_index == len(all_segment_paths):
            # Convert the combined path to a plan array
            item_location = ['none'] * num_legs
            
            # Fill in the plan based on the path
            for action, start, end in current_plan:
                if action.startswith('Box '):
                    # Item is in a box for this leg
                    item_location[start - 1] = action
                elif action == 'use':
                    # Item is being used
                    item_location[start - 1] = 'use'
                elif action == 'carry':
                    # Item is being carried
                    item_location[start - 1] = 'carry'
                elif action == 'take_from_box':
                    # This is a transition action, the next action will determine what happens
                    continue
            
            # Make sure the final required leg is marked as 'use'
            item_location[required_legs[-1] - 1] = 'use'
            
            # Create ItemPlan object with the item_location and calculate its score
            score = score_plan(item_location, activity_legs)
            item_plan = ItemPlan(item_location=item_location, score=score)
            possible_plans.append(item_plan)
            return
        
        # Try each possible path for this segment
        for path in all_segment_paths[segment_index]:
            combine_segments(current_plan + path, segment_index + 1)
    
    # Start combining segments with empty plan
    combine_segments([], 0)
    
    return possible_plans


def find_paths_between_required_legs(start: int, end: int, activity_legs: List[Leg], required_legs: List[int]) -> List[List[Tuple[str, int, int]]]:
    """Find all possible paths between two required legs using DFS"""
    all_paths = []
    
    def dfs(current_leg: int, current_path: List[Tuple[str, int, int]], current_box: Optional[str] = None):
        if current_leg == end:
            all_paths.append(current_path.copy())
            return
            
        # Get available boxes at the NEXT leg (where the item will actually be)
        next_leg_idx = current_leg  # Because activity_legs is 0-based
        available_boxes = activity_legs[next_leg_idx].boxes.boxesArray
        
        if current_leg == start:
            if start in required_legs:
                dfs(current_leg + 1, current_path + [('use', current_leg, current_leg + 1)], None)
            else:
                # Can carry
                carry_path = current_path + [('carry', current_leg, current_leg + 1)]
                dfs(current_leg + 1, carry_path, None)
                
                # Can put in any available box
                for box in available_boxes:
                    box_path = current_path + [(f'Box {box}', current_leg, current_leg + 1)]
                    dfs(current_leg + 1, box_path, box)
            return
        
        # Get available boxes at current leg (using 0-based index for activity_legs)
        available_boxes = activity_legs[current_leg - 1].boxes.boxesArray
        
        # Option 1: If carrying item (not in box)
        if current_box is None:
            # Continue carrying
            carry_path = current_path + [('carry', current_leg, current_leg + 1)]
            dfs(current_leg + 1, carry_path, None)
            
            # Try putting in any available box
            for box in available_boxes:
                box_path = current_path + [(f'Box {box}', current_leg, current_leg + 1)]
                dfs(current_leg + 1, box_path, box)
        
        # Option 2: If item is in a box
        else:
            # If box is available here
            if current_box in available_boxes:
                # Can take it out and carry
                new_path = current_path + [('take_from_box', current_leg, current_leg), 
                                         ('carry', current_leg, current_leg + 1)]
                dfs(current_leg + 1, new_path, None)
                
                # Can take out and put in different box
                for box in available_boxes:
                    if box != current_box:
                        new_path = current_path + [('take_from_box', current_leg, current_leg),
                                                 (f'Box {box}', current_leg, current_leg + 1)]
                        dfs(current_leg + 1, new_path, box)
                
                # Can keep in same box
                box_path = current_path + [(f'Box {current_box}', current_leg, current_leg + 1)]
                dfs(current_leg + 1, box_path, current_box)
            else:
                # Box not available here, must carry
                carry_path = current_path + [('carry', current_leg, current_leg + 1)]
                dfs(current_leg + 1, carry_path, None)
    
    dfs(start, [], None)
    return all_paths

def find_path(start: int, end: int, legs: List[Leg], required_legs: List[int]) -> List[List[Tuple[str, int, int]]]:
    """Find all possible paths between required legs"""
    #print(f"\nFinding paths from leg {start} to {end}")
    
    # Get all possible paths for this segment
    possible_paths = find_paths_between_required_legs(start, end, legs, required_legs)
    
    # Print all found paths
    #for i, path in enumerate(possible_paths):
        #print(f"Path option {i + 1}: {path}")
    
    return possible_paths

def score_plan(plan: List[str], legs: List[Leg]) -> float:
    """Score a complete plan based on box usage and carrying penalties"""
    score = 0
    
    for leg_num, location in enumerate(plan):
        if location.startswith('Box'):
            # Box penalties
            box_multiplier = {
                'Box A': 1, 'Box B': 1, 'Box C': 1, 'Box D': 1,
                'Bike Box': 2, 'Paddle Bag': 3
            }.get(location, 1)
            score += box_multiplier
        
        elif location == 'carry' and leg_num < len(legs):
            # Carry penalties
            leg = legs[leg_num]
            if leg.discipline != 'TA':
                multiplier = {
                    'Kayak': 1,
                    'Bike': 2,
                    'Hike': 4
                }.get(leg.discipline, 0)
                score += multiplier * float(leg.avgTime)
    
    return score

def select_best_plan(possible_plans: List[ItemPlan], legs: List[Leg]) -> ItemPlan:
    """Select the best plan based on score"""
    return min(possible_plans, key=lambda x: x.score)
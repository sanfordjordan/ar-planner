from typing import List, Dict
from Objects.gearObject import Gear
from Objects.legObject import Leg
from utils import getThing



def apppendGear2(legs: List[Leg], gear: List[Gear]):\

    sunHat = getThing('sun hat', gear)
    for index, leg in enumerate(legs):
        if ((leg.weather['is_day'] == 1).any()): sunHat.legs.append(leg.number)
    a = itemPlanner(legs, sunHat)
    print(a)


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


def itemPlanner(legs: List[Leg], gear: Gear) -> List[List[str]]:
    if gear.amount == 0: return []
    if gear.legs == []: return []

    totalLegs = legs[-1].number
    item_tracks = [["" for _ in range(totalLegs)] for _ in range(gear.amount)]

    firstLoc = gear.legs[0]
    if firstLoc != 1: startBox = boxPriority(next((l for l in legs if l.number == firstLoc), None))
   
    a = find_item_paths(legs, [1,5])
    print(a)

    # for index, leg in enumerate(legs):
    #     if leg.discipline == 'TA': continue
    #     currentLeg = leg.number
        
    #     isWanted = leg.number in gear.legs
    #     availableLocations = getAvailableSpots(leg)
    #     #isAccessible = any(item_tracks[item_index][currentLeg - 2] in availableLocations for item_index in range(gear.amount))
    #     isAccessible = True#any(item_tracks[0][currentLeg - 2] in availableLocations)

    #     if isWanted:
    #         if leg.number == firstLoc or isAccessible: 
    #             item_tracks[0][index] = "use"
    #             continue

    #     elif currentLeg < firstLoc:  item_tracks[0][index] = startBox
   
    #     else:
    #         nextLoc = next((l for l in legs if l.number in gear.legs and l.number > currentLeg), None)
    #         if nextLoc is None:
    #             break
    #         nextAvailableLocations = getAvailableSpots(nextLoc)

        
        #check if item can get to next needed location (without carry):
        #DFS with boxes as options

        #check if item can get to next needed location (without carry)
        #if true, proceed
        #if false AND only 1 item check if item can get to next needed location (with carry)
        #else added 2nd item to this location
        #iterate through eah item to see who can get to next location
        #if none, iterate through with carry, use lowest score


    return item_tracks

def boxPriority(leg: Leg) -> str:
    boxes = leg.boxes
    if boxes.hasBoxA: return 'Box A'
    if boxes.hasBoxB: return 'Box B'
    if boxes.hasBoxC: return 'Box C'
    if boxes.hasBoxD: return 'Box D'
    if boxes.hasBikeBox: return 'Bike Box'
    if boxes.hasPaddleBag: return 'Paddle Bag'
    return None

def getAvailableSpots(leg: Leg) -> list[str]:
    return ['Use', 'Carry'] + leg.boxes.boxesArray

def find_item_paths(legs, use_legs):
    from collections import defaultdict

    # Build a map of which boxes are available at the start of each leg
    box_at_leg = {}
    for leg in legs:
        leg_number = leg.number
        box_at_leg[leg_number] = [b for b in leg.boxes.boxesArray if b]

    # DFS to find all valid box paths between each pair of use legs
    def dfs_paths(start_leg, end_leg, path, visited, results):
        if start_leg == end_leg:
            results.append(path.copy())
            return
        if start_leg >= end_leg:
            return

        # Boxes available AFTER completing start_leg → at start of (start_leg + 1)
        next_leg = start_leg + 1
        available_boxes = box_at_leg.get(next_leg, [])
        for box in available_boxes:
            if (start_leg, box) in visited:
                continue
            visited.add((start_leg, box))
            for future_leg in range(next_leg + 1, end_leg + 1):
                if box in box_at_leg.get(future_leg, []):
                    path.append((start_leg, box, future_leg))
                    dfs_paths(future_leg, end_leg, path, visited, results)
                    path.pop()
            visited.remove((start_leg, box))

    # Chain DFS between each pair of wanted legs
    all_paths = []
    for i in range(len(use_legs) - 1):
        start = use_legs[i]
        end = use_legs[i + 1]
        results = []
        dfs_paths(start, end, [], set(), results)
        all_paths.append(results)

    return all_paths
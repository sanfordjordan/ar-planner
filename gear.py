from typing import List

from Objects.legObject import Leg


def appendGear(leg: Leg):
    gear = []
    for hikeGear in calcHikingGear(leg): gear.append(hikeGear)
    for kayakGear in calcKayakGear(leg): gear.append(kayakGear)
    for bikeGear in calcBikeGear(leg): gear.append(bikeGear)
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

        prevLeg= legs[index-1]
        if prevLeg.discipline == "Kayak":
            gearTA.extend(["towel", "empty garbage bag"])
        leg.gear = gearTA

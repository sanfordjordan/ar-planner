def getGear(leg):
    gear = []
    for hikeGear in calcHikingGear(leg): gear.append(hikeGear)
    for kayakGear in calcKayakGear(leg): gear.append(kayakGear)
    for bikeGear in calcBikeGear(leg): gear.append(bikeGear)

    return gear  
  
  
def calcHikingGear(leg):
    hikeGear = []
    if leg.discipline != 'Hike': return []
    if leg.elevation > 500: hikeGear.append('hiking poles')
    return hikeGear

def calcKayakGear(leg):
    kayakGear = ['kayak paddles', 'kayak seats', 'kayak handle', 'dry bags', 'throw rope']
    if leg.discipline != 'Kayak': return []
    #if night, glowsticks
    return kayakGear

def calcBikeGear(leg):
    bikeGear = ['bike torch', 'map board']
    if leg.discipline != 'Bike': return []
    return bikeGear

def getTAGear(prevLeg):
    """Determines the gear needed for cleaning up after the previous leg."""
    
    cleanupGear = []
    
    if prevLeg == 'NA': return cleanupGear  # No cleanup gear needed if there's no previous leg

    discipline = prevLeg.discipline

    if discipline == "Kayak":
        cleanupGear.extend(["towel", "empty garbage bag"])
    return cleanupGear
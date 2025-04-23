
from Objects.legObject import Leg


def isHelmet(leg: Leg):
   #If biking or rapids/ ocean kayaking
   if leg.discipline == 'Bike': return True
   if leg.kayakType == 'R' or leg.kayakType == 'O': return True
   return False

def isHat(leg: Leg):
    #If some daytime
    return (leg.weather['is_day'] == 1).any()

GEAR_RULES = {
    'sun hat': lambda leg: isHat(leg),
    'helmet': lambda leg: isHelmet(leg),
  
    
    # Add more gear mappings...
}
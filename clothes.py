from Objects.clothingObject import Clothing
from Objects.legObject import Leg


def appendClothes(leg: Leg):
    clothing = Clothing()
    if isHat(leg): clothing.head.append('sun hat')
    if isHelmet(leg): clothing.head.append('helmet')
    if isSunglasses(leg): clothing.head.append('sunglasses')
    if isBuff(leg): clothing.head.append('buff')
    if isHeadTorch(leg): clothing.head.append('head torch')
    if isMapCase(leg): clothing.head.append('map case')

    for top in calcTops(leg): clothing.body.append(top)
    clothing.hand.append('watch')
    if isThumbpass(leg): clothing.hand.append('thumbpass')
    gloves = calcGloves(leg)
    if gloves is not None: clothing.hand.append(gloves)
    for bottom in calcBottoms(leg): clothing.legs.append(bottom)
    for footwear in calcFeet(leg): clothing.feet.append(footwear) 
    leg.clothing = clothing  
  
  
def isHelmet(leg: Leg):
   #If biking or ocean kayaking
   if leg.discipline == 'Bike': return True
   if leg.kayakType == 'R': return True
   return False

def isHat(leg: Leg):
    #If some daytime
    return (leg.weather['is_day'] == 1).any()

def isSunglasses(leg: Leg):
    #If ocean kayaking OR daytime and not cloudy
    if leg.kayakType == 'O': return True
    
    if 'is_day' in leg.weather.columns and 'cloud_cover' in leg.weather.columns:
        daytime = leg.weather[leg.weather['is_day'] == 1]
        if not daytime.empty and (daytime['cloud_cover'] < 30).any():
            return True
    return False

def isBuff(leg: Leg):
    return leg.minTemp <= 20

def isHeadTorch(leg: Leg):
    #If some daytime
    return (leg.weather['is_day'] == 0).any()

def isMapCase(leg: Leg):
    return leg.discipline == 'Kayak'

def calcTops(leg: Leg):
    tops = []
    if leg.discipline == 'Kayak':
        if leg.kayakType == 'R':
            if leg.minTemp <= 16: tops.append('wetsuit')
            else:
                tops.append('shirt')
                if leg.minTemp <= 15: tops.append('kayak layer')
                if leg.minTemp <= 20: tops.append('rainjacket')
                elif leg.minTemp <= 25: tops.append('arm warmers')
      
        else:
            if (leg.minTemp <= 8): tops.append('wetsuit')
            else:
                tops.append('shirt')
                if leg.minTemp <= 15: tops.append('kayak layer')
                if leg.minTemp <= 20: tops.append('rainjacket')
                elif leg.minTemp <= 25: tops.append('arm warmers')
                
    if leg.discipline == 'Bike':
        tops.append('bike shirt')
        if leg.minTemp <= 4: tops.append('fleece')
        if leg.minTemp <= 9: tops.append('thermal')
        if leg.minTemp <= 17: tops.append('rainjacket')
        elif leg.minTemp <= 22: tops.append('arm warmers')
        
    if leg.discipline == 'Hike':
        tops.append('hike shirt')
        if leg.minTemp <= 4: tops.append('fleece')
        if leg.minTemp <= 9: tops.append('thermal')
        if leg.minTemp <= 17: tops.append('rainjacket')
        
    return tops

def isThumbpass(leg: Leg):
    return leg.discipline == 'Hike'

def calcGloves(leg: Leg):
    if leg.discipline == 'Bike':
        if leg.minTemp <= 10: return 'full bike glove'
        return 'fingerless gloves'
    if leg.discipline == 'Kayak': return 'kayak gloves'
    if leg.discipline == 'Trek': return 'any glove'
    return None

def calcBottoms(leg: Leg):
    bottoms = ['underwear']
    if leg.discipline == 'Kayak':
        bottoms.append('leg compass')
        if leg.kayakType == 'R':
            if leg.minTemp <= 16: bottoms.append('wetsuit')
            else:
                if leg.minTemp <= 15: bottoms.append('wetsuit pants')
                if leg.minTemp <= 20: bottoms.append('leg warmers')
                if leg.minTemp > 15: bottoms.append('shorts')
      
        else:
            if (leg.minTemp <= 8): bottoms.append('wetsuit')
            else:
                if leg.minTemp <= 15: bottoms.append('wetsuit pants')
                if leg.minTemp <= 20: bottoms.append('leg warmers')
                if leg.minTemp > 15: bottoms.append('shorts')
                
    if leg.discipline == 'Bike':
        bottoms.append('bike shorts')
        if leg.minTemp <= 5: bottoms.append('thermal')
        if leg.minTemp <= 10: bottoms.append('rain pants')
        if leg.minTemp <= 22: bottoms.append('leg warmers')
        
    if leg.discipline == 'Hike':
        bottoms.append('shorts')
        bottoms.append('gaiters')
        if leg.minTemp <= 4: bottoms.append('thermal')
        if leg.minTemp <= 8: bottoms.append('rain pants')
        if leg.minTemp <= 14: bottoms.append('leg warmers')
        
    return bottoms


def calcFeet(leg: Leg):
    feet = ['socks']
    if leg.discipline == 'Kayak':
        if leg.kayakType == 'R': feet.append('old shoes')
        else: feet = ['water shoes']
    
    if leg.discipline == 'Bike':
        feet.append('bike shoes')
        
    if leg.discipline == 'Hike':
        feet.append('trail runners')
  
    return feet
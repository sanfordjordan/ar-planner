def getClothes(leg):
    clothing = []
    if isHelmet(leg): clothing.append('helmet')
    if isHat(leg): clothing.append('hat')
    if isSunglasses(leg): clothing.append('sunglasses')
    if isBuff(leg): clothing.append('buff')
    if isMapCase(leg): clothing.append('map case')
    for top in calcTops(leg): clothing.append(top)
    clothing.append('watch')
    if isThumbpass(leg): clothing.append('thumbpass')
    clothing.append(calcGloves(leg))
    for bottom in calcBottoms(leg): clothing.append(bottom)
    for footwear in calcFeet(leg): clothing.append(footwear) 
    return clothing  
  
  
def isHelmet(leg):
   if leg.discipline == 'Bike': return True
   if leg.rapids == 'Y': return True
   return False

def isHat(leg):
   #weather scrape, time
   return True

def isSunglasses(leg):
    #weather, time
    #if sunny, if kayaking ocean
   return False

def isBuff(leg):
    return leg.minTemp <= 22

def isMapCase(leg):
    return leg.discipline == 'Kayak'

def calcTops(leg):
    tops = []
    if leg.discipline == 'Kayak':
        if leg.rapids == True:
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
        
    if leg.discipline == 'hike':
        tops.append('hike shirt')
        if leg.minTemp <= 4: tops.append('fleece')
        if leg.minTemp <= 9: tops.append('thermal')
        if leg.minTemp <= 17: tops.append('rainjacket')
        
    return tops

def isThumbpass(leg):
    return leg.discipline == 'Hike'

def calcGloves(leg):
    if leg.discipline == 'Bike':
        if leg.minTemp <= 10: return 'full bike glove'
        return 'fingerless gloves'
    if leg.discipline == 'Kayak': return 'kayak gloves'
    if leg.discipline == 'Trek': return 'any glove'
    return ''

def calcBottoms(leg):
    bottoms = ['underwear']
    if leg.discipline == 'Kayak':
        bottoms.append('leg compass')
        if leg.rapids == True:
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
        
    if leg.discipline == 'hike':
        bottoms.append('shorts')
        bottoms.append('gaiters')
        if leg.minTemp <= 4: bottoms.append('thermal')
        if leg.minTemp <= 8: bottoms.append('rain pants')
        if leg.minTemp <= 14: bottoms.append('leg warmers')
        
    return bottoms


def calcFeet(leg):
    feet = ['socks']
    if leg.discipline == 'Kayak':
        if leg.rapids == True: feet.append('old shoes')
        else: feet.append('water shoes')
    
    if leg.discipline == 'Bike':
        feet.append('bike shoes')
        
    if leg.discipline == 'hike':
        feet.append('trail runners')
  
    return feet
class Gear:
  def __init__(self, gearStuff):
    self.name = gearStuff[0]
    self.category = gearStuff[1]
    self.subcategory = gearStuff[2]
    self.weight = float(gearStuff[3])
    self.amount = int(gearStuff[4])
    self.legs = []

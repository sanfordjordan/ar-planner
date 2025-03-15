class Food:
  def __init__(self, foodStuff):
    self.name = foodStuff[0]
    self.grams = float(foodStuff[1]) if foodStuff[1] else 0.0
    self.kJ = float(foodStuff[2]) if foodStuff[2] else 0.0
    self.fibre = float(foodStuff[3]) if foodStuff[3] else 0.0
    self.fat = float(foodStuff[4]) if foodStuff[4] else 0.0
    self.protein = float(foodStuff[5]) if foodStuff[5] else 0.0
    self.carbs = float(foodStuff[6]) if foodStuff[6] else 0.0
    self.sugar = float(foodStuff[7]) if foodStuff[7] else 0.0
    self.calcium = float(foodStuff[8]) if foodStuff[8] else 0.0
    self.magnesium = float(foodStuff[9]) if foodStuff[9] else 0.0
    self.phosphorus = float(foodStuff[10]) if foodStuff[10] else 0.0
    self.potassium = float(foodStuff[11]) if foodStuff[11] else 0.0
    self.sodium = float(foodStuff[12]) if foodStuff[12] else 0.0
    self.caffeine = float(foodStuff[13]) if foodStuff[13] else 0.0
    self.water = float(foodStuff[14]) if foodStuff[14] else 0.0
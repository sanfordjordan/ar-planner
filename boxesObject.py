class Box:
  def __init__(self, boxes):
    boxesArray = boxes.split(",")
    
    startGear = False
    paddleBag = False
    bikeBox = False
    boxA = False
    boxB = False
    boxC = False
    boxD = False
    
    for box in boxesArray:
        box = box.strip()
        if box == 'start':
            startGear = True
        if box == 'paddle':
            paddleBag = True
        if box == 'bike':
            bikeBox = True
        if box == 'A':
            boxA = True
        if box == 'B':
            boxB = True
        if box == 'C':
            boxC = True
        if box == 'D':
            boxD = True

    
    self.startGear = startGear
    self.paddleBag = paddleBag
    self.bikeBox = bikeBox
    self.boxA = boxA
    self.boxB = boxB
    self.boxC = boxC
    self.boxD = boxD
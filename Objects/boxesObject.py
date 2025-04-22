class Box:
    def __init__(self, boxes):
        self.boxesArray = [b.strip() for b in boxes.split(",")] if isinstance(boxes, str) else []

        box_set = {box.strip() for box in self.boxesArray}

        self.hasStartGear = "start" in box_set
        self.hasPaddleBag = "paddle" in box_set
        self.hasBikeBox = "bike" in box_set
        self.hasBoxA = "A" in box_set
        self.hasBoxB = "B" in box_set
        self.hasBoxC = "C" in box_set
        self.hasBoxD = "D" in box_set
        
        self.startGear = []
        self.paddleBag = []
        self.bikeBox = []
        self.boxA = []
        self.boxB = []
        self.boxC = []
        self.boxD = []


    def __repr__(self):
        return f"Box({', '.join(self.boxesArray)})"
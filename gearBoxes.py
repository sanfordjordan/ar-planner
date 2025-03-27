from typing import List
from Objects.boxesObject import Box
from Objects.clothingObject import Clothing
from Objects.legObject import Leg

def calcBoxes(legs: List[Leg]) -> list:
    startGear, paddleBag, bikeBox, boxA, boxB, boxC, boxD = [[] for _ in range(7)]
    boxes = Box('')
    for leg in legs:
        gear = leg.gear# + leg.clothing
        if leg.boxes.hasStartGear: boxes.startGear.append(gear)
        if leg.boxes.hasBoxA: boxes.boxA.append(gear)
        if leg.boxes.hasBoxB: boxes.boxB.append(gear)
        if leg.boxes.hasBoxC: boxes.boxC.append(gear)
        if leg.boxes.hasBoxD: boxes.boxD.append(gear)
        if leg.boxes.hasBikeBox: boxes.bikeBox.append(gear)
        if leg.boxes.hasPaddleBag: boxes.paddleBag.append(gear)
    print(boxes.boxA)
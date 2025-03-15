from Objects.legObject import Leg
from Objects.userObject import User


def appendWaterNeeded(leg: Leg, user: User, waterFromFood: float):
    """Calculates the amount of water needed (in liters) for a given leg."""

    # Calculate heat level (minimum value is 1)
    heatLevel = max(leg.avgTemp / 10, 1)
    # Calculate water requirement
    waterNeeded = ((400 + user.sweatLevel * 75 + heatLevel * 75) * leg.avgTime - waterFromFood)  / 1000
    leg.waterReq = round(waterNeeded, 2)
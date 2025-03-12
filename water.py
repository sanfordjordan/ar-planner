from Objects.legObject import Leg


def appendWaterNeeded(leg: Leg, sweatLevel: int):
    """Calculates the amount of water needed (in liters) for a given leg."""

    # Calculate heat level (minimum value is 1)
    heatLevel = max(leg.avgTemp / 10, 1)

    # Calculate water requirement
    waterNeeded = (400 + sweatLevel * 75 + heatLevel * 75) * leg.avgTime  / 1000
    leg.waterReq = round(waterNeeded, 2)
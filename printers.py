from typing import List
from Objects.legObject import Leg

def printWaterRequirements(inputData: List[Leg]):
    total_water = sum(leg.waterReq for leg in inputData)

    print("\n" + "=" * 60)
    print(f"{'Leg':<5} | {'Discipline':<12} | {'Avg Temp (°C)':<14} | {'Avg Time (hrs)':<16} | {'Water Req (L)':<12}")
    print("-" * 60)

    for index, leg in enumerate(inputData, start=1):
        print(f"{index:<5} | {leg.discipline:<12} | {leg.avgTemp:<14.1f} | {leg.avgTime:<16.2f} | {leg.waterReq:<12.2f}")

    print("-" * 60)
    print(f"{'Total':<35} | {'':<16} | {total_water:<12.2f}")
    print("=" * 60 + "\n")

def printLegDetails(inputData: List[Leg]):
    leg_counter = 0  # Track actual legs (excluding TA's)

    for leg in inputData:
        isTA = (leg.discipline == "TA")

        if isTA:
            print(f"  TA Duration: {str(leg.finishTime - leg.startTime)}")
        else:
            leg_counter += 1
            print(f"Leg {leg_counter}: {leg.discipline}")
            print(f"  Start Time:  {leg.startTime.strftime('%A')} {leg.startTime.strftime('%H:%M')}")
            print(f"  Finish Time: {leg.finishTime.strftime('%A')} {leg.finishTime.strftime('%H:%M')}")
            print(f"  Duration:    {leg.avgTime:.2f} hours")
   

        print("-" * 40)
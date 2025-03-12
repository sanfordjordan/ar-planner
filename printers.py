from typing import List
from Objects.legObject import Leg

def printWaterRequirements(inputData: List[Leg]):
    print("\n" + "="*50)
    print(f"{'Leg':<5} | {'Discipline':<10} | {'Avg Temp (°C)':<12} | {'Avg Time (hrs)':<14} | {'Water Req (L)':<12}")
    print("-"*50)

    for index, leg in enumerate(inputData, start=1):
        print(f"{index:<5} | {leg.discipline:<10} | {leg.avgTemp:<12.1f} | {leg.avgTime:<14.2f} | {leg.waterReq:<12.2f}")

    print("="*50 + "\n")

def printLegDetails(inputData: List[Leg]):
    for i, leg in enumerate(inputData):
        leg_number = i + 1
        discipline = leg.discipline
        start_time = leg.startTime
        finish_time = leg.finishTime
        duration = leg.avgTime

        print(f"Leg {leg_number}: {discipline}")
        print(f"  Start Time:  {start_time.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Finish Time: {finish_time.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Duration:    {str(duration)}")

    
        if i < len(inputData) - 1:
            next_leg = inputData[i + 1]
            ta_time = next_leg.startTime - finish_time
            print(f"  TA Time:     {str(ta_time)}")
        
        print("-" * 40)
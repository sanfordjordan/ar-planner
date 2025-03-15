from datetime import datetime, timedelta
from typing import List, Tuple
from Objects.legObject import Leg
from timeUtils import getSleepTimes

def appendNoDoze(legs: List[Leg]):
    noDozSchedule = determineNoDozSchedule(legs)
    noDozePerLeg = getNoDozDuringLegs(noDozSchedule, legs)
    assignNoDozToLegs(noDozePerLeg, legs)

def determineNoDozSchedule(legs: List[Leg]):
    no_doz_times = []
    last_dose_time = None  # To track when the last No-Doz was taken
    current_time = legs[0].startTime 
    end_time = legs[-1].finishTime
    sleep_times = getSleepTimes(legs)
    
    # Iterate through the entire race duration, hour by hour
    while current_time <= end_time:
       # 1. Skip if it's still the same date as the race start date
        if current_time.date() == legs[0].startTime.date():
            current_time += timedelta(hours=1)
            continue
        
        # 2. Only proceed if the current time is between 10pm and 7am
        if not (current_time.hour >= 22 or current_time.hour < 8):
            current_time += timedelta(hours=1)
            continue
        
        # 3. Skip if the current time falls within any sleep period
        if any(sleep_start <= current_time < sleep_end for sleep_start, sleep_end in sleep_times):
            current_time += timedelta(hours=1)
            continue
        
        # 4. Skip if sleep is planned within the next 6 hours
        if any( timedelta(hours=0) < sleep_start - current_time <= timedelta(hours=6) for sleep_start, _ in sleep_times):
            current_time += timedelta(hours=1)
            continue
        
        # 5. Ensure 3 hours have passed since the last dose
        if last_dose_time is None or (current_time - last_dose_time >= timedelta(hours=3)):
            no_doz_times.append(current_time)
            last_dose_time = current_time

        current_time += timedelta(hours=1)
    
    return no_doz_times

def getNoDozDuringLegs(no_doz_times: List[datetime], legs: List[Leg]) -> List[Tuple[str, int]]:
    no_doz_per_leg = [] 
    inTA = 0 

    for leg in legs:
        no_doz_count = sum(1 for no_doz_time in no_doz_times if leg.startTime <= no_doz_time < leg.finishTime)
        
        if leg.discipline == 'TA':
            inTA = no_doz_count  # Save No-Doz count to move to the next leg
        else:
            no_doz_per_leg.append((leg.number, no_doz_count + inTA))
            inTA = 0
    
    return no_doz_per_leg

def assignNoDozToLegs(no_doz_times: List[datetime], legs: List[Leg]) -> None:
    # Loop through each leg and match it with the No-Doz data
    for leg in legs:
        for index, no_doz_count in no_doz_times:
            if leg.number == index and leg.discipline != 'TA':
                leg.food.append(('No-Doz', no_doz_count))
                break  # Break the loop once we have added the No-Doz to the food array
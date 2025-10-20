from datetime import datetime, timedelta, time
from typing import List

from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo

def appendTimes(legs: List[Leg], raceInfo: RaceInfo):
    prevSleptNight = None
    prevLeg = None
    nextLeg = None
    sleepDuring = False
    raceStart = raceInfo.startDateTime

    for index, leg in enumerate(legs):
        if index > 0: prevLeg = legs[index - 1]
        if index < len(legs)-1: nextLeg = legs[index + 1]
        if  leg.discipline == 'TA':
            currentStart, currentFinish, prevSleptNight, sleepDuring = calcTATime(prevLeg, nextLeg, prevSleptNight, raceStart)
        else:
            if prevLeg is None: currentStart = raceStart
            else: currentStart = prevLeg.finishTime
            currentFinish = currentStart + leg.avgTime

        leg.startTime = currentStart
        leg.finishTime = currentFinish
        leg.sleepDuring = sleepDuring
        sleepDuring = False
    raceInfo.finishDateTime = legs[-1].finishTime

def calcTATime(prevLeg: Leg, nextLeg: Leg, prevSleptNight: datetime, raceStart: datetime) -> tuple[datetime, datetime, datetime]:
    """Calculates start and finish time for a TA leg, handling sleep and transition times."""
    lastDiscipline = prevLeg.discipline
    currentDiscipline = nextLeg.discipline
    currentStart = prevLeg.finishTime
    sleepDuring = False

    taTime = timedelta(minutes=10)
    if lastDiscipline == 'Kayak': taTime += timedelta(minutes=10)
    if lastDiscipline == 'Bike': taTime += timedelta(minutes=6)
    if currentDiscipline == 'Kayak': taTime += timedelta(minutes=8)
    if currentDiscipline == 'Bike': taTime += timedelta(minutes=6)

    
    sleep = timedelta(0)  # Default: no sleep

 # Sleep logic - only starts on the **second night**
    finish_date = prevLeg.finishTime.date()
    
    second_race_night =  raceStart.date() + timedelta(days=2)  # Sleep can only start on this night

    if finish_date >= second_race_night and finish_date != prevSleptNight:
        # Calculate when the next leg finishes
        next_leg_time = (nextLeg.shortTime + nextLeg.longTime) / 2
        next_leg_finish = (prevLeg.finishTime + taTime + next_leg_time).time()

        # Sleep now if:
        # 1. The next leg is **too long** (won't finish before the next night).
        # 2. The next leg **won't get us closer to 5 AM**.
        if next_leg_finish > datetime.strptime("05:00", "%H:%M").time() or next_leg_time > timedelta(hours=8):
            sleep = timedelta(hours=3)
            prevSleptNight = finish_date  # Mark sleep for this night
            sleepDuring = True

    currentFinish = currentStart + taTime + sleep
    return currentStart, currentFinish, prevSleptNight, sleepDuring

def getSleepTimes(legs: List[Leg]) -> list:
    sleep_times = []
    
    for leg in legs:
        if leg.sleepDuring:  # If sleep is scheduled during the leg
            sleep_end = leg.finishTime  # The finish time is the sleep end time
            sleep_start = sleep_end - timedelta(hours=3)  # Subtract 3 hours to get the start time
            sleep_times.append((sleep_start, sleep_end))  # Append the sleep period to the list
    
    return sleep_times
from datetime import datetime, timedelta
from typing import List

from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo

def appendTimes(inputData: List[Leg], raceInfo: RaceInfo) -> List[Leg]:
    prevSleptNight = None
    prevLeg = None
    nextLeg = None
    raceStart = raceInfo.startDateTime

    for index, leg in enumerate(inputData):
        if index > 0: prevLeg = inputData[index - 1]
        if index < len(inputData)-1: nextLeg = inputData[index + 1]
        if  leg.discipline == 'TA':
            currentStart, currentFinish, prevSleptNight = calcTATime(prevLeg, nextLeg, prevSleptNight, raceStart)
        else:
            currentStart, currentFinish = calcTime(prevLeg, leg, raceStart)

        leg.startTime = currentStart
        leg.finishTime = currentFinish
        leg.avgTime = (currentFinish - currentStart).total_seconds() / 3600  # Convert to hours

    return inputData

def parse_time_string(time_str: str) -> timedelta:
    """Converts a 'hh:mm' string into a timedelta object."""
    hours, minutes = map(int, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes)

def calcTATime(prevLeg: Leg, nextLeg: Leg, prevSleptNight: datetime, raceStart: datetime) -> tuple[datetime, datetime, datetime]:
    """Calculates start and finish time for a TA leg, handling sleep and transition times."""
    lastDiscipline = prevLeg.discipline
    currentDiscipline = nextLeg.discipline
    currentStart = prevLeg.finishTime

    taTime = timedelta(minutes=10)
    if lastDiscipline == 'Kayak': taTime += timedelta(minutes=10)
    if lastDiscipline == 'Bike': taTime += timedelta(minutes=6)
    if currentDiscipline == 'Kayak': taTime += timedelta(minutes=8)
    if currentDiscipline == 'Bike': taTime += timedelta(minutes=6)

    
    sleep = timedelta(0)  # Default: no sleep

 # Sleep logic - only starts on the **second night**
    finish_date = prevLeg.finishTime.date()
    finish_time = prevLeg.finishTime.time()
    
    second_race_night =  raceStart.date() + timedelta(days=2)  # Sleep can only start on this night

    if finish_date >= second_race_night and finish_date != prevSleptNight:
        # Calculate when the next leg finishes
        next_leg_time = (parse_time_string(nextLeg.shortTime) + parse_time_string(nextLeg.longTime)) / 2
        next_leg_finish = (prevLeg.finishTime + taTime + next_leg_time).time()

        # Sleep now if:
        # 1. The next leg is **too long** (won't finish before the next night).
        # 2. The next leg **won't get us closer to 5 AM**.
        if next_leg_finish > datetime.strptime("05:00", "%H:%M").time() or next_leg_time > timedelta(hours=8):
            sleep = timedelta(hours=3)
            prevSleptNight = finish_date  # Mark sleep for this night

    currentFinish = currentStart + taTime + sleep
    return currentStart, currentFinish, prevSleptNight

def calcTime(prevLeg: Leg, currentLeg: Leg, startDateTime: datetime) -> tuple[datetime, datetime]:
    """Calculate start and finish times for a moving leg."""
    if prevLeg is None:
        currentStart = startDateTime
    else:
        currentStart = prevLeg.finishTime

    # Calculate leg duration
    shortTime = parse_time_string(currentLeg.shortTime)
    longTime = parse_time_string(currentLeg.longTime)
    currentLegTimeEst = shortTime + (longTime - shortTime) / 2
    currentFinish = currentStart + currentLegTimeEst

    return currentStart, currentFinish
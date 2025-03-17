from datetime import datetime, timedelta, time
from typing import List

from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo

def appendTimes(inputData: List[Leg], raceInfo: RaceInfo):
    prevSleptNight = None
    prevLeg = None
    nextLeg = None
    sleepDuring = False
    raceStart = raceInfo.startDateTime

    for index, leg in enumerate(inputData):
        if index > 0: prevLeg = inputData[index - 1]
        if index < len(inputData)-1: nextLeg = inputData[index + 1]
        if  leg.discipline == 'TA':
            currentStart, currentFinish, prevSleptNight, sleepDuring = calcTATime(prevLeg, nextLeg, prevSleptNight, raceStart)
        else:
            currentStart, currentFinish = calcTime(prevLeg, leg, raceStart)

        leg.startTime = currentStart
        leg.finishTime = currentFinish
        leg.avgTime = (currentFinish - currentStart).total_seconds() / 3600  # Convert to hours
        leg.sleepDuring = sleepDuring
        sleepDuring = False
    raceInfo.finishDateTime = inputData[-1].finishTime

def parse_time_string(time_str: str) -> timedelta:
    """Converts a 'hh:mm' string into a timedelta object."""
    hours, minutes = map(int, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes)

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
        next_leg_time = (parse_time_string(nextLeg.shortTime) + parse_time_string(nextLeg.longTime)) / 2
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

#This method might be wrong idk
def doesLegIntersectTimeRange(leg, start_hour, end_hour):
    """Check if a leg's time range intersects with a given time window, even across multiple days."""
    leg_start = leg.startTime
    leg_end = leg.finishTime

    # If the leg spans multiple days, it MUST intersect some time window
    if (leg_end - leg_start).days >= 1:
        return True

    # Convert times into absolute timestamps
    leg_date = leg_start.date()
    range_start = datetime.combine(leg_date, time(start_hour, 0))
    range_end = datetime.combine(leg_date, time(end_hour, 0))

    if start_hour < end_hour:
        # Case 1: Time range does NOT cross midnight (e.g., 10:00 - 18:00)
        return leg_start < range_end and leg_end > range_start

    else:
        # Case 2: Time range CROSSES midnight (e.g., 22:00 - 07:00)
        next_day = leg_date + timedelta(days=1)
        range_end_next_day = datetime.combine(next_day, time(end_hour, 0))

        return (leg_start.time() >= time(start_hour, 0) or leg_start.time() < time(end_hour, 0)) or \
               (leg_end.time() >= time(start_hour, 0) or leg_end.time() < time(end_hour, 0)) or \
               (leg_start < range_end_next_day and leg_end > range_start)

def getSleepTimes(legs: List[Leg]) -> list:
    sleep_times = []
    
    for leg in legs:
        if leg.sleepDuring:  # If sleep is scheduled during the leg
            sleep_end = leg.finishTime  # The finish time is the sleep end time
            sleep_start = sleep_end - timedelta(hours=3)  # Subtract 3 hours to get the start time
            sleep_times.append((sleep_start, sleep_end))  # Append the sleep period to the list
    
    return sleep_times
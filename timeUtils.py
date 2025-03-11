from datetime import datetime, timedelta

def parse_time_string(time_str):
    """Converts a 'hh:mm' string into a timedelta object."""
    hours, minutes = map(int, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes)

def calcTime(prevLeg, currentLeg, startDateTime, prevSleptNight=None):
    """Calculate start and finish times for a race leg, ensuring 3-hour sleep every night except the first."""
    currentDiscipline = currentLeg.discipline
    sleep = timedelta(minutes=0)  # Default: no sleep
    currentStart = startDateTime

    if prevLeg != 'NA': 
        taTime = timedelta(minutes=10)  # Default transition time

        lastDiscipline = prevLeg.discipline
        if lastDiscipline == 'Kayak': taTime += timedelta(minutes=10)
        if lastDiscipline == 'Bike': taTime += timedelta(minutes=6)
        if currentDiscipline == 'Kayak': taTime += timedelta(minutes=8)
        if currentDiscipline == 'Bike': taTime += timedelta(minutes=6)

        # Check if a sleep should be added
        finish_date = prevLeg.finishTime.date()
        finish_time = prevLeg.finishTime.time()

        if finish_date != prevSleptNight:  # Ensure only one sleep per night
            if finish_time >= datetime.strptime("21:00", "%H:%M").time():  # After 9 PM
                sleep_start = prevLeg.finishTime
            elif finish_time < datetime.strptime("05:00", "%H:%M").time():  # Before 5 AM
                sleep_start = prevLeg.finishTime
            else:
                sleep_start = prevLeg.finishTime  # Edge case (not really needed)

            # Ensure sleep starts as close to 5 AM as possible
            if sleep_start.time() < datetime.strptime("02:00", "%H:%M").time():
                sleep_start = sleep_start.replace(hour=2, minute=0)
            elif sleep_start.time() > datetime.strptime("05:00", "%H:%M").time():
                sleep_start = sleep_start.replace(hour=5, minute=0)

            sleep = timedelta(hours=3)
            prevSleptNight = finish_date  # Update last slept night

        currentStart = prevLeg.finishTime + taTime + sleep

    shortTime = parse_time_string(currentLeg.shortTime)
    longTime = parse_time_string(currentLeg.longTime)
    currentLegTimeEst = shortTime + (longTime - shortTime) / 2
    currentFinish = currentStart + currentLegTimeEst
    didSleep = sleep > timedelta(0)
    return currentStart, currentFinish, prevSleptNight, didSleep

def printLegDetails(inputData):
    for i, leg in enumerate(inputData):
        leg_number = i + 1
        discipline = leg.discipline
        start_time = leg.startTime
        finish_time = leg.finishTime
        duration = finish_time - start_time

        print(f"Leg {leg_number}: {discipline}")
        print(f"  Start Time:  {start_time.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Finish Time: {finish_time.strftime('%d/%m/%Y %H:%M')}")
        print(f"  Duration:    {str(duration)}")

    
        if i < len(inputData) - 1:
            next_leg = inputData[i + 1]
            ta_time = next_leg.startTime - finish_time
            print(f"  TA Time:     {str(ta_time)}")
        
        print("-" * 40)
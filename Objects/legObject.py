from datetime import datetime, timedelta
from Objects.boxesObject import Box


class Leg:
  def __init__(self, legStuff):
    self.number = legStuff[0]
    self.discipline = legStuff[1]
    self.shortTime = legStuff[2]
    self.longTime = legStuff[3]
    self.elevation = int(legStuff[4])
    self.rapids = legStuff[6]
    self.minTemp = 10
    self.maxTemp = 20
    self.startTime = datetime(2001, 6, 19, 0, 0)
    self.finishTime = datetime(2001, 6, 19, 0, 0)
    self.avgTime =  timedelta(minutes=0)
    self.avgTemp = 20
    self.waterReq = 0
    self.sleepDuring = False
    self.food = []
    self.spareSJ = 0
    self.weather = None
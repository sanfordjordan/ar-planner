from boxesObject import Box


class Leg:
  def __init__(self, legStuff):
    self.number = legStuff[0]
    self.discipline = legStuff[1]
    self.shortTime = legStuff[2]
    self.longTime = legStuff[3]
    self.elevation = int(legStuff[4])
    makeBoxObj = Box(legStuff[5])
    self.rapids = legStuff[6]
    self.minTemp = 10
    self.maxTemp = 20
    self.startTime = 0
    self.finishTime = 0
    self.sleepBefore = False

    self.boxes = makeBoxObj


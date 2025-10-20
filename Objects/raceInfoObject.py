from datetime import datetime

class RaceInfo:
  def __init__(self, line):
    latitude, longitude = line[2].split(',')
    self.startDateTime = datetime.strptime(f"{line[1]} {line[0]}", "%d/%m/%Y %H:%M")
    self.finishDateTime = None
    self.latitude = latitude
    self.longitude = longitude




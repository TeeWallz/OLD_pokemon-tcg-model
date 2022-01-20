from dataclasses import dataclass
import datetime

@dataclass
class Set:
  id: str
  series: str
  printedTotal: int
  total: int
  ptcgoCode: str
  releaseDate : datetime.date
  updatedAt: datetime.datetime
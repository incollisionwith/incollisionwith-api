from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .police_force import *
from .accident_severity import *
from .vehicle_type import *
from .towing_and_articulation import *
from .accident import *
from .vehicle import *
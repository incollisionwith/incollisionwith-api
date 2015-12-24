from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .age_band import *
from .police_force import *
from .casualty_class import *
from .junction_control import *
from .junction_detail import *
from .junction_location import *
from .casualty_severity import *
from .sex import *
from .vehicle_type import *
from .towing_and_articulation import *
from .vehicle_location import *
from .vehicle_manoeuvre import *
from .pedestrian_location import *
from .pedestrian_movement import *
from .accident import *
from .vehicle import *
from .casualty import *

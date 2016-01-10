from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .reference import *

from .police_force import *

from .accident import *
from .vehicle import *
from .casualty import *
from .citation import *
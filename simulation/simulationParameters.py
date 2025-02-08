import vector

__all__ = ['TOP',
           'LEFT',
           'SCREEN_WIDTH',
           'SCREEN_HEIGHT',
           'PERCEPTION_DISTANCE',
           'SEPARATION_DISTANCE',
           'DIRECTION_GAIN',
           'COHESION_GAIN',
           'SEPARATION_GAIN',
           'NUM_ENTITIES',
           'MAX_SPEED']

TOP = vector.obj(x = 0, y = 1)
LEFT = vector.obj(x = 1, y = 0)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PERCEPTION_DISTANCE = 100
SEPARATION_DISTANCE = 75
DIRECTION_GAIN = 0.02
COHESION_GAIN = 0.003
SEPARATION_GAIN = 0.0035
NUM_ENTITIES = 100
MAX_SPEED = 4
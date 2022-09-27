from src.Point import Point
from src.Polygon import Polygon

class Curve(Polygon):
    def __init__(self, *v: Point):
        assert len(v) > 1
        super().__init__(*v)
        
    def lerp(self, t):
        pass
    
    def draw(self):
        pass
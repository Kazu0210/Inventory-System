from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

class AddGraphics:
    def __init__(self):
        pass
    
    def shadow_effect(self, widget, **kwargs):
        """Shadow effects"""

        blur = kwargs.get('blur', 10)
        offsetX = kwargs.get('x', 0)
        offsetY = kwargs.get('y', 0)
        r = kwargs.get('r', 0)
        g = kwargs.get('g', 0)
        b = kwargs.get('b', 0)
        alpha = kwargs.get('alpha', 255)

        shadow_fx = QGraphicsDropShadowEffect()
        shadow_fx.setBlurRadius(blur)
        shadow_fx.setColor(QColor(r, g, b, alpha))
        shadow_fx.setOffset(offsetX, offsetY)

        widget.setGraphicsEffect(shadow_fx)
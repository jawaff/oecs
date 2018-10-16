import sfml as sf

class Component(object):
    def __init__(self, sComponentName, bUpdatable, iDrawableType):
        #This is here to adapt to the dictionary of components within the Entity instances.
        #This name will be used as the Key for this component.
        self._sName = sComponentName
        self._bUpdatable = bUpdatable

        #This integer can be either
        #   0, 1, or 2.
        #   0 - Not Drawable
        #   1 - Screen Drawable
        #   2 - View Drawable
        self._iDrawableType = iDrawableType

    def get_name(self):
        """This is primarily used for letting the Entity class determine
        the key for the component instance"""
        return self._sName

    def get_updatable(self):
        """For checking to see if this component is updatable."""
        return self._bUpdatable

    def set_updatable(self, bUpdatable):
        """For the entities that need to change updatable ability."""
        self._bUpdatable = bUpdatable

    def is_view_drawable(self):
        """For checking to see if this component is drawable."""
        return (self._iDrawableType == 2)

    def is_screen_drawable(self):
        """For checking to see if this component is drawable."""
        return (self._iDrawableType == 1)

    def set_drawable(self, iDrawableType):
        """For the entities that need to change drawable ability."""
        self._iDrawableType = iDrawableType

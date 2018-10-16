import component
import config

class Entity(object):
    def __init__(self, sEntityName, sEntityType, iDrawPriority, dAttribs):
        #The id is mostly for debugging purposes.
        self._sName = sEntityName
        self._sType = sEntityType

        self._iDrawPriority = iDrawPriority

        #All entities are uncollidable until they added into a Collision_Space.
        self._bCollidable = False

        #componentName:component
        #Drawable components that are in the dComponents dictionary will have a pointer to them in this list.
        self._dComponents = {}

        #These drawable components will be drawn with respect to the
        #   view of the game.
        self._lViewDrawables = []
        
        #These drawable components will be drawn with respect to the
        #   screen, the view is independent.
        self._lScreenDrawables = []

        #Updatable components that hold pointer variables that point to the updatable components in the dComponents dictionary.
        self._lUpdatables = []

        self._bExpired = False

        for key in list(dAttribs.keys()):
            self.add_component(dAttribs.pop(key))


    def add_component(self, componentInstance):
        """This takes in an instance of a class that inherits from the Component class
        and then it adds that instance into the list of components for this particular entity."""

        #print "Componet being added to %s entity."%(self._sName)
        #print componentInstance
        
        self._dComponents[componentInstance.get_name()] = componentInstance

        #These if statements will save a pointer of the same variable as in dComponents if True.

        if componentInstance.get_updateable():
            self._lUpdatables.append(componentInstance)

        if componentInstance.is_view_drawable():
            self._lViewDrawables.append(componentInstance)

        elif componentInstance.is_screen_drawable():
            self._lScreenDrawables.append(componentInstance)


    def remove_component(self, sCompName):
        """This searches through our list of components for the component with
        the specified ID and then removes it from the list."""
        del self._dComponents[sCompName]

    def __len__(self):
        return len(self._dComponents)

    def set_collidable(self, bCollidable):
        """This is for making the Entity update its position over time
        based on where the physics shapes are.
        @param bCollidable A boolean that says whether this entity
            uses physics or not."""

        self._bCollidable = bCollidable

    def get_draw_priority(self):
        return self._iDrawPriority
    
    def get_name(self):
        """This is for accessing the names of the entities."""
        return self._sName

    def get_type(self):
        """This is essential information needed to locate the entity within the Entity_Manager's entity dictionary."""
        return self._sType

    def get_component(self, sCompName):
        """This will return the instance of a component that contains
        the specified ID."""
        return self._dComponents.get(sCompName, None)

    def get_all_components(self, sSubName):
        """This is meant for getting all components that contain a certain string at the beginning of their name.
        @return a list of components that have part of the string that was given in their name.
        @param sSubName This is the string that will be looked for within the components."""

        lComponents = []

        for (sCompName, component) in list(self._dComponents.items()):

            if sCompName.startswith(sSubName):

                lComponents.append(component)

        return lComponents

    def remove_all_components(self, sSubName):
        """This is meant for removing all components that contain a certain string at the beginning of their name.
        @param sSubName This is the string that will be looked for within the components."""

        for (sCompName, component) in list(self._dComponents.items()):

            if sCompName.startswith(sSubName):

                self._dComponents.pop(sCompName)


    def _update_collidable_components(self):
        """This is meant to update the position of a component
        based on the collision shape that is connected to. The collision shape
        is merely a representation of a component in a physics environment.
        @post The position of some components will be altered based on the position
            of its connect collision shape."""

        #First we must iterate through each collision shape component.
        for cBody in self.get_all_components("CBODY"):

            #Then for each collison shape, we must grab its position and
            #   update the dependent component of the collision shape.

            #The y position needs flipped because pymunk and sfml's y coordinates start
            #   on different sides (top-left is (0,0) in sfml, bottom-left is (0,0) in pymunk)
            lPosition = [cBody._Get_Body().position[0],   \
                        config.WINDOW_HEIGHT - cBody._Get_Body().position[1]]

            dependentSprite = self.get_component(cBody._Get_Dependent_Component_ID())

            if (dependentSprite):
                dependentSprite._Update_Position(lPosition, cBody._Get_Body().angle)
        

    def update(self, timeElapsed):
        """This will update the updatable components within the dComponents dictionary by indirectly updating the pointer variables within lUpdatables."""

        for i in range(len(self._lUpdatables)):

            #This calls the Updatable component's update() method.
            self._lUpdatables[i].update(timeElapsed)

    def render(self, renderWindow, windowView):
        """This will render the drawable components within the dCOmponents dictionary by indirectly rendering the pointer variables within lDrawables."""

        #Before rendering, we need to see if this entity exists within a COllision Space.
        if self._bCollidable: 

            #print "%s:%s entity needs its components updated for rendering"%(self.get_type(),self.get_name())

            #If the entity does exist in the colllision space, then we need to update
            #   the position of its components with respect to the Collision SHape positions

            self._update_collidable_components()

        #print "These are the drawable components that are being drawn."
        #print self._lViewDrawables
        #print self._lScreenDrawables

        renderWindow.view = windowView
        
        for i in range(len(self._lViewDrawables)):

            #This calls the Drawable component's render() method.
            self._lViewDrawables[i].render(renderWindow)

        renderWindow.view = renderWindow.default_view

        for i in range(len(self._lScreenDrawables)):

            #This calls the Drawable component's render() method.
            self._lScreenDrawables[i].render(renderWindow)

    def set_expired(self, bExpired):
        """This is for signaling an entity to be removed from the Entity_Manager's dictionary of entities."""
        self._bExpired = bExpired

    def is_expired(self):
        """This is for checking to see if we should delete the entity or not."""
        return self._bExpired

    def on_expire(self):
        """This is what is to be done when the entity is removed. It's almost like a destructor.
        I don't know what to use it for though. Maybe for removing system functions that are associated with this entity.
        That would require the entity to store something that will tell us the associated system functions."""
        pass



        


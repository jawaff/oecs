import oecs.priority_queue

class EntityManager(object):
    def __init__(self):
        #This allows access to specific entities
        #sEntityType:(sEntityName:entity)
        self._dEntities = {}

        #This orders the entities so that the ones with the highest draw
        #   priority will be first in the list (highest priority is 0.)
        self._pqDrawableEntities = priority_queue.PriorityQueue()

    def empty_entity_containers(self):
        """This is for cleaning up the Entity Containers for when we need to change
        the buttons for the next state."""\
		
        self._dEntities.clear()

        self._pqDrawableEntities.clear()

    def add_entity(self, entity):
        """This will add entities into our dictionary of lists of entities.
        And it will also add the Entity to the PriorityQueue so that it can be drawn.
        @param entity This should be an actual instance of the Entity class. So it
            holds components and that's about it.
        @param iPriority This is the draw priority for the Entity that it being
            added. Zero is the highest draw priority (gets drawn first,) -1 means
            the Entity doesn't need added to the PriorityQueue."""

        if self._dEntities.get(entity.get_type(), None) == None:
            #If there wasn't already a dictionary, then we'll make one
            self._dEntities[entity.get_type()] = {}

        #This will overwrite or create a new entity of the given name.
        self._dEntities[entity.get_type()][entity.get_name()] = entity

        #THis filters out the entities with -1 priorities to being added
        #   To the list of drawable Entities.
        if (entity.get_draw_priority() != -1):
            self._pqDrawableEntities.add_entity(entity)

        

    def remove_entity(self, sEntityTypeName, sEntityName):
        """When an entity expires it will be removed with this."""
        #This just prevents errors from occuring in the dictionary accessing.
        if self._dEntities.get(sEntityTypeName,None) != None:
            self._dEntities[sEntityTypeName].pop(sEntityName)

        #Entities that aren't within the priority queue will be ignored.
        self._pqDrawableEntities.remove_entity(entity.get_name(), entity.get_type())

    def get_entity(self, sEntityTypeName, sEntityName):
        """This is for retrieving entities from the dictionary. It so far
        is only used for the System functions in the ChangeState() function."""

        if self._dEntities.get(sEntityTypeName,None) != None    \
           and self._dEntities[sEntityTypeName].get(sEntityName,None) != None:

            return self._dEntities[sEntityTypeName][sEntityName]

        #If the entity wasn't found, we'll look for it within the
        #   containers of entities.
        elif self._dEntities.get("EntityManager") != None:

            for key in list(self._dEntities["EntityManager"].keys()):

                tmp = self._dEntities["EntityManager"][key].get_entity(sEntityTypeName, sEntityName)

                #This checks to see if the entity was in that container
                if tmp != None:

                    return tmp

        #If the entity still wasn't found, then it doesn't exist at this point in time
        else:
            print("EntityType: %s, EntityName: %s doesn't exist in the EntityManager's container of entities!" % (sEntityTypeName, sEntityName))

        return None

    def _Call_System_Func(self, sSystemFuncName, lEntities):
        """This will call a system function from the systems.py file. And it will provide the appropriate entities that are needed to be passed to the function.
        This will also return a variable from the system function.
        @param sSystemFuncName This is the name of the System function that is to be called.
        @param lEntities This is a list of tuples containing information on the entities
            that will have to be passed to the system function that is to be called. This allows
            systems to act upon entities, so the components can be changed."""

        #If one entity to pass to the systemFunc
        #lEntities == [(sEntityType, sEntityName, sComponentName)]
        #If two entities to pass to the systemFunc
        #lEntities == [(sEntityType, sEntityName, sComponentName),(sEntityType, sEntityName, sComponentName)]
        
        module = importlib.import_module('systems')
        systemFunc = getattr(module, sSystemFuncName)

        #I'm sure that this is suppose to be an empty list
        if lEntities == []:

            return systemFunc({})

        else:
            #sComponentName:entityInstance
            dEntities = {}

            for indx in range(len(lEntities)):

                #This grabs the entity and stores it into the new dictionary we just made
                dEntities[lEntities[indx][2]] = self.get_entity(lEntities[indx][0], lEntities[indx][1])

            #print sSystemFuncName + " is being executed."

            return systemFunc(dEntities)        

    def input_update(self):
        """This will essentially execute all of the system functions that it is told to by the InputManager. And it will return the new lNextState variable, which
        should be ["NULL","NULL"] if a state change isn't needed."""

        #Loop through all of the inputs that are active according to the InputManager class
        for (sSystemFuncName, lEntities) in InputManager.get_active_inputs():

            sNextState = self._Call_System_Func(sSystemFuncName, lEntities)

            #print sNextState

            #Only strings are allowed to be returned from the system functions and only if the state needs to be changed.
            #Otherwise, we'll just keep calling system functions and eventually return something that makes no state change occur.
            if sNextState != "NULL,NULL":

                return sNextState.split(',')

        return ["NULL","NULL"]

    def logic_update(self, timeElapsed):
        """This method is simple, but important. It signals the Entities within our dictionary of entities to update themselves with only the timeElapsed as new data.
        NOTE: This may be able to be put into the Entity_Manager class instead of here."""

        #Before updating any of the entities, we need to call all of the active system functions (providing the associated entities as arguments.)

        for (sSystemFuncName, lEntities) in System_Manager.get_active_systems():
            #print sSystemFuncName + " system is being exectuted."
            
            sNextState = self._Call_System_Func(sSystemFuncName, lEntities)

            if sNextState != "NULL,NULL":

                return sNextState.split(',')
            

        #This block iterates through all of the entities in our dictionary of dictionaries and signals each to update itself.
        for (sEntityType, dEntities) in list(self._dEntities.items()):

            for (sEntityName, entity) in list(dEntities.items()):

                #Check to see if the Entity is expired
                if entity.is_expired():
                    entity.on_expire()
                    self.remove_entity(entity.get_type(), entity.get_name())

                entity.update(timeElapsed)

        return ["NULL","NULL"]


    def render_update(self, pWindow, pWindowView):
        #print "Render Update!"

        pWindow.clear(sf.Color.BLACK)

        #This will iterate through all of the Entities
        #   that exist within the PriorityQueue of
        #   drawable entities.
        for i in range(len(self._pqDrawableEntities)):
            self._pqDrawableEntities[i].render(pWindow, pWindowView)

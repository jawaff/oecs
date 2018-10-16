
class SystemManager(object):

    def __init__(self):
        self._action_systems = []
        self._state_systems = []

    def empty_systems():
        """This simply will empty the Systems that were signaled to be called."""
        del self._action_systems[:]
        del self._state_systems[:]

    def add_system(sType, sSystemFuncName, lEntities):
        """This will be for adding in various types of systems into the game. Systems will exist as more than just a single function.
        For the different types of systems, I'd like them to be handled differently. A state system for instance will have two functions associated with it.
        One function will be to activate continuously and the other one will activate once when the system is removed."""

        #print "systemFunction:%s"%(sSystemFuncName)

        if sType == 'action':
            self._action_systems.append((sSystemFuncName, lEntities))

        elif sType == 'state':
            self._state_systems.append((sSystemFuncName, lEntities))

    def remove_system(sSystemFuncName):
        """This will be for removing the systems that stay active until told otherwise (this is where we say otherwise.)
        Since the Actions systems will be removed once they are executed, they don't really play an importance here. But then
        again, those might need to be canceled."""
        
        for indx in range(len(self._state_systems)):
           if self._state_systems[indx][0] == sSystemFuncName:
                self._state_systems.pop(indx)
                break

        for indx in range(len(self._action_systems)):
            if self._action_systems[indx][0] == sSystemFuncName:
                self._action_systems.pop(indx)
                break

    def get_active_systems():
        """This will return the active systems. Removing the actions from there containers, while just getting copies of the states."""
        lSystems = self._action_systems + self._state_systems

        #print "The list of systems to be executed: "
        #print lSystems

        del self._action_systems[:]

        return lSystems
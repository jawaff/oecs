class OECS(object):
    def __init__(self, window, view, state_loader, entity_manager, system_manager, input_manager, asset_manager):
	    """
        @param window The SFML window object that the state is to be loaded onto.
        @param view This is SFML's View object and allows us to zoom in on the what would be shown in the window. This
            essentially just gives us the option to zoom in on the stuff visible for a certain state (can be specified in xml data.)
		@param state_loader The loader for loading the next state's entities, systems, inputs and assets.
        @param entity_manager This is for loading entities into the game based on the state being switched to.
		@param system_manager This is for manipulating the systems that are to be executed.
		@param input_manager This is for manipulating what inputs are listened for and how they interact with systems and entities.
		@param asset_manager This contains the assets that are to be used by SFML's renderer."""
		self._window = window
		self._view = view
		self._state_loader = state_loader
		self._entity_manager = entity_manager
		self._self._system_manager = system_manager
		self._input_manager = input_manager
		self._asset_manager = asset_manager
	    	
        self._last_key_press_timer = sf.Clock()
        #This will be False if the player clicks outside of the program's window and "pause" the program
        self._is_window_active = True
        self._is_quit = False
		
    def close(self):
	    self._window.close()
		
    def is_quit(self):
	    return self._is_quit
		
	def process_inputs(self):
        #This will loop through all of the events that have been triggered by player input
        for event in self._window.iter_events():

            if event.type == sf.Event.MOUSE_MOVED:
                self._input_manager.mouse_has_moved(self._window.convert_coords(event.x,event.y))

            #elif event.type == sf.Event.TEXT_ENTERED:
                #InputManager.key_input(event.unicode, True, self._last_key_press_timer.elapsed_time)

                #This restarts the Timer for the self._last_key_press_timer since a new key just
                #   got pressed.
                #self._last_key_press_timer.restart()
            
            elif event.type == sf.Event.KEY_PRESSED:
                self._input_manager.key_input(event.code, True, self._last_key_press_timer.elapsed_time)

                #This restarts the Timer for the self._last_key_press_timer since a new key just
                #   got pressed.
                self._last_key_press_timer.restart()
                
            elif event.type == sf.Event.KEY_RELEASED:
                #The time elapsed isn't necessary for the released key.
                self._input_manager.key_input(event.code)
            
            elif event.type == sf.Event.MOUSE_BUTTON_PRESSED:
                self._input_manager.mouse_input(event.button, True)
            
            elif event.type == sf.Event.MOUSE_BUTTON_RELEASED:
                self._input_manager.mouse_input(event.button,False)

            elif event.type == sf.Event.CLOSED:
                for stateIndx in range(len(lNextState)):                     
                    lNextState[stateIndx] = "QUIT"
                self._is_quit = True
                
            elif event.type == sf.Event.LOST_FOCUS:
                self._is_window_active = False

            elif event.type == sf.Event.GAINED_FOCUS:
                self._is_window_active = True
				
    def update_frame(self, time_change):
	    #This makes the program so that it basically pauses all of its game updates when a user clicks outside of the window. And it waits until the user clicks on the window.
        if self._is_window_active:
            #We don't want to change lNextState if the game has been set to QUIT
            if not self._is_quit:                
                #lNextState will contain "NULL"s when no state change is signaled
                #lNextState will have all of its elements change when switching to a new state.
                lNextState = self._entity_manager.input_update()

                #Check to see if we have signaled to quit the game thus far
                if lNextState[0] == "QUIT":
                    self._is_quit = True

                #If one of the lNextState elements is changed, they all are (just how it goes.)
                if lNextState[0] != "NULL" and lNextState[0] != "QUIT":
				    # TODO Change to self._state_loader.load_state()
                    ChangeState(lCurrentState, lNextState, window, view, entity_manager)

                #Finally after we've handled input and have correctly adjusted to the nextState (in most cases it won't happen,)
                #we can then update our game's model with stuff that will happen in the respective state with each game update.

                lNextState = self._entity_manager.logic_update(time_change)

                #Check to see if we have signaled to quit the game thus far
                if lNextState[0] == "QUIT":
                    self._is_quit = True

                #If one of the lNextState elements is changed, they all are (just how it goes.)
                if lNextState[0] != "NULL" and lNextState[0] != "QUIT":
				    # TODO Change to self._state_loader.load_state()
                    ChangeState(lCurrentState, lNextState, window, view, entity_manager)

    def render_frame(self):
        #This makes the program so that it basically pauses all of its game updates when a user clicks outside of the window. And it waits until the user clicks on the window.
        if self._is_window_active:
            self._entity_manager.render_update(self._window, self._view)
            
        self._window.display()
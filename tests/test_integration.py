import oecs
import oecs.entity_manager
import oecs.system_manager
import oecs.input_manager
import oecs.asset_manager
import oecs.state_loader

def init_window():
    """This will setup the window and whatever needs setup (just once) at the start of the program."""
    window = sf.RenderWindow( sf.VideoMode( config.WINDOW_WIDTH, config.WINDOW_HEIGHT ), "TileGame" )

    #This makes the background of the screen Black.
    window.clear(sf.Color.BLACK)

    view = sf.View()
    view.reset(sf.FloatRect(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

    return (window, view)
    
def init_state_loader(window, view, entity_manager, system_manager, input_manager, asset_manager):
    # TODO: Load the classes within some directory that inherit from the Component base class.
    component_refs = {}
    
    # TODO: Load the classes within some directory that inherit from the System base class.
    system_refs = {}

    state_loader.StateLoader(window, view, entity_manager, system_manager, input_manager, asset_manager, component_refs, system_refs)

def init_oesc():
    (window, view) = init_window()
    
    entity_manager = entity_manager.EntityManager()
    system_manager = system_manager.SystemManager()
    input_manager = input_manager.InputManager()
    asset_manager = asset_manager.AssetManager()
    state_loader = init_state_loader(window, view, entity_manager_system_manager, input_manager, asset_manager)
    
    return oecs.OECS(window, view, state_loader, entity_manager, system_manager, input_manager, asset_manager)

def main():
    oesc = init_oesc()
    
    t = sf.Time(0.0)
    accumulator = sf.Time(0.0)
    MAX_FRAMESKIP = 5
    timer = sf.Clock()

    while not oesc.is_quit():
        frameTime = timer.elapsed_time
        timer.restart()

        #This caps the time inbetween frames to
        #   prevent a spiral of death (which happens when the computer
        #   can't keep up.)
        if frameTime > sf.Time(0.25):

            # print("preventing spiral of death")
            frameTime = sf.Time(0.25)

        accumulator += frameTime

        # Iterates the window's input events and applies them to the input manager.
        oesc.process_inputs()

        iLoops = 0  #A counter for the amount of game update loops that are made in sucession whilst skipping rendering updates.
        
        #This loop will start if it is time to commence the next update and will keep going if we are behind schedule and need to catch up.
        while accumulator >= sf.Time(1./config.FRAME_RATE) and iLoops < MAX_FRAMESKIP:
            #Notice that time difference is a constant variable that represents how much time is going by during
            #   this update.
            oesc.update_frame(sf.Time(1./config.FRAME_RATE))

            #If we have received a quit signal, we should stop our loop and quit the game!
            if oesc.is_quit():
                break

            #The accumulator contains the time that hasn't yet been used for the updates.
            #Each update will assume that dt time is going by, so the accumulator just
            #   needs to subtract by the time that is being used up.
            accumulator -= sf.Time(1./config.FRAME_RATE)
            
            #This counts the Update loop
            iLoops += 1
            
        oesc.render_frame()

    oesc.close()


#If this file was ran as the main, then we will call the main (if it was included in another file, this would prevent main() from being called.)
if __name__ == '__main__':
    main()

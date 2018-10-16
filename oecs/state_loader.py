class StateLoader(object):
    def __init__(self, window, view, entity_manager, system_manager, input_manager, asset_manager, component_refs={}, system_refs={}):
        """
        @param window The SFML window object that the state is to be loaded onto.
        @param view This is SFML's View object and allows us to zoom in on the what would be shown in the window. This
            essentially just gives us the option to zoom in on the stuff visible for a certain state (can be specified in xml data.)
        @param entity_manager This is for loading entities into the game based on the state being switched to.
        @param system_manager This is for manipulating the systems that are to be executed.
        @param input_manager This is for manipulating what inputs are listened for and how they interact with systems and entities.
        @param asset_manager This contains the assets that are to be used by SFML's renderer.
        @param component_refs A dictionary containing the accessible component class references. The key is the name of the component 
            and the value is the associated component class.
        @param system_refs A dictionary containing the accessible system class references. The key is the name of the system 
            and the value is the associated system class."""
        self._current_state = "NULL"
        self._window = window
        self._view = view
        self._entity_manager = entity_manager
        self._self._system_manager = system_manager
        self._input_manager = input_manager
        self._asset_manager = asset_manager
        
        # Below are the references for the things that are able to be instantiated by this state manager.
        self._component_refs = {}
        self._system_refs = {}

    def assemble_entity_info(self, root, sSystemRoot=None):
        """This will assemble the entity info for possibly several entities that are associated with a system call.
        This is meant to automate a way that we retrieve and assemble entity information for our xml files.
        @param root This is the root of some parsed xml, this object comes from the ElementTree library.
            The specific root object is of a sub-tree of the original xml data, only important
            entities will be contained in this sub-tree.
        @param sSystemRoot If this is specified, then it means that this is a section that needs to be looked in
            to find the entity data we want to return. The section is a child of the root.
        @return A list of entity data that can be used by the self._input_manager and self._system_manager."""
        lEntities = []
    
        if sSystemRoot == None:
            for entity in root.findall("entity"):
                lEntities.append((entity.find("entityType").text, entity.find("entitytName").text, entity.find("componentName").text))
                
        elif root.find(sSystemRoot) != None:       
            for entity in root.find(sSystemRoot).findall("entity"): 
                lEntities.append((entity.find("entityType").text, entity.find("entitytName").text, entity.find("componentName").text))
    
        return lEntities
    
    def get_entity_blueprints(self, entityRoot):
        """This is separate from ChangeState() because this chunk needs to be able to be recursive.
        This is necessary for the Entity_List entity to be able to hold entities (which may also
        end up being Entity_Lists, Giants may work as a special Entity_List.)
        This essentially just creates Entities recursively and stores them inside of its parent Entity
        like it's an attribute.
        @param entityRoot This is an ElementTree Node object and this is where we'll
            be using to look for the attributes (which may be entities, and if so recursion is necessary.)
        @return An Entity object that contains the attributes (which may have Entities within it) that
            were specified within the main xml file for the game."""
    
        entity = None
    
        iEntityDrawPriority = -1
    
        if entityRoot.find("drawPriority") != None:
            iEntityDrawPriority = int(entityRoot.find("drawPriority").text)
        
        #This checks to see if there is a function that exists that will assemble this entity.
        if entityRoot.find("assembleFunc") != None:
            #This will hold all of the attributes needed to assemble the entity (using the xml files to get the data later on.)
            dEntityAttribs = {}
    
            #This will loop through all of the attributes for the current entity
            #   Note that this only iterates over the immediate children.
            for attrib in entityRoot.find("Attributes"):
    
                #Sounds are ultimately stored in the AssetManager, but pointers to those sounds are within entities.
                if attrib.tag == 'Sound':
                    #THis will start a new list of Sounds if we haven't already loaded one into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}
    
                    #Query the AssetManager for a sound that is associated with this entity, then throw that into the dictionary of attributes!
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = self._asset_manager.get_sound(attrib.attrib["name"], attrib.text)
    
                #Music are ultimately stored in the AssetManager, but pointers to the music is within entities.
                elif attrib.tag == 'Music':
    
                    #THis will start a new list of Musics if we haven't already loaded one into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}
    
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = self._asset_manager.get_music(attrib.attrib['name'], attrib.text)
    
                #Textures are ultimately stored in the AssetManager, but pointers to those textures are within entities.
                elif attrib.tag == 'Texture':
    
                    #THis will start a new list of Textures if we haven't already loaded one into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}
    
                    #Query the AssetManager for a texture that is associated with this entity, then throw that into the dictionary of attributes!
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = self._asset_manager.get_texture(attrib.attrib['name'], attrib.text)
    
                #This is for the tileAtlas'
                elif attrib.tag == 'RenderState':
    
                    #THis will start a new list of sf.RenderStates if we haven't already loaded one into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}
    
                    #Query the AssetManager for a sf.RenderState that is associated with this entity, then throw that into the dictionary of attributes!
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = self._asset_manager.get_render_state(attrib.attrib['name'], attrib.text)
    
    
                #Fonts are also in the AssetManager like textures.
                elif attrib.tag == 'Font':
     
                    #THis will start a new list of Fonts if we haven't already loaded one into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}
    
                    #Query the AssetManager for a font that is associated with this entity, then throw that into the dictionary of attributes!
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = self._asset_manager.get_font(attrib.attrib['name'], attrib.text)
    
                #The Collision_Body needs a list of shapes represented by dictionaries of attribs for each shape. This
                #   assembles that data representation so that not just entity assemblers are required for collisidable entities.
                elif attrib.tag == 'CollisionBody':
                    #THis will start a new list of CollisionShapes if we haven't already loaded one into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}
    
                    #This list of shapes will define the collision body.
                    lShapes = []
    
                    #Iterate through the collision shapes
                    for cShape in attrib:
                        dShapeAttribs = {}
    
                        for shapeAttrib in cShape:
                            dShapeAttribs[shapeAttrib.tag] = shapeAttrib.text
                            
                        lShapes.append(dShapeAttribs)
    
                    #Bodies are marked by their name and are defined by a list of shapes.
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = lShapes
    
                #For storing entities within entities. This was originally for the EntityPQueue.
                elif attrib.tag == 'entity':
    
                    #THis will start a new list of Entities if we haven't already loaded one into this entity's attributes.
                    if dEntityAttribs.get(attrib.tag, None) == None:
                        dEntityAttribs[attrib.tag] = {}
    
                    #Here's the one and only recursive call. The base case occurs
                    #   when there aren't anymore nested Entities.
                    dEntityAttribs[attrib.tag][attrib.attrib["name"]] = self.get_entity_blueprints(attrib)
    
                else:
                    #Anything else will just be put in the dictionary as an attribute
                    dEntityAttribs[attrib.tag] = attrib.text
    
            assembleFunc = ClassRetrieval.getClass(entityRoot.find('assembleFunc').text)
               
            #Here we're using the Assemble*() function associated with the name of this entity to assemble the entity so that
            #we can add it to the EntityManager.
            #And all Assemble*() functions will use the same arguments(using a dictionary to allow dynamic arguments.)
            entity = assembleFunc(entityRoot.attrib['name'], entityRoot.attrib['type'], iEntityDrawPriority, dEntityAttribs)
    
        else:
            #Here we will add in a default entity instance.
            entity = Entity.Entity(entityRoot.attrib['name'], entityRoot.attrib['type'], iEntityDrawPriority,{})
    
        #THis adds in the components that exist in the xml file for this entity (it allows custom/variations of entities to exist.)
        for component in entityRoot.findall('Component'):
    
            componentClass = ClassRetrieval.getClass(component.attrib['name'])
    
            #This will add in a component into the entity we just created.
            #And note that it is giving the component a dictionary of the data in the xml files.
            entity.add_component(componentClass({DataTag.tag: DataTag.text for DataTag in component}))
    
        return entity

        
    # TODO: Need These
    # - StateDefinition class that declares how a state is loaded.
    # - load_state() must take in a StateDefinition whether it was programmatic or loaded from a json file.
    # - load_state() must use the class references stored within the managed dictionaries. This
    #   allows a very flexible linking system.
    def load_state(self, state_definition):
        """This function is passed a couple lists representing the info on the different levels of this game's
        hierarchical finite state machine. This function essentially generically sets up the Entity and Asset Managers
        based off of data that can be retreived from xml files.
        @param lNxtState This list contains the information on which state the program is to be switched to and it takes acount into
            sub-states. So each element of the list is a sub-state of the previous element.
        @param self._view This is SFML's View object and allows us to zoom in on the what would be shown in the self._window. This
            essentially just gives us the option to zoom in on the stuff visible for a certain state (can be specified in xml data.)
        @param self._entity_manager This is the entity manager and is for loading entities into the game based on the state being switched to.
            The xml data tells which entities need to be loaded for what state."""
    
        print("NEW !", lNxtState)
        #The data will lie within the nextState[0]+".txt" file and the nextState[1] element within that elemthe ent.
        tree = parse("StateData/%s/%s.xml"%(lNxtState[0],lNxtState[1]))
        
        #The root element and the element containing the entities we need will be using this variable.
        root = tree.getroot()
    
    
        #This will reset the self._windowView's dimensions within the actual self._window with respect to the new state
        #self._view.reset(sf.FloatRect((self._window.width - int(root.find('viewWidth').text))/2, \
        #            (self._window.height - int(root.find('viewHeight').text))/2,   \
        #            int(root.find('viewWidth').text),    \
        #            int(root.find('viewHeight').text)))
    
        #print float(root.find('viewWidthRatio').text)
    
        print("The new view's stats:\nx:%f\ny:%f\nwidth:%f\nheight:%f"%(int(self._window.width - int(self._window.width*float(root.find('viewWidthRatio').text)))/2,     \
                                    int(self._window.height - int(self._window.height*float(root.find('viewHeightRatio').text)))/2,  \
                                    int(self._window.width*float(root.find('viewWidthRatio').text)),                           \
                                    int(self._window.height*float(root.find('viewHeightRatio').text))))
        
        self._view.reset(sf.FloatRect((self._window.width - int(self._window.width*float(root.find('viewWidthRatio').text)))/2,     \
                                    (self._window.height - int(self._window.height*float(root.find('viewHeightRatio').text)))/2,  \
                                    self._window.width*float(root.find('viewWidthRatio').text),                           \
                                    self._window.height*float(root.find('viewHeightRatio').text)))
        
        config.Tile_Width = self._window.width / (config.CHUNK_TILES_WIDE*2.)
        config.Tile_Height = self._window.height / (config.CHUNK_TILES_HIGH*2.)
    
        print("TileWidth is %f and TileHeight is %f"%(config.Tile_Width, config.Tile_Height))
        print("self._window dimensions are %d x %d"%(self._window.width, self._window.height))
        
        #self._view.reset(sf.FloatRect(int(self._window.width - self._window.width*float(root.find('viewWidthRatio').text)/2), \
        #                int(self._window.height - self._window.height*float(root.find('viewHeightRatio').text)/2),            \
        #                int(self._window.width*float(root.find('viewWidthRatio').text)),               \
        #                int(self._window.height*float(root.find('viewHeightRatio').text))))
    
        #This clears all of the things that in the game since the last state
        self._entity_manager.empty_entity_containers()
        self._asset_manager.empty_assets()
        self._input_manager.empty_inputs()
        self._system_manager.empty_systems()
    
        for entity in root.findall('Entity'):
    
            entityInstance = self.get_entity_blueprints(entity)
    
            self._entity_manager.add_entity(entityInstance)
    
                
        #Each one of these nodes will be an input that will be initialized for the state that is being loaded (and a multitude of kinds.)
        for inpoot in root.findall("Input"):
    
            #print inpoot.attrib
    
            #Check to see if this input's type is a hotspot.
            if inpoot.attrib["type"] == "hotspot":
                self._input_manager.add_hotspot(inpoot.find("x").text, inpoot.find("y").text, inpoot.find("width").text, inpoot.find("height").text, \
                                           inpoot.find("OnPressed").find("type").text if inpoot.find("OnPressed") != None else None,    \
                                           inpoot.find("OnSelected").find("system").text if inpoot.find("OnSelected") != None else None,    \
                                           self.assemble_entity_info(inpoot, "OnSelected"), \
                                           inpoot.find("OnDeselected").find("system").text if inpoot.find("OnDeselected") != None else None,    \
                                           self.assemble_entity_info(inpoot, "OnDeselected"), \
                                           inpoot.find("OnPressed").find("system").text if inpoot.find("OnPressed") != None else None,    \
                                           self.assemble_entity_info(inpoot, "OnPressed"), \
                                           inpoot.find("OnReleased").find("system").text if inpoot.find("OnReleased") != None else None,   \
                                           self.assemble_entity_info(inpoot, "OnReleased"))
    
            #Check to see if thisinput's type is a action.
            elif inpoot.attrib["type"] == "key":
                #This will add a key_Listener to our self._input_manager given the attribute data from the inpoot elemenet from the xml file.
                self._input_manager.add_key_listener(inpoot.find("key").text,    \
                                                inpoot.find("OnPressed").find("type").text if inpoot.find("OnPressed") != None else None,  \
                                                inpoot.find("OnPressed").find("system").text if inpoot.find("OnPressed") != None else None,   \
                                                self.assemble_entity_info(inpoot, "OnPressed"),    \
                                                inpoot.find("OnReleased").find("system").text if inpoot.find("OnReleased") != None else None,   \
                                                self.assemble_entity_info(inpoot, "OnReleased"))
    
            elif inpoot.attrib["type"] == "mouse":
                self._input_manager.add_mouse_listener(inpoot.find("button").text,             \
                                                  inpoot.find("OnPressed").find("type").text if inpoot.find("OnPressed") != None else None,  \
                                                  inpoot.find("OnPressed").find("system").text if inpoot.find("OnPressed") != None else None,   \
                                                  self.assemble_entity_info(inpoot, "OnPressed"),    \
                                                  inpoot.find("OnReleased").find("system").text if inpoot.find("OnReleased") != None else None,   \
                                                  self.assemble_entity_info(inpoot, "OnReleased"))
    
        #These are the systems that are relevant to this state and they will be added into the System_Queue class.
        for system in root.findall("System"):
            
            #This will load a system into the System_Queue and then it will be activated next update.
            self._system_manager.add_system(system.find("type").text, system.find("systemFunc").text,  self.assemble_entity_info(system))
            
                
        #Now we gotta update the state variables so that we aren't signaling to change states anymore
        # TODO: This thing has been completely broken by the new state format.
        for i in range(len(_lCurrentState)):
            _lCurrentState[i] = lNxtState[i]
            lNxtState[i] = "NULL"
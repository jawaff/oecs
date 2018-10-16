import os
import sfml as sf

class AssetManager(object):
    def __init__(self):
        #These four dictionaries will store the SFML objects that are currently in use
        #in the program.
        self._fonts = {}
        self._textures = {}
        self._render_states = {}
        self._sounds = {}
        self._music = {}

    def empty_assets(self):
        """This essentially will be used at the beginning of each state so that there aren't
        any unnecessary assets in the dictionaries from the last state."""
        self._fonts.clear()
        self._textures.clear()
        self._render_states.clear()
        self._sounds.clear()
        self._music.clear()

    def get_font(self, sName, sFileName):
        """This is for retrieving a pointer to a specific Font object in our dictionary.
        Input: The name of the font's actual file (string.)
        Output: An SFML Font object that was requested."""

        #Check to see if that filename is listed in our dictionary already.
        if self._fonts.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return self._fonts[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            self._fonts[sName] = sf.Font.load_from_file('Resources/Fonts/'+sFileName)

            #We can now just return the SFML object that is within the dictionary.
            return self._fonts[sName]

    def get_texture(self, sName, sFileName):
        
        #Check to see if that filename is listed in our dictionary already.
        if self._textures.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return self._textures[sName]
        else:
            #We must create a new SFML Texture object while using the sFileName to load in a font.
            self._textures[sName] = sf.Texture.load_from_file('Resources/Textures/'+sFileName)

            #We can now just return the SFML object that is within the dictionary.
            return self._textures[sName]

    def get_render_state(self, sName, sFileName):
        
        #Check to see if that filename is listed in our dictionary already.
        if self._render_states.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return self._render_states[sName]
        else:
            #We must create a new SFML Texture object while using the sFileName to load in a font.
            texture = sf.Texture.load_from_file('Resources/Textures/'+sFileName)

            self._render_states[sName] = sf.RenderStates(sf.BLEND_ALPHA,
                                                                None,
                                                                texture)

            #We can now just return the SFML object that is within the dictionary.
            return self._render_states[sName]

    def get_sound(self, sName, sFileName):
        """A sound is assumed to be a lot shorter than music and it will be loaded into memory unlike the music (which is streamed.)"""

        #Check to see if that filename is listed in our dictionary already.
        if self._sounds.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return self._sounds[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            Asset_Managers.self._sounds[sName] = sf.Sound.load_from_file('Resources/Sounds/'+sFileName)

            #We can now just return the SFML object that is within the dictionary.
            return self._sounds[sName]

    def get_music(self, sName, sFileName):
        """The Music object that is returned will stream the music as it plays."""

        #Check to see if that filename is listed in our dictionary already.
        if self._music.get(sName, None) != None:
            #We can now just return the SFML object that is within the dictionary.
            return self._music[sName]
        else:
            #We must create a new SFML Font object while using the sFileName to load in a font.
            self._music[sName] = sf.Music.open_from_file('Resources/Musics/'+sFileName)

            #We can now just return the SFML object that is within the dictionary.
            return self._music[sName]

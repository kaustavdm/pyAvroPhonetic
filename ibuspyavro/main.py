#!/usr/bin/env python

"""Provides iBus component and bus for pyAvroPhonetic

Details of IBus api is available at:
http://ibus.googlecode.com/svn/docs/ibus-1.5

-------------------------------------------------------------------------------

Copyright (C) 2013 Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.

This file is part of pyAvroPhonetic.

pyAvroPhonetic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyAvroPhonetic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyAvroPhonetic.  If not, see <http://www.gnu.org/licenses/>.

"""

# Imports
import sys
from pyavrophonetic import avro
from gi.repository import IBus


# Initialize IBus
print "Initializing IBus"
IBus.init()
# Get the IBus Bus
BUS = IBus.Bus()

def reset_all(engine):
    """Resets engine's properties"""
    engine.buffertext = ""

def commit_candidate(engine):
    """Commit candidate"""
    if len(engine.buffertext) > 0:
        commit_text = IBus.Text.new_from_string(avro.parse(engine.buffertext))
        engine.commit_text(commit_text)
        print "Text at commit : {0} - {1}".format(engine.buffertext, commit_text)
    # Reset all
    reset_all(engine)

def process_key_event(engine, keyval, keycode, state):
    """Closure for process-key-event signal"""
    # print keypress info, useful for debugging
    print "{0} - {1} - {2}".format(keyval, keycode, state)
    # ignore release event
    if state not in [0, 1, 16, 17]:
        print "state was {0}. Returning False".format(state)
        return False
    # capture shift key
    if keycode == 42:
        print "Shift key pressed"
        return True

    # process letter key events
    if ((33 <= keyval <= 126) or (IBus.KP_0 <= keyval <= IBus.KP_9) or
        (keyval in [IBus.KP_Decimal, IBus.KP_Add, IBus.KP_Subtract,
                    IBus.KP_Multiply, IBus.KP_Divide])):
        engine.buffertext += IBus.keyval_to_unicode(keyval)
        print "engine.buffertext: {0}".format(engine.buffertext)
        # update suggestions here

    elif keyval in [IBus.Return, IBus.space, IBus.Tab]:
        if len(engine.buffertext) > 0:
            if ((keyval == IBus.Return) and engine.setting_switch_newline and
                engine.setting_switch_preview):
                commit_candidate(engine)
                return True
            else:
                commit_candidate(engine)
                print "engine.buffertext: {0}".format(engine.buffertext)

    elif keyval == IBus.BackSpace:
        if len(engine.buffertext) > 0:
            print "Backspace fired. Removing last char from buffertext"
            engine.buffertext = engine.buffertext[:-1]
            # update suggestions here
            if len(engine.buffertext) <= 0:
                print "buffertext was <= 0. Reset all engine"
                reset_all(engine)
            return True

    elif keyval in [IBus.Left, IBus.KP_Left, IBus.Right, IBus.KP_Right]:
        print "Pressed arrow {0}".format(IBus.keyval_to_unicode(keyval))
        return True

    elif keyval in [IBus.Up, IBus.KP_Up, IBus.Down, IBus.KP_Down]:
        print "Pressed arrow {0}".format(IBus.keyval_to_unicode(keyval))
        return True

    elif keyval in [IBus.Control_L, IBus.Control_R, IBus.Insert, IBus.KP_Insert,
                    IBus.Delete, IBus.KP_Delete, IBus.Home, IBus.KP_Home,
                    IBus.Page_Up, IBus.KP_Page_Up, IBus.Page_Down,
                    IBus.KP_Page_Down, IBus.End, IBus.KP_End, IBus.Alt_L,
                    IBus.Alt_R, IBus.Return, IBus.space, IBus.Tab,
                    IBus.KP_Enter]:
        commit_candidate(engine)
        print "Pressed {0}".format(IBus.keyval_to_unicode(keyval))
    # if nothing match, return False
    return False

def get_proplist():
    """Generates IBus.PropList"""
    proplist = IBus.PropList()
    propp = IBus.Property.new('about', IBus.PropType.NORMAL,
                              IBus.Text.new_from_string("About"),
                              'gtk-about',
                              IBus.Text.new_from_string("About pyAvroPhonetic"),
                              True, True, IBus.PropState.UNCHECKED, None)
    proplist.append(propp)
    return proplist

def focus_in(engine):
    """Closure for focus-in signal"""
    proplist = get_proplist()
    engine.register_properties(proplist)

def focus_out(engine):
    """Closure for focus-out signal"""
    if len(engine.buffertext) > 0:
        commit_candidate(engine)

def create_engine_cb(factory, engine_name):
    """Creates engine if bus is connected"""
    # Create engine
    engine = IBus.Engine(engine_name = engine_name,
                         object_path = "/org/freedesktop/IBus/Engine/1",
                         connection = BUS.get_connection())
    # Connect to process-key-event signal
    engine.connect('process-key-event', process_key_event)
    # Connect to focus-in signal
    #engine.connect('focus-in', focus_in)
    # Connect to focus-out signal
    engine.connect('focus-out', focus_out)
    # Call reset
    reset_all(engine)
    return engine

def get_component():
    """Creates new component instance (IBus.Component)"""
    # Support for older versions
    data = {'name': "org.freedesktop.IBus.pyAvro",
            'description': "Avro Phonetic -- Python",
            'version': "0.1",
            'license': "GNU GPL v3+",
            'author': "Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in>",
            'homepage': "https://github.com/kaustavdm/pyAvroPhonetic",
            'exec': "/usr/bin/env python -m ibuspyavro.main",
            'textdomain': "ibus-pyavro"}
    # Support for newer versions
    data_new = {'name': "org.freedesktop.IBus.pyAvro",
                'description': "Avro Phonetic -- Python",
                'version': "0.1",
                'license': "GNU GPL v3+",
                'author': "Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in>",
                'homepage': "https://github.com/kaustavdm/pyAvroPhonetic",
                'command_line': "/usr/bin/env python -m ibuspyavro.main",
                'textdomain': "ibus-pyavro"}
    # Try and see which version clicks
    try:
        component = IBus.Component(**data)
    except TypeError:
        component = IBus.Component(**data_new)
    # Return the Component object
    return component

def get_engine_desc():
    """Creates new engine description (IBus.EngineDesc)"""
    data = {'name': "ibus-pyavro",
            'longname': "pyAvroPhonetic",
            'description': "Avro Phonetic -- Python implementation",
            'language': "bn",
            'license': "GNU GPL v3+",
            'author': "Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in>",
            'icon': "",
            'layout': "bn"}
    engine = IBus.EngineDesc(**data)
    return engine

def main():
    """Function executed when script is called"""
    # Get argument passed to script
    try:
        exec_by_ibus = (sys.argv[1] == '--ibus')
    except IndexError:
        exec_by_ibus = False


    # if bus is connected, do stuff
    if BUS.is_connected():
        # Create new IBus Factory
        factory = IBus.Factory.new(BUS.get_connection())
        factory.connect('create-engine', create_engine_cb)
        # Create new component
        component = get_component()
        # Create engine description
        enginedesc = get_engine_desc()
        # Add engine description to component
        component.add_engine(enginedesc)
        # Check if '--ibus' parameter was given
        if exec_by_ibus:
            BUS.request_name("org.freedesktop.IBus.pyAvro", 0)
        else:
            BUS.register_component(component)
        # Call IBus.main()
        IBus.main()
    else:
        # Bus is not connected
        print "Exiting because IBus Bus not found..."
        print "...maybe the daemon is not running ?"


# Call main() if called as script
if __name__ == '__main__':
    main()

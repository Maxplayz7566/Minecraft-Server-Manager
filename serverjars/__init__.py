# Plugin
from serverjars.plugin.paper import *
from serverjars.plugin.folia import *

# Proxies
from serverjars.proxies.velocity import *
from serverjars.proxies.waterfall import *
from serverjars.proxies.bungeecord import *

# Modded
from serverjars.modded.forge import *
from serverjars.modded.fabric import *

# Vanilla
from serverjars.vanilla.realase import *

def get_loaders():
    return ['fabric', 'forge', 'paper', 'folia', 'waterfall', 'velocity', 'bungeecord', 'vanilla', 'snapshot']

def get_jar(loader='vanilla', version=None, filepath='./server.jar'):
    if loader == 'vanilla':
        get_vanilla_jar(version, filepath)
    elif loader == 'bungeecord':
        get_bungeecord_jar(version, filepath)
    elif loader == 'paper':
        get_paper_jar(version, filepath)
    elif loader == 'folia':
        get_folia_jar(version, filepath)
    elif loader == 'velocity':
        get_velocity_jar(version, filepath)
    elif loader == 'waterfall':
        get_waterfall_jar(version, filepath)
    elif loader == 'forge':
        get_forge_jar(version, filepath)
    elif loader == 'fabric':
        get_fabric_jar(version, filepath)
    else:
        raise ValueError("Invalid loader specified. Choose from: " + ', '.join(get_loaders()))

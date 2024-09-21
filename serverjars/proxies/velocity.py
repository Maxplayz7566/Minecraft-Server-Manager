import requests


def get_velocity_versions():
    """
    Gets all the velocity versions

    :return: list
    """

    versions = requests.get('https://papermc.io/api/v2/projects/velocity').json()['versions']

    return versions

def get_velocity_jar(version=None, filepath='./server.jar'):
    """
    Downloads the velocity jar of your choosing

    :param version: What version of velocity automaticly selects latest
    :param filepath: Where you want to save the jarfile
    :return: filepath
    """
    if version is None:
        version = get_velocity_versions()[-1]
    buildResponse = requests.get(f'https://papermc.io/api/v2/projects/velocity/versions/{version}')
    buildResponse.raise_for_status()
    build = buildResponse.json()['builds'][-1]
    download = requests.get(f'https://papermc.io/api/v2/projects/velocity/versions/{version}/builds/{build}/downloads/velocity-{version}-{build}.jar')
    download.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(download.content)

    return filepath
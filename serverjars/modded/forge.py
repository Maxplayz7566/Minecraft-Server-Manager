import requests

def get_forge_versions():
    """
    Gets all the forge installer versions

    :return: list
    """

    response = requests.get('https://centrojars.com/api/fetchJar/modded/forge/fetchAllDetails.php').json()
    versions = []

    for version in response['response']['files']:
        versions.append(version['version'])

    return versions


def get_forge_jar(version=None, filepath='./server.jar'):
    """
    Downloads the forge installer jar of your choosing

    :param version: What version of forge automaticly selects latest
    :param filepath: Where you want to save the jarfile
    :return: filepath
    """
    if version is None:
        version = get_forge_versions()[0]

    response = requests.get(f'https://centrojars.com/api/fetchJar/modded/forge/{version}')

    with open(filepath, 'wb') as f:
        f.write(response.content)

    return filepath
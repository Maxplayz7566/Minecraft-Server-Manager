import requests

def get_fabric_versions():
    """
    Gets all the fabric versions

    :return: list
    """

    response = requests.get('https://centrojars.com/api/fetchJar/modded/fabric/fetchAllDetails.php').json()
    versions = []

    for version in response['response']['files']:
        versions.append(version['version'])

    return versions


def get_fabric_jar(version=None, filepath='./server.jar'):
    """
    Downloads the fabric jar of your choosing

    :param version: What version of fabric automaticly selects latest
    :param filepath: Where you want to save the jarfile
    :return: filepath
    """
    if version is None:
        version = get_fabric_versions()[0]

    response = requests.get(f'https://centrojars.com/api/fetchJar/modded/fabric/{version}')

    with open(filepath, 'wb') as f:
        f.write(response.content)

    return filepath
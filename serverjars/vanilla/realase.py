import requests

def get_vanilla_versions():
    """
    Gets all the vanilla versions

    :return: list
    """

    response = requests.get('https://centrojars.com/api/fetchJar/vanilla/vanilla/fetchAllDetails.php').json()
    versions = []

    for version in response['response']['files']:
        versions.append(version['version'])

    return versions


def get_vanilla_jar(version=None, filepath='./server.jar'):
    """
    Downloads the vanilla jar of your choosing

    :param version: What version of vanilla automaticly selects latest
    :param filepath: Where you want to save the jarfile
    :return: filepath
    """
    if version is None:
        version = get_vanilla_versions()[0]

    response = requests.get(f'https://centrojars.com/api/fetchJar/vanilla/vanilla/{version}')

    with open(filepath, 'wb') as f:
        f.write(response.content)

    return filepath
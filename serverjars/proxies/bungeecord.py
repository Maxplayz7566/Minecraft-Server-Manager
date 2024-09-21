import requests

def get_bungeecord_versions():
    """
    Gets all the bungeecord versions

    :return: list
    """

    response = requests.get('https://centrojars.com/api/fetchJar/proxies/bungeecord/fetchAllDetails.php').json()
    versions = []

    for version in response['response']['files']:
        versions.append(version['version'])

    return versions


def get_bungeecord_jar(version=None, filepath='./server.jar'):
    """
    Downloads the bungeecord jar of your choosing

    :param version: What version of bungeecord automaticly selects latest
    :param filepath: Where you want to save the jarfile
    :return: filepath
    """
    if version is None:
        version = get_bungeecord_versions()[0]

    response = requests.get(f'https://centrojars.com/api/fetchJar/proxies/bungeecord/{version}')

    with open(filepath, 'wb') as f:
        f.write(response.content)

    return filepath
import requests


def get_folia_versions():
    """
    Gets all the folia versions

    :return: list
    """

    versions = requests.get('https://papermc.io/api/v2/projects/folia').json()['versions']

    return versions

def get_folia_jar(version=None, filepath='./server.jar'):
    """
    Downloads the folia jar of your choosing

    :param version: What version of folia automaticly selects latest
    :param filepath: Where you want to save the jarfile
    :return: filepath
    """
    if version is None:
        version = get_folia_versions()[-1]
    buildResponse = requests.get(f'https://papermc.io/api/v2/projects/folia/versions/{version}')
    buildResponse.raise_for_status()
    build = buildResponse.json()['builds'][-1]
    download = requests.get(f'https://papermc.io/api/v2/projects/folia/versions/{version}/builds/{build}/downloads/folia-{version}-{build}.jar')
    download.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(download.content)

    return filepath
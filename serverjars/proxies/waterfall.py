import requests


def get_waterfall_versions():
    """
    Gets all the waterfall versions

    :return: list
    """

    versions = requests.get('https://papermc.io/api/v2/projects/waterfall').json()['versions']

    return versions

def get_waterfall_jar(version=None, filepath='./server.jar'):
    """
    Downloads the waterfall jar of your choosing

    :param version: What version of waterfall automaticly selects latest
    :param filepath: Where you want to save the jarfile
    :return: filepath
    """
    if version is None:
        version = get_waterfall_versions()[-1]
    buildResponse = requests.get(f'https://papermc.io/api/v2/projects/waterfall/versions/{version}')
    buildResponse.raise_for_status()
    build = buildResponse.json()['builds'][-1]
    download = requests.get(f'https://papermc.io/api/v2/projects/waterfall/versions/{version}/builds/{build}/downloads/waterfall-{version}-{build}.jar')
    download.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(download.content)

    return filepath
import requests


def get_paper_versions():
    """
    Gets all the paper versions

    :return: list
    """

    versions = requests.get('https://papermc.io/api/v2/projects/paper').json()['versions']

    return versions

def get_paper_jar(version=None, filepath='./server.jar'):
    """
    Downloads the paper jar of your choosing

    :param version: What version of paper automaticly selects latest
    :param filepath: Where you want to save the jarfile
    :return: filepath
    """
    if version is None:
        version = get_paper_versions()[-1]
    buildResponse = requests.get(f'https://papermc.io/api/v2/projects/paper/versions/{version}')
    buildResponse.raise_for_status()
    build = buildResponse.json()['builds'][-1]
    download = requests.get(f'https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{build}/downloads/paper-{version}-{build}.jar')
    download.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(download.content)

    return filepath
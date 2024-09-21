import requests


def get_messages(url, key):
    url = f"{url}/studioclock/messages"
    headers = {"Authorization": f"Bearer {key}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:  # Unauthorised - invalid API key
        raise ValueError("Invalid API key")
    else:
        raise ValueError("Unable to fetch messages.")

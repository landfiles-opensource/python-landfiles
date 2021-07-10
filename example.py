import sys

from landfiles import LandfilesClient


if __name__ == "__main__":
    try:
        client_id = sys.argv[1]
        client_secret = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
    except IndexError:
        print("Usage : python example.py <client_id> <client_secret> <username> <password>")
        sys.exit(1)

    client = LandfilesClient(client_id, client_secret, username, password)

    farm = client.get_farm("F-9b0f9331-4ded-4ea0-9549-d01dec0f6897")
    print(farm.list_parcels()[0].api_data)
    # print(farm.api_data)
    pub = farm.list_publications()[0]

    group = client.get_group("GR-183ef8d8-e07c-4697-88b7-6611633cf252")

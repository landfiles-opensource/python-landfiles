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

    print("Groups:")
    print(client.list_groups())

    print()
    print("Farms:")
    farms = client.list_farms()
    print(farms)

    farm = farms[0]
    print()
    print(f"Parcels of farm '{farm}':")
    print(farm.list_parcels())

    parcel = farm.list_parcels()[0]
    print()
    print(f"Data of parcel '{parcel}':")
    print(parcel.api_data)

    print()
    print(f"Publications of farm '{farm}':")
    print(farm.list_publications())

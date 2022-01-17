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
    groups = client.list_groups()
    print(groups)

    group = groups[0]
    print(f"Parcels of group '{group}':")
    #print(list(group.list_parcels()))

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

    print()
    print(f"Parcels with no COLL_00070 of farm '{farm}':")
    print(list(farm.list_parcels_with_all_missing_data(["COLL_00070"])))

    print()
    print(f"Parcels with no COLL_00070 of group '{group}':")
    #print(list(group.list_parcels_with_all_missing_data(["COLL_00070"])))

    group_id = "GR-5b9f8337-bbf7-4388-8c65-4e215164700c"
    print()
    print(f"Observations of group '{group_id}'")
    group = client.get_group(group_id)
    print(group.list_observations())

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

    """
    print("Groups:")
    groups = client.list_groups()
    print(groups)

    print()
    print("Farms:")
    farms = client.list_farms()
    print(farms)

    farm = farms[0]
    print()
    print(f"Parcels of farm '{farm}':")
    print(farm.list_parcels())
    """

    group_id = "GR-5b9f8337-bbf7-4388-8c65-4e215164700c"
    print()
    print(f"Observations of group '{group_id}'")
    group = client.get_group(group_id)
    group_obs = group.list_observations()
    print(sorted([td.type for td in group_obs.get_measure_typedefs()]))
    print(list(group_obs.list_parcels_with_all_data(["COLL_00070", "COLL_00404"])))

import sys

from landfiles import LandfilesClient


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        password = sys.argv[2]
        basic_token = sys.argv[3]
    except IndexError:
        print(
            "Usage : python example.py <username> <password> <basic_token>"
        )
        print(
            "Ex : python example.py agri@landfiles.fr 1234 dfgkpoere4zfe89fze1496"
        )
        sys.exit(1)

    client = LandfilesClient(username, password, auth=f"Basic {basic_token}")

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

    group_id = "GR-5b9f8337-bbf7-4388-8c65-4e215164700c"
    print()
    print(f"Observations of group '{group_id}'")
    group = client.get_group(group_id)
    group_obs = group.list_observations()
    print(len(group_obs))
    print(len(group_obs.filter(any_measured=["COLL_00070", "COLL_00404"])))
    print(
        group_obs.filter(all_measured=["COLL_00070", "COLL_00404"])[
            "PA-c5192de0-2e06-4cbe-8358-5c0785946130"
        ]
    )

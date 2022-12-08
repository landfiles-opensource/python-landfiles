import datetime as dt

import requests
from requests.auth import HTTPBasicAuth

from .data_structures import (
    Measure,
    MeasureDict,
    ParcelObservation,
    ParcelObservationDict,
    ParcelObservationList,
)


class APIError(requests.exceptions.RequestException):
    pass


class APIDataWrapper:
    default_id_field = "uuid"
    default_str_field = None

    def __init__(self, api_data, api_client, id_field=None, str_field=None):
        self.api_data = api_data
        self.api_client = api_client
        self.id_field = id_field or self.default_id_field
        self.str_field = str_field or self.default_str_field

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id} ({str(self)})"

    def __str__(self):
        return self.api_data[self.str_field or self.id_field]

    @property
    def id(self):
        return self.api_data[self.id_field]


class Farm(APIDataWrapper):
    default_str_field = "name"

    def list_parcels(self):
        return [
            Parcel(x, self.api_client)
            for x in self.api_client.get(
                f"/landfilesservice/v1/external/parcels/farms/{self.id}"
            )["parcels"]
        ]


class Parcel(APIDataWrapper):
    default_id_field = "id"
    default_str_field = "name"

    @property
    def observations(self):
        raise NotImplementedError("The API does not provide this information yet.")


class Group(APIDataWrapper):
    default_str_field = "name"

    def list_farms(self):
        return [
            Farm(x, self.api_client, id_field="id")
            for x in self.api_client.get(
                f"/landfilesservice/v1/external/farms/groups/{self.id}"
            )["farms"]
        ]

    def list_observations(self, start_date=None, end_date=None):
        if start_date is None:
            start_date = "0000-01-01"
        if end_date is None:
            end_date = "9999-12-31"
        data = self.api_client.get(
            f"/landfilesservice/v1/external/observations/groups/{self.id}?startDate={start_date}&endDate={end_date}"
        )
        return ParcelObservationDict(
            {
                parcel["parcelUuid"]: ParcelObservationList(
                    [
                        ParcelObservation(
                            id=obs["id"],
                            date=dt.datetime.fromtimestamp(obs["date"] / 1000),
                            url=obs["url"],
                            measures=MeasureDict(
                                {
                                    type: Measure(
                                        type=type,
                                        label=data["label"],
                                        value=data["value"],
                                        value_type=data["type"],
                                        value_label=data.get("valueLabel"),
                                    )
                                    for type, data in obs["data"].items()
                                }
                            ),
                        )
                        for obs in parcel["observations"]
                    ]
                )
                for parcel in data
            }
        )

    def _iterate_farms(self, farm_method, *farm_args, **farm_kwargs):
        for farm in self.list_farms():
            yield from getattr(farm, farm_method)(*farm_args, **farm_kwargs)

    def list_parcels(self):
        for farm in self.list_farms():
            yield from farm.list_parcels()


class LandfilesClient:
    BASE_URL = "https://api.landfiles.fr/api"

    def __init__(self, username, password, auth=None, base_url=None):
        self.base_url = base_url or self.BASE_URL
        headers = {}
        if auth:
            headers["Authorization"] = auth
        resp = requests.post(
            self.build_url("/authenticationservice/auth/oauth/token"),
            headers=headers,
            data={
                "username": username,
                "password": password,
                "grant_type": "password",
                "scope": "mobileclient",
            },
        )
        try:
            data = resp.json()
            self.token = data["access_token"]
        except KeyError:
            raise APIError(f"'access_token' key missing in the API response: {data}", response=resp)

    def build_url(self, endpoint):
        return self.base_url + endpoint

    def get(self, endpoint, **kwargs):
        try:
            resp = requests.get(
                self.build_url(endpoint),
                headers={"Authorization": f"Bearer {self.token}"},
                **kwargs,
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise APIError(str(e), response=e.response, request=e.request) from e
        return resp.json()

    def list_farms(self):
        return [
            Farm(api_data, self)
            for api_data in self.get("/landfilesservice/v1/farms/me")
        ]

    def get_farm(self, farm_id):
        return Farm(self.get(f"/landfilesservice/v1/farms/{farm_id}"), self)

    def list_groups(self):
        return [Group(x, self) for x in self.get("/landfilesservice/v1/groups/me")]

    def get_group(self, group_id):
        return Group(self.get(f"/landfilesservice/v1/groups/{group_id}"), self)

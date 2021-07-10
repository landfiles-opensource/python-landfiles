import requests
from requests.auth import HTTPBasicAuth


class APIError(Exception):
    def __init__(self, message, api_response):
        super().__init__(message)
        self.api_response = api_response


class APIDataWrapper:
    default_id_field = "uuid"

    def __init__(self, api_data, api_client, id_field=None):
        self.api_data = api_data
        self.api_client = api_client
        self.id_field = id_field or self.default_id_field

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id}"

    def __str__(self):
        return str(self)

    @property
    def id(self):
        return self.api_data[self.id_field]


class Farm(APIDataWrapper):
    def list_publications(self):
        return [
            Publication(x, self.api_client)
            for x in self.api_client.get("/landfilesservice/v1/external/pictures", params={"farmUuid": self.id})
        ]

    def list_parcels(self):
        return [
            Parcel(x, self.api_client)
            for x in self.api_client.get(f"/landfilesservice/v1/external/parcels/farms/{self.id}")["parcels"]
        ]


class ParcelData(dict):
    def __str__(self):
        return f"{self['dataLabel']} = {self['valueLabel']}"


class Parcel(APIDataWrapper):
    default_id_field = "id"

    @property
    def data(self):
        return {
            data["dataId"]: ParcelData(data)
            for data in self.api_data.get("data", [])
        }


class PublicationData(dict):
    def __str__(self):
        return f"{self['dataLabel']} = {self['valueLabel']}"


class Publication(APIDataWrapper):
    @property
    def data(self):
        return {
            obs["dataId"]: PublicationData(obs)
            for obs in self.api_data.get("data", [])
        }

    def get_image_url(self):
        try:
            return self.api_client.get(f"/filesservice/v1/pictures/image/{self.id}")[0]
        except IndexError:
            return


class Group(APIDataWrapper):
    def list_farms(self):
        return [
            Farm(x, self.api_client, id_field="id")
            for x in self.api_client.get(f"/landfilesservice/v1/external/farms/groups/{self.id}")["farms"]
        ]

class LandfilesClient:
    BASE_URL = "https://api.landfiles.fr/api"

    def __init__(self, client_id, client_secret, username, password):
        resp = requests.post(self.build_url("/authenticationservice/auth/oauth/token"), auth=HTTPBasicAuth(client_id, client_secret), data={
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password,
            "grant_type": "password",
        })
        self.token = resp.json()["access_token"]

    def build_url(self, endpoint):
        return self.BASE_URL + endpoint

    def get(self, endpoint, **kwargs):
        resp = requests.get(self.build_url(endpoint), headers={"Authorization": f"Bearer {self.token}"}, **kwargs)
        data = resp.json()
        if "error" in data:
            raise APIError(data, api_response=resp)
        return data

    def list_farms(self):
        return [
            Farm(api_data, self)
            for api_data in self.get("/landfilesservice/v1/farms/me")
        ]

    def get_farm(self, farm_id):
        return Farm(self.get(f"/landfilesservice/v1/farms/{farm_id}"), self)

    def list_groups(self):
        return [
            Group(x, self)
            for x in self.get("/landfilesservice/v1/groups/me")
        ]

    def get_group(self, group_id):
        return Group(self.get(f"/landfilesservice/v1/groups/{group_id}"), self)

    def list_n_last_publications(self, n):
        return [
            Publication(x, self)
            for x in self.get(f"/landfilesservice/v1/external/pictures/groups/{n}")
        ]

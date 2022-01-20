from collections import namedtuple
from itertools import chain


class MeasureTypeDef(namedtuple("MeasureTypeDef", "type label")):
    def __eq__(self, other):
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)


_Measure = namedtuple(
    "Measure",
    "type label value value_type value_label",
    defaults=[None],
)
class Measure(_Measure):
    def __str__(self):
        return f"{self.label} = {self.value_str}"

    @property
    def value_str(self):
        return self.value_label or str(self.value)


class MeasureDict(dict):
    pass


_GroupParcelObservation = namedtuple(
    "GroupParcelObservation",
    "id date url measures",
)
class GroupParcelObservation(_GroupParcelObservation):
    def __str__(self):
        return self.date.strftime("%Y-%m-%d %H:%M")


class GroupParcelObservationDict(dict):
    def get_measure_typedefs_by_parcel(self):
        return {
            parcel_id: set(chain.from_iterable([
                [MeasureTypeDef(m.type, m.label) for m in obs.measures.values()]
                for obs in observations
            ]))
            for parcel_id, observations in self.items()
        }

    def get_measure_typedefs(self):
        return set.union(*self.get_measure_typedefs_by_parcel().values())

    def _filter_parcels(self, filter_func):
        for parcel_id, observations in self.items():
            if filter_func(observations):
                yield parcel_id

    def _filter_parcels_by_measure_types(self, filter_by_types):
        def filter_func(observations):
            measured_types = chain.from_iterable([
                list(obs.measures)
                for obs in observations
            ])
            return filter_by_types(measured_types)
        return self._filter_parcels(filter_func)

    def list_parcels_with_any_missing_data(self, measure_types):
        return self._filter_parcels_by_measure_types(
            lambda measured_types: any(t not in measured_types for t in measure_types)
        )

    def list_parcels_with_all_missing_data(self, measure_types):
        return self._filter_parcels_by_measure_types(
            lambda measured_types: all(t not in measured_types for t in measure_types)
        )

    def list_parcels_with_any_data(self, measure_types):
        return self._filter_parcels_by_measure_types(
            lambda measured_types: any(t in measured_types for t in measure_types)
        )

    def list_parcels_with_all_data(self, measure_types):
        return self._filter_parcels_by_measure_types(
            lambda measured_types: all(t in measured_types for t in measure_types)
        )

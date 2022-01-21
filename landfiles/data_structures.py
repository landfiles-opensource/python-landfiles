from collections import namedtuple
from itertools import chain


class MeasureTypeDef(namedtuple("MeasureTypeDef", "type label")):
    def __eq__(self, other):
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)


_Measure = namedtuple(
    "Measure", "type label value value_type value_label", defaults=[None],
)


class Measure(_Measure):
    def __str__(self):
        return f"{self.label} = {self.value_str}"

    @property
    def value_str(self):
        return self.value_label or str(self.value)


class MeasureDict(dict):
    pass


_ParcelObservation = namedtuple("GroupParcelObservation", "id date url measures",)


class ParcelObservation(_ParcelObservation):
    def __str__(self):
        return self.date.strftime("%Y-%m-%d %H:%M")


class ParcelObservationList(list):
    pass


class ParcelObservationDict(dict):
    def get_measure_typedefs_by_parcel(self):
        return {
            parcel_id: set(
                chain.from_iterable(
                    [
                        [MeasureTypeDef(m.type, m.label) for m in obs.measures.values()]
                        for obs in observations
                    ]
                )
            )
            for parcel_id, observations in self.items()
        }

    def get_measure_typedefs(self):
        return set.union(*self.get_measure_typedefs_by_parcel().values())

    def _filter(self, filter_func):
        return self.__class__(filter(lambda item: filter_func(*item), self.items()))

    def _filter_by_measure_types(self, filter_by_types):
        def filter_func(parcel_id, observations):
            measured_types = set(
                chain.from_iterable([list(obs.measures) for obs in observations])
            )
            return filter_by_types(measured_types)

        return self._filter(filter_func)

    def filter(
        self,
        any_measured=None,
        all_measured=None,
        any_not_measured=None,
        all_not_measured=None,
    ):
        obj = self
        if any_measured is not None:
            obj = obj._filter_by_measure_types(
                lambda measured_types: any(t in measured_types for t in any_measured)
            )
        if all_measured is not None:
            obj = obj._filter_by_measure_types(
                lambda measured_types: all(t in measured_types for t in all_measured)
            )
        if any_not_measured is not None:
            obj = obj._filter_by_measure_types(
                lambda measured_types: any(
                    t not in measured_types for t in any_not_measured
                )
            )
        if all_not_measured is not None:
            obj = obj._filter_by_measure_types(
                lambda measured_types: all(
                    t not in measured_types for t in all_not_measured
                )
            )
        return obj

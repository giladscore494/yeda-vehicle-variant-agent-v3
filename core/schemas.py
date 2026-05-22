"""Lightweight enums for normalization. No Pydantic dependency for core enums."""
from __future__ import annotations

from enum import Enum


class BodyType(str, Enum):
    hatchback = "hatchback"
    sedan = "sedan"
    wagon = "wagon"
    coupe = "coupe"
    convertible = "convertible"
    suv = "suv"
    crossover = "crossover"
    mpv = "mpv"
    minivan = "minivan"
    pickup = "pickup"
    van = "van"
    roadster = "roadster"
    gran_coupe = "gran_coupe"
    liftback = "liftback"
    fastback = "fastback"
    commercial = "commercial"
    unknown = "unknown"


class FuelType(str, Enum):
    petrol = "petrol"
    diesel = "diesel"
    hybrid = "hybrid"
    plug_in_hybrid = "plug_in_hybrid"
    mild_hybrid = "mild_hybrid"
    electric = "electric"
    hydrogen = "hydrogen"
    lpg = "lpg"
    unknown = "unknown"


class Transmission(str, Enum):
    automatic = "automatic"
    manual = "manual"
    dual_clutch = "dual_clutch"
    cvt = "cvt"
    e_cvt = "e_cvt"
    single_speed_ev = "single_speed_ev"
    unknown = "unknown"


class Market(str, Enum):
    IL = "IL"
    EU = "EU"
    US = "US"
    GLOBAL = "GLOBAL"
    UNKNOWN = "UNKNOWN"

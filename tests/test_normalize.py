"""Tests for core/normalize.py."""
from core.normalize import (
    normalize_fuel_type,
    normalize_transmission,
    normalize_drivetrain,
    normalize_body_type,
)
from core.schemas import FuelType, Transmission, BodyType


class TestFuelType:
    def test_gasoline_to_petrol(self):
        assert normalize_fuel_type("Gasoline") == FuelType.petrol
        assert normalize_fuel_type("Petrol") == FuelType.petrol

    def test_mild_hybrid(self):
        assert normalize_fuel_type("Mild Hybrid Petrol") == FuelType.mild_hybrid
        assert normalize_fuel_type("MHEV Petrol") == FuelType.mild_hybrid

    def test_phev(self):
        assert normalize_fuel_type("PHEV") == FuelType.plug_in_hybrid
        assert normalize_fuel_type("Plug-in Hybrid") == FuelType.plug_in_hybrid

    def test_electric(self):
        assert normalize_fuel_type("EV") == FuelType.electric
        assert normalize_fuel_type("Electric") == FuelType.electric
        assert normalize_fuel_type("BEV") == FuelType.electric

    def test_diesel(self):
        assert normalize_fuel_type("Diesel") == FuelType.diesel


class TestTransmission:
    def test_dual_clutch(self):
        assert normalize_transmission("DSG") == Transmission.dual_clutch
        assert normalize_transmission("S-tronic") == Transmission.dual_clutch
        assert normalize_transmission("S tronic") == Transmission.dual_clutch
        assert normalize_transmission("7-speed DCT") == Transmission.dual_clutch

    def test_cvt(self):
        assert normalize_transmission("CVT") == Transmission.cvt

    def test_e_cvt(self):
        assert normalize_transmission("e-CVT") == Transmission.e_cvt

    def test_single_speed_ev(self):
        assert normalize_transmission("single speed") == Transmission.single_speed_ev
        assert normalize_transmission("single-speed EV") == Transmission.single_speed_ev

    def test_manual(self):
        assert normalize_transmission("6-speed manual") == Transmission.manual

    def test_automatic(self):
        assert normalize_transmission("8-speed automatic") == Transmission.automatic


class TestDrivetrain:
    def test_branded_awd(self):
        assert normalize_drivetrain("quattro") == "AWD"
        assert normalize_drivetrain("xDrive") == "AWD"
        assert normalize_drivetrain("4Motion") == "AWD"
        assert normalize_drivetrain("e-AWD") == "AWD"
        assert normalize_drivetrain("e4WD") == "AWD"

    def test_4x4(self):
        assert normalize_drivetrain("4x4") == "4WD"
        assert normalize_drivetrain("4X4") == "4WD"

    def test_standard(self):
        assert normalize_drivetrain("FWD") == "FWD"
        assert normalize_drivetrain("RWD") == "RWD"
        assert normalize_drivetrain("AWD") == "AWD"
        assert normalize_drivetrain("4WD") == "4WD"

    def test_none(self):
        assert normalize_drivetrain(None) is None

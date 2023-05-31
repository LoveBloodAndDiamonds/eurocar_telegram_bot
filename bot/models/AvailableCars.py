"""MAYBE ITS TRASH"""  # todo

from bot.models import CarClassification, CarParks


class AvailableCars:
    CarParks.EUROPCAR = {
        CarClassification.EDMR: ("WV Polo",),
        CarClassification.CDMR: ("Scoda Oktavia",),
        CarClassification.FDAR: ("Kia K5",),
        CarClassification.FVMD: ("Huindai H1",),
    }
    CarParks.REXRENT = {
        CarClassification.EDMR: ("Renault Logan",),
        CarClassification.CDMR: ("Renault Arcana",),
        CarClassification.FDAR: ("Hyundai Elantra",),
        CarClassification.FVMD: ("VW Caravella",),
    }
    CarParks.RENTMOTORS = {
        CarClassification.EDMR: ("Huindai Solaris",),
        CarClassification.CDMR: None,
        CarClassification.FDAR: ("Toyota Camry",),
        CarClassification.FVMD: ("Hyundai H1",),
    }

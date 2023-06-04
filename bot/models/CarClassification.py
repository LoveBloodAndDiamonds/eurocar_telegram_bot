from enum import Enum


class CarClassification(Enum):
    ECONOMY = (["EXMR", "EDMR", "EDAR", "EWMR", "HDAR", "CDMR", "CDAR", "CWMR"],
               "Эконом",
               "Эконом класс, маленькие и экономичные.",
               "🚕",)
    # ECONOMY = (["EXMR", "EDMR", "EDAR", "EWMR", "KPIW", "HDMR", "HDAR", "CDMR", "CDAR", "CWMR"],
    #            "Эконом",
    #            "Эконом класс, маленькие и экономичные.",
    #            "🚕",)
    COMFORT = (["IDMR", "IDAR", "SDAR", "FDAR"],
               "Комфорт",
               "Для тех, кому нужно больше комфорта.",
               "🛻",)
    CROSSOVER = (["EGAR", "IGAR", "SFAR"],
                 "Кроссовер",
                 "#Текст про кроссовер",  # todo
                 "🚙",)
    MINIVAN = (["FVMD"],
               "Минивэн",
               "Вместительный минивен, отдельная категория прав не нужна.",
               "🚚",)
    BUSINESS = (["PDAR"],
                "Бизнес",
                "Бизнес-класс, для особых случаев.",
                "🚗",)
    OFFROAD = (["XFAR"],
               "Внедорожник",
               "#Текст про оффроад машины",  # todo
               "🚜",)
    # LUXARY = (["LDAR"],
    #           "Люкс",
    #           "#Текст про машины премиум класса",  # todo
    #           "🏎",)

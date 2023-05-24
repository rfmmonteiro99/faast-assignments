"""
Script to create Region enum
"""
from enum import Enum
from typing import List


class Region(Enum):
    """Region enum to select a country"""
    AT = 'AT'
    BE = 'BE'
    BG = 'BG'
    CH = 'CH'
    CY = 'CY'
    CZ = 'CZ'
    DK = 'DK'
    EE = 'EE'
    EL = 'EL'
    ES = 'ES'
    FI = 'FI'
    FR = 'FR'
    HR = 'HR'
    HU = 'HU'
    IS = 'IS'
    IT = 'IT'
    LI = 'LI'
    LT = 'LT'
    LU = 'LU'
    LV = 'LV'
    MT = 'MT'
    NL = 'NL'
    NO = 'NO'
    PL = 'PL'
    PT = 'PT'
    RO = 'RO'
    SE = 'SE'
    SI = 'SI'
    SK = 'SK'
    DE = 'DE'
    DE_TOT = 'DE_TOT'
    AL = 'AL'
    IE = 'IE'
    ME = 'ME'
    MK = 'MK'
    RS = 'RS'
    AM = 'AM'
    AZ = 'AZ'
    GE = 'GE'
    TR = 'TR'
    UA = 'UA'
    BY = 'BY'
    UK = 'UK'
    XK = 'XK'
    FX = 'FX'
    MD = 'MD'
    SM = 'SM'
    RU = 'RU'
    EEA30_2007 = 'EEA30_2007'
    EU27_2007 = 'EU27_2007'
    EU27_2020 = 'EU27_2020'
    EEA31 = 'EEA31'
    EFTA = 'EFTA'
    EA18 = 'EA18'
    EA19 = 'EA19'
    EU28 = 'EU28'

    @classmethod
    def list_all_countries(cls) -> List[str]:
        """Lists all the values in an enum region"""
        group_countries = [
            cls.EEA30_2007,
            cls.EU27_2007,
            cls.EU27_2020,
            cls.EEA31,
            cls.EFTA,
            cls.EA18,
            cls.EA19,
            cls.EU28
        ]

        return [region.value for region in Region if region not in group_countries]

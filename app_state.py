import numpy as np
from backend.app_setup import AppSetup
from frontend.dictionaries import pl, eng

app = AppSetup(20,
               25,
               np.concatenate((np.full(5, 100),
                               np.full(20, 600))),
               np.concatenate((np.full(3, 50),
                               np.full(7, 150),
                               np.full(9, 300),
                               np.full(6, 500))),
               1.0,
               50,
               50,
               "COST",
               "roulette",
               0.6,
               "1-POINT",
               "SWAP",
            0.05,
               eng.dict_ENG)

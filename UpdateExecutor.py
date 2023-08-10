import threading
from main import correct_regNo
from Niid_Correction import correct_regNoNiid


def execute(POLICY_NUMBER, REG_NUMBER, INCORRECT_REGNUMBER):
    x = threading.Thread(target=correct_regNoNiid, args=(POLICY_NUMBER, REG_NUMBER,INCORRECT_REGNUMBER))

    y = threading.Thread(target=correct_regNo, args=(POLICY_NUMBER, REG_NUMBER,))

    x.start()
    y.start()

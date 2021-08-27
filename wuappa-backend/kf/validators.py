# -*- coding: utf-8 -*-
import re


class ValidateNifCif(object):

    def validate_nif(self, nif):
        """
        NIF validation
        nif: the nif to check
        :returns True if NIF is valid, else False
        """

        NIF_regExp = "^\\d{8}[a-zA-Z]{1}$"
        NIF_letters = "TRWAGMYFPDXBNJZSQVHLCKET"
        # First we check nif length. Older DNI could have 7 digits.
        if 9 < len(nif) or len(nif) < 8:
            return False

        if len(nif) == 8:
            nif = '0' + nif

        reg_exp = re.compile(NIF_regExp).findall(nif)
        if not len(reg_exp):
            return False

        char_letter = nif[-1]
        dni = nif[:-1]
        letter = NIF_letters[int(int(dni) % 23)]

        return letter == char_letter.upper()

    def validate_cif(self, cif):
        """
        CIF validation
        cif: the nif to check
        :returns True if CIF is valid, else False
        """

        CIF_regExp = "^[a-zA-Z]{1}\\d{7}[a-jA-J0-9]{1}$"

        # Check if format is correct
        reg_exp = re.compile(CIF_regExp).findall(cif.upper())
        if not len(reg_exp):
            return False  # Is format valid?

        if not re.compile("^[ABCDEFGHJKLMNPQRSUVW]").findall(cif.upper()):
            return False  # Is the letter allowed?

        num_a = 0
        num_b = 0
        for i in range(1, 8):
            if i % 2 == 0:
                num_a += int(cif[i])
            else:
                str_value = str(int(cif[i]) * 2)
                if len(str_value) == 1:
                    num_b += int(str_value)
                else:
                    num_b += int(str_value[0]) + int(str_value[1])

        num_c = num_a + num_b
        num_e = num_c % 10

        dc = 0 if num_e == 0 else 10 - num_e

        cif_last_char = cif.upper()[8]

        return (str(dc) == cif_last_char) or (dc == 1 and cif_last_char == 'A') or\
               (dc == 2 and cif_last_char == 'B') or (dc == 3 and cif_last_char == 'C') or\
               (dc == 4 and cif_last_char == 'D') or (dc == 5 and cif_last_char == 'E') or\
               (dc == 6 and cif_last_char == 'F') or (dc == 7 and cif_last_char == 'G') or\
               (dc == 8 and cif_last_char == 'H') or (dc == 9 and cif_last_char == 'I') or\
               (dc == 0 and cif_last_char == 'J')

    def validate_tr(self, tr):
        """
        TR validation (TR = Tarjeta Residencia)
        tr: the tr to check
        :returns True if TR is valid, else False
        """
        if len(tr) < 9 or len(tr) > 10:
            return False

        if tr.upper()[0] not in ["X", "Y", "Z"]:
            return False

        if tr.upper()[0] == "Y":
            left_number = '1'
        else:
            left_number = '0'

        if len(tr) == 9:
            return self.validate_nif(left_number + tr[1:])
        else:
            return self.validate_nif(tr[1:])


def validate_payment_account(account):
    """Validates if a payment account has a correct format"""
    if not account or (not len(account) == 20 and not len(account) == 24):
        return False

    # We will check control code
    try:
        cc = account[-20:]
        values = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
        control_cc = control_cs = 0
        for i in range(8):
            control_cs += int(cc[i]) * values[i + 2]
        control_cs = 11 - (control_cs % 11)

        if control_cs == 11:
            control_cs = 0
        elif control_cs == 10:
            control_cs = 1

        for i in range(10, 20):
            control_cc += int(cc[i]) * values[i - 10]
        control_cc = 11 - (control_cc % 11)

        if control_cc == 11:
            control_cc = 0
        elif control_cc == 10:
            control_cc = 1
        dc = control_cs + control_cc
        if dc != cc[8:10]:
            return False
    except Exception:
        return False

    # If account length == 20 we have to generate iban
    try:
        ccc = int(cc + "142800")
        iban = 98 - (ccc % 97)
    except Exception:
        return False

    if len(account) != 20 and account[:4] != "ES{:0>2d}".format(iban):
            return False
    return True

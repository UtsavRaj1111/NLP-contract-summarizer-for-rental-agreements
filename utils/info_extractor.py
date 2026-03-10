import re

def extract_agreement_info(text):

    info = {}

    clean = text.replace("\n", " ")

    # Rent amount
    rent_match = re.search(
        r"(rent[^₹\d]{0,20})(₹?\s?\d{3,7})",
        clean,
        re.IGNORECASE
    )

    if rent_match:
        info["Rent Amount"] = rent_match.group(2)

    # Duration
    duration_match = re.search(
        r"(\d{1,2}\s*(months?|years?))",
        clean,
        re.IGNORECASE
    )

    if duration_match:
        info["Agreement Duration"] = duration_match.group(1)

    # Security deposit
    deposit_match = re.search(
        r"(deposit[^₹\d]{0,20})(₹?\s?\d{3,7})",
        clean,
        re.IGNORECASE
    )

    if deposit_match:
        info["Security Deposit"] = deposit_match.group(2)

    return info
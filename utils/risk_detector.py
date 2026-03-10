def detect_clause_risk(clauses):

    risks = {}

    for clause, status in clauses.items():

        if "Missing" in status:
            risks[clause] = "High Risk"

        elif "Present" in status:
            risks[clause] = "Low Risk"

        else:
            risks[clause] = "Medium Risk"

    return risks
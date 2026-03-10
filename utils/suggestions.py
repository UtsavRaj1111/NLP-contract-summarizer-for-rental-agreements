def clause_suggestions(clauses):

    suggestions = {}

    for clause, status in clauses.items():

        if "Missing" in status:
            suggestions[clause] = (
                f"Consider adding a {clause} clause to improve agreement clarity."
            )

    return suggestions
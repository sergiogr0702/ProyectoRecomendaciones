def discretize_age(age):
    age_ranges = {
        (0, 17): 1,
        (18, 24): 18,
        (25, 34): 25,
        (35, 44): 35,
        (45, 49): 45,
        (50, 55): 50,
        (56, 120): 56
    }

    for (min_age, max_age), range_number in age_ranges.items():
        if min_age <= age <= max_age:
            return range_number

    return None


def discretize_ocupacion(ocupation):
    ocupation_ranges = [
        "other",
        "academic/educator",
        "artist",
        "clerical/admin",
        "college/grad student",
        "customer service",
        "doctor/health care",
        "executive/managerial",
        "farmer",
        "homemaker",
        "K-12 student",
        "lawyer",
        "programmer",
        "retired",
        "sales/marketing",
        "scientist",
        "self-employed",
        "technician/engineer",
        "tradesman/craftsman",
        "unemployed",
        "writer"
    ]

    if ocupation in ocupation_ranges:
        index = ocupation_ranges.index(ocupation)
    else:
        index = -1

    return index

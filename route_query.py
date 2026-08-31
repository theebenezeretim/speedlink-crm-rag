def detect_service(query):
    query = query.lower()

    service_keywords = {
        "workspace": [
    "workspace",
    "coworking",
    "office",
    "desk",
    "place to work",
    "somewhere to work",
    "work space",
    "workplace",
    "work station",

        ],
        "ftth internet": [
            "internet",
            "wifi",
            "wi-fi",
            "fiber",
            "fibre",
            "ftth",
            "broadband",
        ],
        "training": [
            "training",
            "course",
            "learn",
            "class",
            "certification",
        ],
        "pearson vue": [
            "pearson",
            "vue",
            "exam",
            "test center",
            "certification exam",
        ],
        "research": [
            "research",
            "thesis",
            "project topic",
            "literature review",
            "methodology",
            "data analysis",
        ],
    }

    for service, keywords in service_keywords.items():
        for keyword in keywords:
            if keyword in query:
                return service

    return "unknown"


if __name__ == "__main__":
    queries = [
        "I need somewhere to work for a few hours",
        "How much is your internet?",
        "I want to take a Python course",
        "Where can I write my Pearson VUE exam?",
        "I don't have a research topic",
    ]

    for query in queries:
        service = detect_service(query)

        print(f"Query: {query}")
        print(f"Detected service: {service}")
        print()
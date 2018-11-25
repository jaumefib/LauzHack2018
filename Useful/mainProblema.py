from Problem import NiceJourney
from mainAlgorisme import hill_climbing


def main():
    print("Starting program")
    # Activate the database
    problem = NiceJourney()
    res = hill_climbing(problem)
    # print the resulting graph


if __name__ == "__main__":
    main()

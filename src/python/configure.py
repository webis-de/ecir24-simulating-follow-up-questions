import os

import yaml

from constants import DATASETS, MODELS


def choose_datasets():
    available_dataset = list(sorted(DATASETS))
    chosen_datasets = []
    error_msg = None
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        if error_msg is not None:
            print(f"Error: {error_msg}")
            error_msg = None

        print(f"Available datasets:")
        for i in range(len(available_dataset)):
            print(f" {i + 1:d}. {available_dataset[i]}")
        print(f"Chosen: {chosen_datasets}")
        choice = input(f"Choose dataset (type associated number or 'x' to continue): ")

        if choice == "x":
            if len(chosen_datasets) == 0:
                error_msg = "No dataset chosen!"
                continue
            else:
                break

        try:
            choice = int(choice)
        except ValueError:
            error_msg = "Non-numeric input!"
            continue

        try:
            dataset = available_dataset[choice - 1]
            chosen_datasets.append(dataset)
            available_dataset.remove(dataset)
        except IndexError:
            error_msg = "Index out of bounds!"
            continue

    return chosen_datasets


def choose_models():
    available_models = list(sorted(MODELS.keys()))
    chosen_models = []
    error_msg = None
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        if error_msg is not None:
            print(f"Error: {error_msg}")
            error_msg = None

        print(f"Available models:")
        for i in range(len(available_models)):
            print(f" {i + 1:d}. {available_models[i]}")
        print(f"Chosen: {chosen_models}")
        choice = input(f"Choose model (type associated number or 'x' to continue): ")

        if choice == "x":
            if len(chosen_models) == 0:
                error_msg = "No model chosen!"
                continue
            else:
                break

        try:
            choice = int(choice)
        except ValueError:
            error_msg = "Non-numeric input!"
            continue

        try:
            dataset = available_models[choice - 1]
            chosen_models.append(dataset)
            available_models.remove(dataset)
        except IndexError:
            error_msg = "Index out of bounds!"
            continue

    return chosen_models


def main():
    datasets = choose_datasets()
    models = choose_models()

    os.system('cls' if os.name == 'nt' else 'clear')
    choice = input("Want to simulate user types [y/N]: ")

    simulate_user = "y" == choice.lower()

    data = {"datasets": datasets, "models": models, "simulate_user": simulate_user}

    with open("run.yml", "w") as out_file:
        yaml.dump(data, out_file)


if __name__ == '__main__':
    main()

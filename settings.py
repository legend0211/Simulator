def main():
    arr = []
    with open("settings.txt", "r") as file:
        for line in file:
            data = line.strip().split("=")
            arr.append(data[1].strip())

    return arr
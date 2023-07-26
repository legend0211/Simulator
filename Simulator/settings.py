def main():
    arr = []
    with open(r"C:\Users\soham\Desktop\Coding\Project\Simulator\Simulator\settings.txt", "r") as file:
        for line in file:
            data = line.strip().split("=")
            arr.append(data[1].strip())

    return arr
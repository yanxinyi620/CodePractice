import random


def get_bus_info(station):
    info = []
    for random_bus in range(10):
        bus_name = f"W{random.randint(1, 100)}"
        bus_arrival_time = random.randint(1, 30)
        bus_info = f"{bus_name} will arrive {station} in {bus_arrival_time} minutes."
        info.append({bus_name: bus_info})
    return info


if __name__=="__main__":
    for bus in get_bus_info('gaoxinnan'):
        print(bus)

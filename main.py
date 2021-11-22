from enum import Flag
from workshop import Workshop

def main():
    simulations_flag = False
    time_flag = False
    t = 480
    
    while not time_flag:
        try:
            t = int(input("Working day hours:"))
            t *= 60
            time_flag = True
        except ValueError:
            print("Hours must be an integer. Try again!")

    while not simulations_flag:
        try:
            n = int(input("Number of simulations: "))
            simulations_flag = True
        except ValueError:
            print("Number of simulations must be an integer. Try again!")


    profit_sum = 0
    client_sum = 0
    overtime_sum = 0
    overtime_count = 0
    for i in range(n):
        # print(f"------------ Simulation {i + 1} -------------")
        workshop = Workshop(t, 2, 3, 1)
        workshop.run()

        # print("*** Results: ***")
        # print("Total clients: ", workshop.client_count)
        # print("Total profit: ", workshop.profit)
        client_sum += workshop.client_count
        profit_sum += workshop.profit

        if workshop.current_time > t:
            overtime = workshop.current_time - t
            # print("There was an overtime of ", overtime)
            overtime_sum += overtime
            overtime_count += 1

    print("------------ Final results: ------------")
    print("Average profit: ", profit_sum / n)
    print("Average clients: ", client_sum / n)
    if overtime_count > 0:
        print("Average overtime: ", overtime_sum / overtime_count)
    else:
        print("There was no overtime")

if __name__ == "__main__":
    main()
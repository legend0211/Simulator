import settings, node, power, resource_allocation, global_arrays

nodes, receiver, fps, event_probability = settings.main()

sec = int(input("Enter the number of seconds : "))

for i in range(sec):
    node.main(int(fps), int(nodes))
    power.main(int(nodes), i, sec)
    resource_allocation.main(i)
import settings, node, power, resource_allocation

nodes, receiver, fps, event_probability, sec = settings.main()

print("Calculating...")
sec = int(sec)
for i in range(sec):
    print("Second",i+1)
    node.main(int(fps), int(nodes))
    power.main(int(nodes), i, sec)
    resource_allocation.main(i)
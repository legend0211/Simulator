import settings

nodes, _, _, _ = settings.main()

prediction_array = [[0] * int(nodes) for _ in range(86400)]

power_list = [0] * int(nodes)

camera_no = [i for i in range(1, int(nodes)+1)]
import settings

nodes, _, _, _, sec = settings.main()

prediction_array = [[0] * int(nodes) for _ in range(int(sec))]

power_list = [0] * int(nodes)

camera_no = [i for i in range(1, int(nodes)+1)]

count_pred = [0 for _ in range(int(nodes))]

value = 0
cnt = [0 for _ in range(int(nodes))]
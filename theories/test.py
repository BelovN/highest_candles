def get_count_for_point_in(capital, point_in, stop_loss):
    delta = abs(point_in - stop_loss)
    print(delta)
    one_percent = capital / 100
    print(one_percent)
    return int(one_percent / delta)


a = get_count_for_point_in(capital=200000, point_in=1150, stop_loss=1000)
print(a)

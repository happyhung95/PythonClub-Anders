def not_number(num):
    """To validate if input is number or not"""
    """Function is stored here to be able to import everywhere else"""
    try:
        int(num)
    except ValueError:
        print('Please enter only number\n')
        return True
    return False


class Database:
    num_player = 0
    dead_player = set()
    dead_computer = set()
    players = list()
    computers = list()
    sleep = 1.2  # sleep 1.2s for computer to think

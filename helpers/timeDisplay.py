# FUNCTIONS
def display(time_value, what):
    if time_value > 60:
        if time_value > 3600:
            hours = int(time_value) // 3600
            minutes = int(time_value) % 3600 // 60
            seconds = int(time_value) % 3600 % 60
            print(
                f'{what} is: {hours} hours, {minutes} minutes and {seconds} seconds!')
        else:
            minutes = int(time_value) // 60
            seconds = int(time_value) % 60
            print(f'{what} is: {minutes} minutes and {seconds} seconds!')
    else:
        print(f'{what} is: {time_value} seconds!')

__author__ = 'kalo'


class Events:
    set_pattern = 0
    start_game = 1
    end_game = 2
    first_sensor_hit = 3
    second_sensor_hit = 4
    third_sensor_hit = 5
    fourth_sensor_hit = 6
    player_error = 9
    player_start_labirinth = 10
    player_won = 11

    error = 100


class EventTypes:
    mcu_event = 7
    rfid_event = 8
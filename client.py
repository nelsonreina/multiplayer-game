from game import *

logging.basicConfig(filename='log.log', level=logging.DEBUG)


def main():


    print("----------------------------------------------------------------\n")
    print("-                                                              -\n")
    print("-                 Multiplayer Battleship Game                  -\n")
    print("-                                                              -\n")
    print("----------------------------------------------------------------\n")
    # network setup
    host = 'localhost'
    port = 5000
    last_shot_hit = False
    last_move = None
    player_won = False
    is_server = input("Do you want to be the host for the game? (y/n)").lower()[0] == "y"
    player_turn = not is_server

    if not is_server:
        host = input("Enter hostname or just hit enter for default parameters") or host
        port = int(input("Enter port or just hit enter for default parameters") or port)

    print("Starting Game!")

    with Network(host, port, is_server) as net:
        # init
        player_board = create_empty_board()
        enemy_board = create_empty_board()

        place_ships(player_board, enemy_board)

        print_boards(player_board, enemy_board)

        # game on
        while not player_lost(player_board):

            if player_turn:
                x, y, exit_ = ask_player_for_shot()
                if exit_:
                    break
                last_move = Shot(x, y, last_shot_hit)
                net.send(bytes(last_move))

            else:
                print("Waiting on other player...")
                data = net.recv()
                if not data:
                    player_won = True
                    break

                enemy_shot = Shot.decode(data)

                last_shot_hit = update_player_board(enemy_shot, player_board)

                if last_move:
                    last_move.last_shot_hit = enemy_shot.last_shot_hit
                    update_enemy_board(last_move, enemy_board)

            print_boards(player_board, enemy_board)
            player_turn = not player_turn

        if player_won:
            print("You won!")
        else:
            print("You lost!")


if __name__ == "__main__":
    main()

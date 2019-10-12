def is_legal_pair(player1, player2):
    return player1.test_legal_pairing(player2) and \
        player2.test_legal_pairing(player1)


def num_rounds(player_count, event_type="Competitive"):
    rounds = 3
    if event_type == "Competitive":
        if player_count > 9:
            rounds += 1
            if player_count > 32:
                rounds += 1
                if player_count > 56:
                    rounds += 1
                    if player_count > 80:
                        rounds += 1
                        if player_count > 128:
                            rounds += 1
                            if player_count > 192:
                                rounds += 1
                                if player_count > 256:
                                    rounds += 1
    if event_type == "Casual":
        if player_count > 11:
            rounds += 1
            if player_count > 15:
                rounds += 1
                if player_count > 32:
                    rounds += 1
                    if player_count > 64:
                        rounds += 1
                        if player_count > 96:
                            rounds += 1
                            if player_count > 128:
                                rounds += 1
    return rounds


def cut_size(player_count, event_type="Competitive"):
    cut_num: int = 0
    if event_type == "Competitive":
        if player_count > 15:
            cut_num += 4
            if player_count > 24:
                cut_num += 4
                if player_count > 128:
                    cut_num += 8
    if event_type == "Casual":
        if player_count > 15:
            cut_num += 4,
            if player_count > 32:
                cut_num += 4
                if player_count > 128:
                    cut_num += 8
    return cut_num

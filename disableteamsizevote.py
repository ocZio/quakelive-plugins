import minqlx


DISABLE_TEAMSIZE_VOTE_AFTER_ROUNDS = 10

class disableteamsizevote(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        self.teamsize_is_disabled = False

        self.add_hook('vote_called', self.handle_vote_called)
        self.add_hook('round_start', self.handle_round_start)
        self.add_hook('map', self.handle_map)

    def handle_map(self, *args, **kwargs):
        self.teamsize_is_disabled = False
        self.game.teamsize = 8

    def handle_vote_called(self, caller, vote, args):
        '''
        if the vote is for a teamsize and we have already played 10 rounds, just ignore this vote.
        '''
        if vote.lower() == 'teamsize' and self.teamsize_is_disabled:
            caller.tell('Voting teamsize is currently disabled, this happens when the game rounds are >%s' % DISABLE_TEAMSIZE_VOTE_AFTER_ROUNDS)
            return minqlx.RET_STOP_ALL

        return minqlx.RET_NONE
    
    def handle_round_start(self, *args, **kwargs):
        rounds = self.game.red_score + self.game.blue_score
        if rounds > DISABLE_TEAMSIZE_VOTE_AFTER_ROUNDS:
            teams = self.teams()
            max_teamsize = min(len(teams['red']), len(teams['blue']))

            if max_teamsize > 0:
                self.game.teamsize = max_teamsize
                self.teamsize_is_disabled = True
        else:
            self.teamsize_is_disabled = False


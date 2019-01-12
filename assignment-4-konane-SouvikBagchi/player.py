import game_rules, random
import pdb

###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): 
    	super(MinimaxPlayer, self).__init__(symbol)
    	self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def change_player(self,symbol):
        if symbol == 'o':
            return 'x'
        else :
            return 'o'

    # Edit this one here. :)
    def getMove(self, board):
 
        player = self.symbol

        utility_move = [NEG_INF,None]

        curr_depth = self.depth

        # print("getMove utility_move_board : {}".format(utility_move))

        make_move_list = self.max_value(board,player,curr_depth)


        return make_move_list[1]


    def max_value(self, board, player, curr_depth): 
   
        #check if the max depth is reached - then return the utility function
        if curr_depth == 0:
            new_utility = self.h1(board,player)
            new_utility_move = [new_utility, None]
            return new_utility_move
        curr_depth = curr_depth -1
        available_moves = game_rules.getLegalMoves(board, player)
        #check if it is a leaf node -> return utility function
        if len(available_moves) ==0 :
            new_utility = self.h1(board,player)
            new_utility_move = [new_utility, None]
            return new_utility_move
        
        check_utility = [NEG_INF,None] 
        for move in available_moves :

            new_player = self.change_player(player)
            new_board= game_rules.makeMove(board,move)
            new_utility = self.min_value(new_board,new_player,curr_depth)

            #check if the utility returned is greater than the current utility
            #update the utility and the move associated with that 
            if new_utility[0]>check_utility[0]:
                check_utility[0] = new_utility[0]
                check_utility[1] =move

        return check_utility

    def min_value(self, board, player, curr_depth):
 
        if curr_depth == 0:
            new_utility = self.h1(board,player)
            new_utility_move = [new_utility, None]
            return new_utility_move
        curr_depth = curr_depth -1

        available_moves = game_rules.getLegalMoves(board, player)
        if len(available_moves) ==0 :
            new_utility = self.h1(board,player)
            new_utility_move = [new_utility, None]
            return new_utility_move

        check_utility = [POS_INF,None]
        for move in available_moves :
            new_player = self.change_player(player)
            new_board = game_rules.makeMove(board,move)
            new_utility = self.max_value(new_board,new_player,curr_depth)

            if new_utility[0]<check_utility[0]:
                check_utility[0] = new_utility[0]
                check_utility[1] =move
                
        return check_utility


# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def change_player(self,symbol):
        if symbol == 'o':
            return 'x'
        else :
            return 'o'

    # Edit this one here. :)

    def getMove(self, board):
 
        player = self.symbol

        utility_move = [NEG_INF,None]

        curr_depth = self.depth

        # print("getMove utility_move_board : {}".format(utility_move))

        make_move_list = self.max_value_alpha_beta(board,player,curr_depth,NEG_INF,POS_INF)


        return make_move_list[1]



    def max_value_alpha_beta(self, board, player, curr_depth,alpha,beta): 
   
        if curr_depth == 0:
            new_utility = self.h1(board,player)
            new_utility_move = [new_utility, None]
            return new_utility_move
        curr_depth = curr_depth -1
        available_moves = game_rules.getLegalMoves(board, player)
        if len(available_moves) ==0 :
            new_utility = self.h1(board,player)
            new_utility_move = [new_utility, None]
            return new_utility_move
        
        check_utility = [NEG_INF,None] 
        for move in available_moves :

            new_player = self.change_player(player)
            new_board= game_rules.makeMove(board,move)
            new_utility = self.min_valuealpha_beta(new_board,new_player,curr_depth,alpha,beta)

            if new_utility[0]>check_utility[0]:
                check_utility[0] = new_utility[0]
                check_utility[1] =move

            alpha = max(alpha,new_utility[0])            
            if alpha>=beta:
                break

        return check_utility

    def min_valuealpha_beta(self, board, player, curr_depth, alpha,beta):
 
        if curr_depth == 0:
            new_utility = self.h1(board,player)
            new_utility_move = [new_utility, None]
            return new_utility_move
        curr_depth = curr_depth -1

        available_moves = game_rules.getLegalMoves(board, player)
        if len(available_moves) ==0 :
            new_utility = self.h1(board,player)
            new_utility_move = [new_utility, None]
            return new_utility_move

        check_utility = [POS_INF,None]
        for move in available_moves :
            new_player = self.change_player(player)
            new_board = game_rules.makeMove(board,move)
            new_utility = self.max_value_alpha_beta(new_board,new_player,curr_depth,alpha,beta)

            if new_utility[0]<check_utility[0]:
                check_utility[0] = new_utility[0]
                check_utility[1] =move

            beta = min(beta,new_utility[0])            
            if alpha>=beta:
                break
                
        return check_utility


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)

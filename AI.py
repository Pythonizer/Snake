
from Settings import BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE


class AI(object):
    def __init__(self, snake, food_dispatcher):
        self._snake = snake
        self._food_dispatcher = food_dispatcher
        self._last_move_direction = None

    def _right_wall(self):
        return self._snake.get_head_position()[0] >= WINDOW_SIZE[0] - BLOCKSIZE - BORDER_SIZE

    def _left_wall(self):
        return self._snake.get_head_position()[0] <= BORDER_SIZE

    def _upper_wall(self):
        return self._snake.get_head_position()[1] <= 2*BLOCKSIZE

    def _lower_wall(self):
        return self._snake.get_head_position()[1] >= WINDOW_SIZE[1] - 3*BLOCKSIZE

    def _lower_wall_with_space(self):
        return self._snake.get_head_position()[1] >= WINDOW_SIZE[1] - 4*BLOCKSIZE

    def tryout(self):
        if self._snake.get_move_direction() == 'right':
            #print "right -> up"
            self._snake.update_move_direction('up')
        elif self._snake.get_move_direction() == 'left':
            #print "left -> down"
            self._snake.update_move_direction('down')
        elif self._snake.get_move_direction() == 'down':
            #print "down -> right"
            self._snake.update_move_direction('right')
        elif self._snake.get_move_direction() == 'up':
            #print "up -> left"
            self._snake.update_move_direction('left')
        else:
            self._snake.update_move_direction('right')

    def tryout_wall(self):
        if not self._snake.get_move_direction():
            self._snake.update_move_direction('right')

        if self._left_wall():
            if self._snake.get_move_direction() == 'left':
                self._snake.update_move_direction('down')

        if self._right_wall():
            if self._snake.get_move_direction() == 'right':
                self._snake.update_move_direction('up')

        if self._upper_wall():
            if self._snake.get_move_direction() == 'up':
                self._snake.update_move_direction('left')

        if self._lower_wall():
            if self._snake.get_move_direction() == 'down':
                self._snake.update_move_direction('right')

    def simple_walk(self):
        if not self._snake.get_move_direction():
            self._snake.update_move_direction('right')
            self._last_move_direction = 'right'

        if self._right_wall():
            if self._snake.get_move_direction() == 'right':
                self._last_move_direction = 'right'
                self._snake.update_move_direction('up')
                return

        if self._upper_wall():
            if self._snake.get_move_direction() == 'up':
                if self._last_move_direction == 'left':
                    self._snake.update_move_direction('left')
                    return
                elif self._last_move_direction == 'right':
                    if not self._right_wall():
                        self._snake.update_move_direction('right')
                    else:
                        self._snake.update_move_direction('left')
                self._last_move_direction = 'up'

            elif self._snake.get_move_direction() == 'left':
                self._last_move_direction = 'left'
                self._snake.update_move_direction('down')
                return

        if self._left_wall():
            print "LLL"
            if self._snake.get_move_direction() == 'down':
                pass
                print "DDD"
                if self._lower_wall():
                    self._last_move_direction = 'down'
                    self._snake.update_move_direction('right')
                    print "RRRRRRRRRRRRRR"
                    return
            elif self._snake.get_move_direction() == 'right':
                self._last_move_direction = 'right'
                self._snake.update_move_direction('up')
                return

        if self._lower_wall_with_space():
            print "LS"
            if self._snake.get_move_direction() == 'down':
                print "***LSD***"
                if not self._left_wall():
                    self._last_move_direction = 'down'
                    self._snake.update_move_direction('left')
                else:
                    return
                    #self._snake.update_move_direction('right')
            elif self._snake.get_move_direction() == 'left':
                self._last_move_direction = 'left'
                self._snake.update_move_direction('up')


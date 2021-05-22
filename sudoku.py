import numpy as np


def dfs(cb, dep):
    if not np.any(cb == 0):
        print('Solved at %d-th depth' % dep)
        print(cb)
        return

    pos = np.argwhere(cb == 0)[0]

    for val in range(1, 10):
        if check(cb, pos, val):
            cb[pos[0], pos[1]] = val
            dfs(cb, dep+1)
            cb[pos[0], pos[1]] = 0

    # raise ValueError('\n'+str(cb)+ '\n'+ str(pos))


def check(cb, pos, val):
    if val in cb[pos[0], :] or val in cb[:, pos[1]]:
        return False

    start_row, start_col = int(pos[0] / 3) * 3, int(pos[1] / 3) * 3
    if val in cb[start_row:start_row+3, start_col:start_col+3]:
        return False
    return True


def main():
    chessboard = np.array([
        [2, 0, 3, 4, 0, 0, 0, 9, 0],
        [0, 0, 0, 1, 0, 2, 0, 0, 5],
        [5, 0, 6, 0, 0, 0, 1, 0, 0],
        [0, 2, 0, 5, 0, 0, 8, 1, 0],
        [9, 8, 1, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 1, 9, 2, 0, 0],
        [4, 3, 0, 0, 8, 0, 0, 0, 1],
        [0, 9, 0, 0, 5, 0, 6, 0, 0],
        [0, 0, 0, 0, 2, 1, 0, 5, 4]
    ])
    visit = chessboard.copy()
    visit[visit != 0] = 1
    pos = np.argwhere(chessboard == 0)
    dfs(chessboard, 0)


if __name__ == '__main__':
    main()

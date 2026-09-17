class Boggle:
    def __init__(self, grid, dictionary):
        # save the grid + dict, start with no solution
        self.grid = grid
        self.dictionary = dictionary
        self.solution = []

    def setGrid(self, grid):
        # set the grid
        self.grid = grid

    def setDictionary(self, dictionary):
        # set the dictionary
        self.dictionary = dictionary

    def getSolution(self):
        # returns found words, or [] if nothing found or bad input
        self.solution = []

        # bail out on bad input
        if not self._is_valid_grid() or not self._is_valid_dictionary():
            return []

        # lowercase the whole board so matching doesn't care about case
        rows = len(self.grid)
        cols = len(self.grid[0])
        board = [[self.grid[r][c].lower() for c in range(cols)] for r in range(rows)]

        # words = real words (3+ letters). prefixes = every start of a word,
        # so we can quit a dead-end path early
        words = set()
        for w in self.dictionary:
            w = w.lower()
            if len(w) >= 3:
                words.add(w)

        prefixes = set()
        for w in words:
            for i in range(1, len(w) + 1):
                prefixes.add(w[:i])

        found = set()

        # kick off a search from every tile
        for r in range(rows):
            for c in range(cols):
                visited = [[False] * cols for _ in range(rows)]
                self._search(board, r, c, "", visited, words, prefixes, found)

        self.solution = list(found)
        return self.solution

    def _search(self, board, r, c, path, visited, words, prefixes, found):
        # dfs from tile (r,c). path is what earlier tiles spelled
        rows = len(board)
        cols = len(board[0])

        # add this tile. note it might be 2 chars like "qu"
        current = path + board[r][c]

        # dead end, this can't start any word
        if current not in prefixes:
            return

        visited[r][c] = True

        # got a real word? save it
        if current in words:
            found.add(current)

        # check all 8 neighbors
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                    self._search(board, nr, nc, current, visited, words, prefixes, found)

        # free the tile back up
        visited[r][c] = False

    def _is_valid_grid(self):
        # grid has to be a non-empty square of non-empty strings
        if not self.grid or not isinstance(self.grid, list):
            return False
        n = len(self.grid)
        for row in self.grid:
            if not isinstance(row, list) or len(row) != n:
                return False
            for tile in row:
                if not isinstance(tile, str) or tile == "":
                    return False
        return True

    def _is_valid_dictionary(self):
        # dict just needs to be a non-empty list
        if not self.dictionary or not isinstance(self.dictionary, list):
            return False
        return True


def main():
    grid = [["A", "B", "C", "D"],
            ["E", "F", "G", "H"],
            ["Ie", "J", "K", "L"],
            ["A", "B", "C", "D"]]
    dictionary = ["ABEF", "AFJIEB", "DGKD", "DGKA"]

    mygame = Boggle(grid, dictionary)
    print(mygame.getSolution())


if __name__ == "__main__":
    main()
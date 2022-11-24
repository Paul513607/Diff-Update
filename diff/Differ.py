class Differ:
    file1: str
    file2: str
    file1_lines: list
    file2_lines: list
    path: list

    sequence_matrix: list
    flags: set
    operations: list
    diff: list

    def __init__(self, file1: str, file2: str):
        self.file1 = file1
        self.file2 = file2
        self.file1_lines = []
        self.file2_lines = []

        self.path = []

        self.sequence_matrix = []
        self.flags = set()
        self.operations = []
        self.diff = []

        self.load()

    def __str__(self):
        return f'Differ({self.file1}, {self.file2})'

    def load(self):
        with open(self.file1, 'rb') as f:
            self.file1_lines = [line.rstrip().decode('utf-8') for line in f.readlines()]
        with open(self.file2, 'rb') as f:
            self.file2_lines = [line.rstrip().decode('utf-8') for line in f.readlines()]

    def fill_sequence_matrix(self):
        n, m = len(self.file1_lines), len(self.file2_lines)
        self.sequence_matrix = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if self.file1_lines[i - 1] == self.file2_lines[j - 1]:
                    self.sequence_matrix[i][j] = self.sequence_matrix[i - 1][j - 1] + 1
                    self.flags.add((i, j))
                else:
                    self.sequence_matrix[i][j] = max(self.sequence_matrix[i - 1][j], self.sequence_matrix[i][j - 1])

    def reconstruct_path(self):
        i, j = len(self.file1_lines), len(self.file2_lines)
        self.operations = []
        path = [(i, j)]
        while True:
            if i <= 0 and j <= 0:
                break
            if (i, j) in self.flags:
                i, j = i - 1, j - 1
                path.append((i, j))
                self.operations.append(('equal', self.file1_lines[i], i, j))
            elif self.sequence_matrix[i][j] == self.sequence_matrix[i - 1][j] and i > 0:
                i, j = i - 1, j
                path.append((i, j))
                self.operations.append(('delete', self.file1_lines[i], i, j))
            elif self.sequence_matrix[i][j] == self.sequence_matrix[i][j - 1] and j > 0:
                i, j = i, j - 1
                path.append((i, j))
                self.operations.append(('insert', self.file2_lines[j], i, j))
        path.reverse()
        self.path = path
        self.operations.reverse()

    def format_diff(self):
        for op, line, x, y in self.operations:
            if op == 'equal':
                self.diff.append(f' {line}')
            elif op == 'insert':
                self.diff.append(f'+{line}')
            elif op == 'delete':
                self.diff.append(f'-{line}')

    def get_diff_queue(self):
        self.diff_queue = []
        x_prev, y_prev = 0, 0
        for x, y, line in self.longest_matching_path:
            if x == 0 and y == 0:
                continue
            if x_prev == x:
                self.diff_queue.append(('insert', line, x, y))
            elif y_prev == y:
                self.diff_queue.append(('delete', line, x, y))
            else:
                self.diff_queue.append(('equal', line, x, y))
            x_prev, y_prev = x, y
        [print(x) for x in self.diff_queue]
        print('-----------------')
        #self.squash_operations()

    def squash_operations(self):
        op = self.diff_queue[0][0]
        i = 0
        new_diff_queue = []
        while True:
            if i >= len(self.diff_queue):
                break
            j = i
            curr_lines = []
            while op == 'equal' and j < len(self.diff_queue):
                curr_lines.append(self.diff_queue[j][1])
                j += 1
                op = self.diff_queue[j][0]
            if j != i:
                new_diff_queue.append(('equal', curr_lines.copy(), (self.diff_queue[i][2], self.diff_queue[j][2]),
                                       (self.diff_queue[i][3], self.diff_queue[j][3])))
            i = j
            curr_lines = []
            has_insert = False
            has_delete = False
            while op != 'equal' and j < len(self.diff_queue):
                if op == 'insert':
                    has_insert = True
                elif op == 'delete':
                    has_delete = True
                curr_lines.append(self.diff_queue[j][1])
                j += 1
                op = self.diff_queue[j][0]

            if j != i:
                if has_insert and not has_delete:
                    new_diff_queue.append(('insert', curr_lines.copy(), (self.diff_queue[i][2], self.diff_queue[i][2]),
                                           (self.diff_queue[i][3], self.diff_queue[j][3])))
                elif has_delete and not has_insert:
                    new_diff_queue.append(('delete', curr_lines.copy(), (self.diff_queue[i][2], self.diff_queue[j][2]),
                                           (self.diff_queue[i][3], self.diff_queue[i][3])))
                else:
                    new_diff_queue.append(('change', curr_lines.copy(), (self.diff_queue[i][2], self.diff_queue[j][2]),
                                           (self.diff_queue[i][3], self.diff_queue[j][3])))
            i = j
        [print(x) for x in new_diff_queue]

    # Myers Diff algorithm
    def shortest_edit(self):
        n, m = len(self.file1_lines), len(self.file2_lines)
        maximum = n + m

        v = [None] * (2 * maximum + 1)
        v[1] = 0
        history = []

        for d in range(0, maximum + 1):
            history.append(v.copy())
            for k in range(-d, d + 1, 2):
                if k == -d or k != d and v[k - 1] < v[k + 1]:
                    x = v[k + 1]
                else:
                    x = v[k - 1] + 1
                y = x - k
                while x < n and y < m and self.file1_lines[x] == self.file2_lines[y]:
                    x = x + 1
                    y = y + 1
                v[k] = x
                if x >= n and y >= m:
                    return history

    def backtrack(self):
        x, y = len(self.file1_lines), len(self.file2_lines)
        history = self.shortest_edit()
        for d, v in reversed(list(enumerate(history))):
            k = x - y
            if k == -d or k != d and v[k - 1] < v[k + 1]:
                k_prev = k + 1
            else:
                k_prev = k - 1
            x_prev = v[k_prev]
            y_prev = x_prev - k_prev

            while x > x_prev and y > y_prev:
                self.path.append(((x - 1, y - 1), (x, y)))
                x = x - 1
                y = y - 1

            if d > 0:
                self.path.append(((x_prev, y_prev), (x, y)))
                x, y = x_prev, y_prev

    def get_diff(self):
        self.diff = []
        self.path.reverse()
        for (x_prev, y_prev), (x, y) in self.path:
            if x_prev == x:
                self.diff.append((self.file2_lines[y_prev], x_prev, y_prev, 'insert'))
            elif y_prev == y:
                self.diff.append((self.file1_lines[x_prev], x_prev, y_prev, 'delete'))
            else:
                self.diff.append((self.file1_lines[x_prev], x_prev, y_prev, 'equal'))
        return self.diff

    def squash_diff(self):
        self.get_diff()
        result = []
        for i in range(len(self.diff)):
            if self.diff[i][3] == 'equal':
                continue
            if i < len(self.diff) - 1 and self.diff[i + 1][3] == 'equal':
                result.append(self.diff[i])
            elif i > 0 and self.diff[i - 1][3] == 'equal':
                result.append(self.diff[i])
            else:
                result.append(self.diff[i])
        return result

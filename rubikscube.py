from numpy import array as narray
from numpy import rot90


class Piece:
    """One piece of Rubik's cube (virtually)"""

    _vectors = []
    _colors = []

    """Creates new Piece object with given sides(vectors) and their colors"""
    def __init__(self, vectors, colors):
        if len(vectors) != len(colors):
            raise Exception("Vectors and Colors not of same length")
        self._vectors = vectors
        self._colors = colors

    """Rotates all vectors by given axis"""
    def rotate(self, axis):
        a = axis[0]
        b = axis[1]
        for v in self._vectors:
            v[a], v[b] = v[b] * -1, v[a]

    """Returns face of given vector"""
    def face(self, vector):
        try:
            ret = self._colors[self._vectors.index(vector)]
        except ValueError:
            return '-'  # + '---'
        return ret

    def __str__(self):
        return str(self._vectors) + '\n' + str(self._colors)

    def __repr__(self):
        return str(self._vectors) + '\n' + str(self._colors)


class RubiksCube:
    """RubiksCube"""

    _rotations = {  # rotation: slice index, slice start end, rotation axis, rotation count
        "x":  [2, (None, None), (0, 1), 1],
        "x2": [2, (None, None), (0, 1), 2],
        "x'": [2, (None, None), (1, 0), 1],
        "R":  [2, (2, 3),       (0, 1), 1],
        "R2": [2, (2, 3),       (0, 1), 2],
        "R'": [2, (2, 3),       (1, 0), 1],
        "M":  [2, (1, 2),       (1, 0), 1],
        "M2": [2, (1, 2),       (1, 0), 2],
        "M'": [2, (1, 2),       (0, 1), 1],
        "L":  [2, (0, 1),       (1, 0), 1],
        "L2": [2, (0, 1),       (1, 0), 2],
        "L'": [2, (0, 1),       (0, 1), 1],
        "r":  [2, (1, 3),       (0, 1), 1],
        "r2": [2, (1, 3),       (0, 1), 2],
        "r'": [2, (1, 3),       (1, 0), 1],
        "l":  [2, (0, 2),       (1, 0), 1],
        "l2": [2, (0, 2),       (1, 0), 2],
        "l'": [2, (0, 2),       (0, 1), 1],

        "y":  [0, (None, None), (1, 2), 1],
        "y2": [0, (None, None), (1, 2), 2],
        "y'": [0, (None, None), (2, 1), 1],
        "D":  [0, (2, 3),       (1, 2), 1],
        "D2": [0, (2, 3),       (1, 2), 2],
        "D'": [0, (2, 3),       (2, 1), 1],
        "E":  [0, (1, 2),       (2, 1), 1],
        "E2": [0, (1, 2),       (2, 1), 2],
        "E'": [0, (1, 2),       (1, 2), 1],
        "U":  [0, (0, 1),       (2, 1), 1],
        "U2": [0, (0, 1),       (2, 1), 2],
        "U'": [0, (0, 1),       (1, 2), 1],
        "d":  [0, (1, 3),       (1, 2), 1],
        "d2": [0, (1, 3),       (1, 2), 2],
        "d'": [0, (1, 3),       (2, 1), 1],
        "u":  [0, (0, 2),       (2, 1), 1],
        "u2": [0, (0, 2),       (2, 1), 2],
        "u'": [0, (0, 2),       (1, 2), 1],

        "z":  [1, (None, None), (2, 0), 1],
        "z2": [1, (None, None), (2, 0), 2],
        "z'": [1, (None, None), (0, 2), 1],
        "F":  [1, (2, 3),       (2, 0), 1],
        "F2": [1, (2, 3),       (2, 0), 2],
        "F'": [1, (2, 3),       (0, 2), 1],
        "S":  [1, (1, 2),       (0, 2), 1],
        "S2": [1, (1, 2),       (0, 2), 2],
        "S'": [1, (1, 2),       (2, 0), 1],
        "B":  [1, (0, 1),       (0, 2), 1],
        "B2": [1, (0, 1),       (0, 2), 2],
        "B'": [1, (0, 1),       (2, 0), 1],
        "f":  [1, (1, 3),       (2, 0), 1],
        "f2": [1, (1, 3),       (2, 0), 2],
        "f'": [1, (1, 3),       (0, 2), 1],
        "b":  [1, (0, 2),       (0, 2), 1],
        "b2": [1, (0, 2),       (0, 2), 2],
        "b'": [1, (0, 2),       (2, 0), 1],
    }

    def __init__(self):

        vector_color = {
            str([1, 0, 0]): "W",
            str([0, -1, 0]): "G",
            str([0, 0, -1]): "R",
            str([0, 1, 0]): "B",
            str([0, 0, 1]): "O",
            str([-1, 0, 0]): "Y",
        }

        cube = []

        pos = [0, 0, 0]

        for pos[0] in range(3):
            cube.append([])
            for pos[1] in range(3):
                cube[pos[0]].append([])
                for pos[2] in range(3):
                    vectors = []
                    colors = []
                    for i, p in enumerate(pos):
                        if p == 0 or p == 2:
                            vect = [0 if x != i else 1 if p == 0 else -1 for x in range(3)]
                            vectors.append(vect)
                            col = vector_color[str(vect)]  # + str(pos[0]) + str(pos[1]) + str(pos[2])
                            colors.append(col)
                    if len(vectors) > 0:
                        cube[pos[0]][pos[1]].append(Piece(vectors, colors))
                    else:
                        cube[pos[0]][pos[1]].append(None)
        self._cube = narray(cube)

    def __str__(self):
        row = ['', '', '', '', '', '', '', '', '', '', '']
        for i, piece1 in enumerate(self._cube[0, :, :]):  # white
            row[i] += '       '  # + '         '
            for piece in piece1:
                row[i] += piece.face([1, 0, 0])
                row[i] += ' '

        for i, piece1 in enumerate(self._cube[:, :, 0]):  # orange
            for piece in piece1:
                row[i+4] += piece.face([0, 0, 1])
                row[i + 4] += ' '
            row[i + 4] += ' '

        for i, piece1 in enumerate(self._cube[:, 2, :]):  # green
            for piece in piece1:
                row[i+4] += piece.face([0, -1, 0])
                row[i + 4] += ' '
            row[i + 4] += ' '

        for i, piece1 in enumerate(self._cube[:, ::-1, 2]):  # red
            for piece in piece1:
                row[i+4] += piece.face([0, 0, -1])
                row[i + 4] += ' '
            row[i + 4] += ' '

        for i, piece1 in enumerate(self._cube[:, 0, ::-1]):  # blue
            for piece in piece1:
                row[i+4] += piece.face([0, 1, 0])
                row[i + 4] += ' '

        for i, piece1 in enumerate(self._cube[2, ::-1, :]):  # yellow
            row[i + 8] += '       '  # + '         '
            for piece in piece1:
                row[i + 8] += piece.face([-1, 0, 0])
                row[i + 8] += ' '

        return '\n'+'\n'.join(row)

    def __repr__(self):
        return self.__str__()

    """Creates tokens from given algo"""
    def _tokenize(self, algo):
        algo = algo.replace(" ", "")
        funcs = []
        val = ""
        for c in algo:
            if (len(val) == 1 and c != "2" and c != "'") or len(val) == 2:
                funcs.append(val)
                val = ""
            val += c
        if val != "":
            funcs.append(val)
        return funcs

    """Executes given algo"""
    def e(self, algo):
        funcs = self._tokenize(algo)
        for f in funcs:
            self.rotate(f)

    """Perform single rotation"""
    def rotate(self, rotation):
        s = [slice(None, None), slice(None, None), slice(None, None)]
        s[self._rotations[rotation][0]] = slice(self._rotations[rotation][1][0], self._rotations[rotation][1][1])
        self._rotate(self._rotations[rotation][2], slices=s, k=self._rotations[rotation][3])

    def _rotate(self, axes, slices, k=1):
        self._cube[slices[0], slices[1], slices[2]] = rot90(self._cube[slices[0], slices[1], slices[2]], k=k, axes=axes)
        for piece in self._cube[slices[0], slices[1], slices[2]].ravel():
            if piece is not None:
                for i in range(k):
                    piece.rotate(axes)

from fractions import Fraction as frac
from fractions import gcd

def solution(m):

    #Handle edge case where matrix is 1x1 and cannot transition anywhere
    if len(m) == 1:
        return[1,1]

    mat = sort(m)
    mat = cast_to_probability_matrix(mat)
    Q, R = extract_Q_and_R(mat)
    I = build_I(len(Q))
    N = I - Q
    N = N.invert()
    M = N * R
    probabilities = M[0]
    lcm = lcd(probabilities) 
    return [p.numerator * lcm/p.denominator for p in probabilities] + [lcm]

def lcd(fractions):
    """Find the lowest common denominator from a list of fractions"""
    denoms = [f.denominator for f in fractions]
    lcm = denoms[0]
    for denom in denoms[1:]:
        lcm = denom*lcm/gcd(denom, lcm)
    return lcm

def sort(mat):
    """Re-order the rows in the matrix such that the absorbent ones come last"""
    for i in reversed(range(len(mat))):
        if reduce((lambda x,y : x + y), mat[i]) != 0: #if row is not empty
            for j in reversed(range(i)):
                if reduce((lambda x,y : x + y), mat[j]) == 0: #if row is empty
                    swap_rows(mat, i, j)
                    break
    return mat

def swap_rows(mat, x, y):
    """Swap rows x and y as well as the xth and yth columns"""
    mat[x], mat[y] = mat[y], mat[x]
    for row in mat:
        row[x], row[y] = row[y], row[x]
    return mat
        
def cast_to_probability_matrix(m):
    """Takes the input matrix and casts each row to a probabilistic representation with fractions
    where the total of each row is calculated and each entry in the row represents it's fraction of the total"""
    m_new = []
    for i in range(len(m)):
        row_sum = reduce((lambda x,y : x + y), m[i])
        if row_sum > 0:
            m_new.append(map((lambda x: frac(x, row_sum)), m[i]))
        else:
            m_new.append(map((lambda x: frac(x, 1)), m[i]))

    return matrix(m_new)

def transpose_matrix(m):
    """Transpose the matrix (switch columns and rows)"""
    transpose = []
    for i in range(len(m)):
        transpose.append(m.get_col(i))
    return matrix(transpose)

def calc_determinant(mat):
    """Calculate the determinant of the matrix"""
    x, y = mat.shape()
    if x != y:
        raise Exception("Cannot find deteminant of non-square matrix")
    if x == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    
    return reduce((lambda a,b : a + b), [mat[0][z] * ((-1) ** z) * calc_determinant(reduce_matrix(mat, 0, z)) for z in range(x)])

def build_I(size):
    """Build an identity matrix of dimensions (size, size)"""
    mat = []
    for i in range(size):
        row = []
        for j in range(size):
            if i==j: 
                row.append(1)
            else:
                row.append(0)
        mat.append(row)
    return matrix(mat)

def extract_Q_and_R(m):
    """Extract (Q,R) where Q shows the probability of moving from a non-absorbing state to another non-absorbing state
    and R shows the probability of moving from a non-absorbing state to and absorbing one"""
    mat = []
    for i in range(len(m)):
        if reduce((lambda a,b : a + b), m[i]) == 0:
            return matrix([m[j][:i] for j in range(i)]), matrix([m[j][i:] for j in range(i)])
    raise Exception("No absorbing states")

def reduce_matrix(mat, x, y):
    """Remove row x and column y from matrix"""
    return matrix([row[:y] + row[y+1:] for row in (mat[:x]+mat[x+1:])])

class matrix: 
    def __init__(self, matrix):
        """Construct a matrix consisting of a list of vectors out of a 2d list"""
        if type(matrix) != list or (type(matrix[0]) != list and not isinstance(matrix[0], vector)):
            raise Exception("Expected 2d list in matrix constructor")

        self.matrix = [vector(row) for row in matrix]

        for row in matrix[1:]:
            if len(matrix[0]) != len(row):
                raise Exception("Invalid matrix - rows of unequal length")

    def invert(self):
        """Find inverse of this matrix"""
        m = self.copy()
        size = len(m)
        det = calc_determinant(m)

        if det == 0:
            raise Exception("Zero determinant - cannot invert matrix")

        if size == 2:
            return matrix([[m[1][1]/det, -1*m[0][1]/det], [-1*m[1][0]/det, m[0][0]/det]])

        cf = []
        for r in range(size):
            row = []
            for c in range(size):
                minor = reduce_matrix(m,r,c)
                row.append(((-1)**(r+c)) * calc_determinant(minor))
            cf.append(row)
        cf = transpose_matrix(matrix(cf))
        for r in range(len(cf)):
            for c in range(len(cf)):
                cf[r][c] = cf[r][c]/det
        return cf

    def copy(self):
        """Make deep copy"""
        return matrix([row.copy() for row in self.matrix])
            
    def scale(self, scalar):
        """Multiply entire matrix by a scalar"""
        return matrix([row*scalar for row in self.matrix])

    def matrix_mul(self, other):
        """Multiply two matrices together, in order [self.matrix] * [other.matrix]"""
        if len(self.matrix[0]) != len(other.matrix):
            raise Exception("Invalid matrix operation - size mismatch")
        m = []
        o_x, o_y = other.shape()
        for row in self.matrix:
            m.append([reduce((lambda x,y : x + y), row * other.get_col(i)) for i in range(o_y)])     
        return matrix(m)

    def __sub__(self, other):
        """Subtract another matrix from this matrix (elementwise)"""
        return matrix([self[i] - other[i] for i in range(len(self))])

    def __mul__(self, other):
        """Scalar or matrix multiplication"""
        if(type(other) == int or type(other) == frac or type(other) == float):
            return self.scale(other)
        
        return self.matrix_mul(other)
    
    def __getitem__(self, index):
        """Get the row at the specified index"""
        return self.matrix[index]
    
    def __setitem__(self, index, val):
        """Set the row at the specified index"""
        self.matrix[index] = val
        return self
    
    def __eq__(self, other):
        if self.shape() != other.shape():
            return False
        for i in range(len(self.matrix)):
            if not self[i] == other[i]:
                return False
        return True

    def get_col(self, index):
        """Extract a column at a specific index from a matrix"""
        if index > len(self.matrix[0]) - 1:
            raise Exception("Column requested out of index bounds")

        return vector([self.matrix[i][index] for i in range(len(self.matrix))])
    
    def shape(self):
        """Get the (x,y) dims of this matrix"""
        return (len(self.matrix), len(self.matrix[0]))
    
    def __str__(self):
        return '\n'.join([str(row) for row in self.matrix])

    def __len__(self):
        """Get the number of rows in the matrix"""
        return len(self.matrix)

class vector:
    """Vector class used to store a 1d array with specialized operations"""
    def __init__(self, v):
        if type(v) != list and not isinstance(v, vector):
            raise Exception("Invalid type passed to vector constructor. Expected type list or vector")
        if type(v) == list:
            self.vec = v
        else:
            self.vec = v.vec
    
    def scale(self, scalar):
        """Multiply vector by a scalar"""
        return vector(map((lambda x: x*scalar), self.vec))

    def elementwise_mul(self, other):
        """Multiply two vectors elementwise"""
        if len(self) != len(other):
            raise Exception("Invalid vector addition - vectors not of same length")

        return vector(map(lambda x, y: x * y, self.vec, other.vec))

    def copy(self):
        """Make deep copy"""
        return vector([elem for elem in self.vec])
        
    def __mul__(self, other):
        """Multiply vector elementwize or with a scalar"""
        if(type(other) == int or type(other) == frac or type(other) == float):
            return self.scale(other)
        
        return self.elementwise_mul(other)

    def __add__(self, other):
        """Perform an elementwise addition between two vectors of the same size"""
        if len(self) != len(other):
            raise Exception("Invalid vector addition - vectors not of same length")
        return map(lambda x, y: x + y, self.vec, other.vec)
    
    def __sub__(self, other):
        """Subtract other vector from this vector"""
        if len(self) != len(other):
            raise Exception("Invalid vector addition - vectors not of same length")
        return map(lambda x, y: x - y, self.vec, other.vec)

    def __eq__(self, other):
        return self.vec == other.vec

    def __len__(self):
        """Get the number of elements in the vector"""
        return len(self.vec)
    
    def __getitem__(self, index):
        return self.vec[index]
    
    def __setitem__(self, index, val):
        """Set the item at the specified index"""
        self.vec[index] = val
        return self
    
    def __str__(self):
        return str(self.vec)
    
    def __repr__(self):
        return self.__str__()


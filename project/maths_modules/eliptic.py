import collections


def inv(n, q):
    for i in range(q):
        if (n * i) % q == 1:
            return i
        pass
    raise Exception("Cant find inv")
    pass


def sqrt(n, q):
    if not (n < q):
        raise Exception("in sqrt n < q")
    for i in range(1, q):
        if i * i % q == n:
            return i, q - i
        pass
    raise Exception("not found")


Coord = collections.namedtuple("Coord", ["x", "y"])


class EC(object):
    """System of Elliptic Curve"""
    def __init__(self, a, b, q):
        """elliptic curve as: (y**2 = x**3 + a * x + b) mod q
        - a, b: params of curve formula
        - q: prime number
        """
        a = a % q
        b = b % q

        if not(0 < a and a < q and 0 < b and b < q and q > 2):
            raise Exception("Invalid value of elliptic curve")
        if not ((4 * (a ** 3) + 27 * (b ** 2))  % q != 0):
            raise Exception("Ellipitc curve is singular")
        self.a = a
        self.b = b
        self.q = q
        self.zero = Coord(0, 0)
        pass

    def is_valid(self, p):
        if p == self.zero: return True
        l = (p.y ** 2) % self.q
        r = ((p.x ** 3) + self.a * p.x + self.b) % self.q
        return l == r

    def at(self, x):
        if not (x < self.q):
          raise Exception ("x > q")
        ysq = (x ** 3 + self.a * x + self.b) % self.q
        y, my = sqrt(ysq, self.q)
        return Coord(x, y), Coord(x, my)

    def neg(self, p):
        return Coord(p.x, -p.y % self.q)

    def add(self, p1, p2):
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            return self.zero
        if p1.x == p2.x:
            l = (3 * p1.x * p1.x + self.a) * inv(2 * p1.y, self.q) % self.q
            pass
        else:
            l = (p2.y - p1.y) * inv(p2.x - p1.x, self.q) % self.q
            pass
        x = (l * l - p1.x - p2.x) % self.q
        y = (l * (p1.x - x) - p1.y) % self.q
        return Coord(x, y)

    def mul(self, p, n):
        r = self.zero
        m2 = p
        while 0 < n:
            if n & 1 == 1:
                r = self.add(r, m2)
                pass
            n, m2 = n >> 1, self.add(m2, m2)
            pass
        return r

    def order(self, g):
        if not(self.is_valid(g) and g != self.zero):
            raise Exception("point is not valid")
        for i in range(1, self.q + 1):
            if self.mul(g, i) == self.zero:
                return i
            pass
        return self.q

    def generate(self):
        gen = set()
        for i in range(0, self.q + 1):
            try:
                p = self.at(i)
            except Exception:
                pass
            gen.add(p[0])
            gen.add(p[1])
        return gen

    def generate_from_point(self, p):
        if not(self.is_valid(p) and p != self.zero):
            raise Exception("point is not valid")
        buf = p
        gen = set()
        for i in range(0, self.q + 1):
            gen.add(buf)
            buf = self.add(buf, p)
        return gen

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return 1
        return 0


from PIL import Image  # type: ignore[import]
from pprint import pprint as pp

def generate_matrix(size):
    if size == 0:
        return [[1]]

    t = [[0, 2], [3, 1]]

    small_matrix = generate_matrix(size - 1)

    result = [[0 for x in range(2 ** size)] for y in range(2 ** size)]

    for i in range(2 ** size):
        for j in range(2 ** size):
            k = 2 ** (size - 1)

            a = t[i >= k][j >= k]

            result[i][j] = ((small_matrix[i % k][j % k] * (k ** 2) - 1) * 4 + a + 1) / ((2 ** size) ** 2)

    print(f'matrix({size}) = ')
    # pp(result)
    return result


def dither(img: Image, *, bit_trunc: int = 3, matrix_n = 3):
    # matrix_n - номер матрицы для преобразования (размер матрицы = 2 ** matrix_n)
    # (без дизеринга) 0 <= matrix_n <= 3 (максимальное значение, при котором не будут появляться артефакты)
    # 1 / 2 ** (2 ** matrix_n) == 1/256 == 1/(кол-во цветов) - при matrix_n=3 это равенство выполнится, после будут появляться артефакты

    # bit_trunc - кол-во бит глубины цвета, на которое нужно снизить глубину цвета
    # (без уменьшения глубины цвета) 0 <= bit_trunc <= 8 (1 бит на каждый канал)
    # я не понял почему тут такие границы, но это так)

    assert 0 <= bit_trunc <= 8, f'Invalid value: bit_trunc={bit_trunc}'
    assert 0 <= matrix_n <= 3, f'Invalid value: matrix_n={matrix_n}'

    k = 2 ** bit_trunc
    matrix_size = 2 ** matrix_n
    matrix = generate_matrix(matrix_n)

    img = img.convert('RGBA') # создает копию пикчи, изначальная меняться не будет
    w, h = img.size

    for i in range(h):
        for j in range(w):
            px = img.getpixel((j, i))
            r, g, b, a = px

            mi, mj = i % matrix_size, j % matrix_size
            mc = (matrix[mi][mj] - 0.5) * k

            r += mc
            g += mc
            b += mc

            r = round(r / k) * k
            g = round(g / k) * k
            b = round(b / k) * k

            new_px = r, g, b, a
            img.putpixel((j, i), new_px)

    return img


_in = 'pic.png'
_out = 'out.png'

img = Image.open(_in)
result = dither(img)
result.save(_out)
print('Done')
result.show()

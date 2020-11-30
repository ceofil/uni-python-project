import png
import src.canvas as canvas


def main():
    c = canvas.Canvas(255, 255)
    for x in range(255):
        for y in range(255):
            c.put_pixel(x, y, x, y, y)
    c.dump_to_png('test.png')


if __name__ == '__main__':
    main()

import sys
from PyQt5.QtGui import QImage, qAlpha, qRed, qGreen, qBlue

TRANSPARENCY_COLOR = '0xf81f'


def get_16bit_color_from_rgb(alpha, red, green, blue):
    """
    Get a 16bit color string (0x...) from RGB values.
    :param red: 0..255
    :param green: 0..255
    :param blue: 0..255
    :return:  A string with the 16bit value in hex format.
    """
    if alpha == 0:
        return TRANSPARENCY_COLOR
    red_16bit = int((red/255)*31) << 11
    green_16bit = int((green/255)*63) << 5
    blue_16bit = int((blue/255)*31)
    rgb_16bit = red_16bit | green_16bit | blue_16bit
    if rgb_16bit > 65535:
        raise RuntimeError('Value ({}) too large for 16bit.'.format(rgb_16bit))
    return '0x{0:04x}'.format(rgb_16bit)


def image_to_rgb_array(input_path, output_path, variable_name='rgb_array'):
    """
    Converts an image to an unsigned char array containing RGB values.
    :param input_path: Path to the image.
    :param output_path: Output path.
    :param variable_name: Name for the array variable.
    """
    image = QImage(input_path)
    with open(output_path, 'w') as file_:
        # Write the first line of the file, declaring an array with the size of the image's pixel count and the given
        # name.
        file_.write('const uint16_t {}[{}] = {}\n\t'.format(variable_name, image.width() * image.height(), '{'))
        for y in range(0, image.width()):
            for x in range(0, image.height()):
                pixel = image.pixel(x, y)
                if x == image.width() - 1 and y == image.height() - 1:
                    # Last pixel in image: Close the array with '}' and add a semicolon.
                    if x == 0:
                        # Catches the edge case of an image with width 1 and ensures correct file formatting in that
                        # case.
                        file_.write('{}{};'.format(get_16bit_color_from_rgb(qAlpha(pixel),
                                                                            qRed(pixel),
                                                                            qGreen(pixel),
                                                                            qBlue(pixel)), '}'))
                    else:
                        # Last pixel of an image with a width larger than 0.
                        file_.write(' {}{};'.format(get_16bit_color_from_rgb(qAlpha(pixel),
                                                                             qRed(pixel),
                                                                             qGreen(pixel),
                                                                             qBlue(pixel)), '}'))
                elif x == 0:
                    # First pixel in a line.
                    file_.write('{},'.format(get_16bit_color_from_rgb(qAlpha(pixel),
                                                                      qRed(pixel),
                                                                      qGreen(pixel),
                                                                      qBlue(pixel))))
                else:
                    # All other pixels.
                    file_.write(' {},'.format(get_16bit_color_from_rgb(qAlpha(pixel),
                                                                       qRed(pixel),
                                                                       qGreen(pixel),
                                                                       qBlue(pixel))))
            if y < image.height() - 1:
                # If more lines follow, add a line break and an initial tab stop.
                file_.write('\n\t')
        # Add an empty line to the end of the file.
        file_.write('\n')


if __name__ == '__main__':
    if len(sys.argv) > 3:
        image_to_rgb_array(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        image_to_rgb_array(sys.argv[1], sys.argv[2])
#!bin/env python3.8
# -*- coding: utf-8 -*-
"""
readis2.py reads out IS2 thermal images made by a Fluke Ti480 PRO
Copyright (C) 2021  Roelof Ymker

 This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import os
from zipfile import ZipFile
import shutil
from struct import unpack
from otherfunctions import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
from mpl_toolkits.axes_grid1 import make_axes_locatable


def read_is2_new(filename):
    """
    Read the Fluke IS2 file made by an Ti480 PRO. This function gives back a dictionary with all extracted data.
    :param filename: file to be read
    :return:
    """
    ir = {}
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall('temp')

    ir['FileName'] = os.path.split(filename)[1]

    # Camera info
    camera_info_file = open(os.path.join('temp', 'CameraInfo.gpbenc'), 'r', encoding='latin-1')
    camera_info = camera_info_file.read()
    camera_info_file.close()
    ir['CameraManufacturer'] = str(camera_info[76:94])
    ir['CameraModel'] = str(camera_info[97:103])
    ir['EngineSerial'] = str(camera_info[104:112])
    ir['CameraSerial'] = str(camera_info[115:124])

    # Calibration data
    cal_data = np.fromfile(os.path.join('temp', 'CalibrationData.gpbenc'), dtype=np.uint8)
    ir['range'] = int(cal_data[18])  # Auto 1 or 2, maybe more?
    ir['conversion'] = {}
    for i in range(len(cal_data)):
        if cal_data[i] == 74 and cal_data[i + 1] == 25 and cal_data[i + 2] == 13:  # Every part of the conversion function starts with this 3 bytes
            curve_part = cal_data[i + 3:i + 27]
            temp_range = np.array([unpack('<f', curve_part[:4])[0], unpack('<f', curve_part[5:9])[0]])
            if temp_range[0] >= -180:
                equation_variables = {'a': unpack('<f', curve_part[20:24])[0],
                                      'b': unpack('<f', curve_part[15:19])[0],
                                      'c': unpack('<f', curve_part[10:14])[0]}
                data_range = calc_equation(
                    [equation_variables['a'], equation_variables['b'], equation_variables['c']],
                    temp_range)
                data_range_int = [int(data_range[0]) + (data_range[0] % 1 > 0), int(data_range[1]) + (data_range[1] % 1 > 0)]
                for j in range(data_range_int[0], data_range_int[1]):
                    # Fluke uses a quadratic function with temperature as input, and IR-data as output. We want data as input and temperature as output, so the abc-equation is used.
                    ir['conversion'][j] = (-equation_variables['b'] + np.sqrt(equation_variables['b'] ** 2 - 4 * equation_variables['a'] * (equation_variables['c'] - j))) / (2 * equation_variables['a'])

    # IRImageInfo
    ir_image_info = np.fromfile(os.path.join('temp', 'Images', 'Main', 'IRImageInfo.gpbenc'), dtype=np.uint8)
    ir['transmission'] = unpack('<f', ir_image_info[43:47])[0]
    ir['emissivity'] = unpack('<f', ir_image_info[33:37])[0]
    ir['backgroundtemperature'] = unpack('<f', ir_image_info[38:42])[0]

    # IR data
    d = np.fromfile(os.path.join('temp', 'Images', 'Main', 'IR.data'), dtype=np.uint16)
    ir['size'] = [int(d[192]), int(d[193])]
    index = ir['size'][1]
    raw_temp = []
    for i in d[index:index + (ir['size'][0] * ir['size'][1])]:
        raw_temp.append((ir['conversion'][i] - (2 - ir['transmission'] - ir['emissivity']) * ir['backgroundtemperature']) / (ir['transmission'] * ir['emissivity']))

    ir['data'] = np.reshape(raw_temp, [ir['size'][0], ir['size'][1]])

    # Thumbnail
    thumbnails_dir = os.path.join('temp', 'Thumbnails')
    thumbnails_list = []
    thumbnails_list += [each for each in os.listdir(thumbnails_dir) if each.endswith('.jpg')]
    ir['thumbnail'] = plt.imread(os.path.join(thumbnails_dir, thumbnails_list[0]))

    # Visible image
    images_dir = os.path.join('temp', 'Images', 'Main')
    image = ''
    maxsize = 0
    for each in os.listdir(images_dir):
        if each.endswith('.jpg'):
            # Take the biggest image, the smaller image is cropped from the bigger one.
            filesize = os.path.getsize(os.path.join(images_dir, each))
            if filesize > maxsize:
                image = each
                maxsize = filesize
    ir['photo'] = plt.imread(os.path.join(images_dir, image))

    # Remove temp directory
    shutil.rmtree('temp')
    return ir


def plot_ir(ir, colormap='nipy_spectral', limits=[], contourplot=True, tempscale='C', saveas='', grid=True,
            label='Temperature', rotate=0, returndata=False, title=''):
    """
    This function shows a thermal image from an IS2 file
    :param ir: dictionary with extracted data form IS2 file
    :param colormap: change the default colormap 'nipy_spectral'
    :param limits: define lowest and highest value of the image: [l, h]
    :param contourplot: plot a contourplot on the image, True or False
    :param tempscale: change the temperature scale: C (Celsius), K, (Kelvin), F (Fahrenheid) or N (Newton) default is C
    :param saveas: if defined, the image will be saved to this location
    :param grid: enable grid on the image. Default is True
    :param label: set the label of the colorbar. Default is Temperature
    :param rotate: rotate the image by an angle. Default is 0
    :param returndata: get back the image data
    :param title: set the title of the image. Default is the filename
    :return:
    """

    if tempscale == 'C':
        data = ir['data']
        colorbar_label = '{} [$^\circ$C]'.format(label)
    elif tempscale == 'K':
        data = c2k(ir['data'])
        colorbar_label = '{} [K]'.format(label)
    elif tempscale == 'F':
        data = c2f(ir['data'])
        colorbar_label = '{} [$^\circ$F]'.format(label)
    elif tempscale == 'N':
        data = c2n(ir['data'])
        colorbar_label = '{} [$^\circ$N]'.format(label)
    else:
        data = ir['data']
        colorbar_label = '{} [$^\circ$C]'.format(label)

    if not title:
        title = ir['FileName']
    if not limits:
        min_t = minloc(data)[2]
        max_t = maxloc(data)[2]
        limits = [min_t, max_t]
    else:
        min_t, max_t = limits

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.subplots_adjust(right=0.9)

    if rotate != 0 and rotate != 180:
        data = ndimage.rotate(data, rotate)
        ax.axis([0, ir['size'][0], ir['size'][1], 0])
    else:
        ax.axis([0, ir['size'][1], ir['size'][0], 0])
    img = ax.imshow(data, cmap=colormap, aspect='equal', vmin=limits[0], vmax=limits[1])
    ax.set_title(title)
    ax.grid(grid)
    ax.set_xlabel("E: {}, T: {}%, BG: {}'C    Min.: {}'C, Max.: {}'C".format(
        round(ir['emissivity'], 2),
        round(ir['transmission'] * 100),
        round(ir['backgroundtemperature'], 1),
        round(min_t, 1),
        round(max_t, 1)))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05)

    plt.colorbar(img, cax=cax, label=colorbar_label)

    if contourplot:
        levels = []
        for i in range(-100, 10010, 10):
            levels.append(i)
        img2 = ax.contour(gaussian_filter(data, 0.9), colors='k',
                          levels=(levels),
                          linewidths=0.5)
        plt.clabel(img2, fontsize=9, inline=0.01, fmt="%1.0f")

    plt.tight_layout()

    if saveas:
        plt.savefig(saveas, transparent=True)
    # plt.show()
    if returndata:
        return data


def show_thumbnail(ir, title='', saveas='', rotate=0):
    if not title:
        title = ir['FileName']

    foto = ir['thumbnail']

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if rotate != 0:
        foto = ndimage.rotate(foto, rotate)
    ax.imshow(foto, aspect='equal')
    ax.set_title(title)

    plt.tight_layout()

    if saveas:
        plt.savefig(saveas)
    # plt.show()


def show_photo(ir, title='', saveas='', rotate=0):
    if not title:
        title = ir['FileName']

    foto = ir['photo']

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if rotate != 0:
        foto = ndimage.rotate(foto, rotate)
    ax.imshow(foto, aspect='equal')
    ax.set_title(title)

    plt.tight_layout()

    if saveas:
        plt.savefig(saveas)
    # plt.show()

if __name__ == "__main__":
    import argparse
    from unitconversion import *
    from scipy import ndimage

    p = argparse.ArgumentParser()
    p.add_argument('filename')
    p.add_argument('-m', '--colormap', dest='colormap', required=False, default='nipy_spectral',
                   help='Change the default colormap')
    p.add_argument('-l', '--limits', dest='limits', required=False, default=[],
                   help='Define the limits of the plot, lowest and highest value l,h.'
                        'Default the minimum and maximum value are extracted from data')
    p.add_argument('-c', '--contourplot', dest='contourplot', required=False, default=True,
                   help='Add a contourplot to the image. True or False, default is True')
    p.add_argument('-s', '--temperaturescale', dest='tempscale', required=False, default='C',
                   help='Change the temperaturescale of the thermal image.'
                        'C (Celsius), K, (Kelvin), F (Fahrenheid) or N (Newton) default is C')
    p.add_argument('-S', '--saveas', dest='saveas', required=False, default='',
                   help='If defined, the extracted image wil saved into this file')
    p.add_argument('-g', '--grid', dest='grid', required=False, default=True,
                   help='Enable grid on image. Default is True')
    p.add_argument('--label', dest='label', required=False, default='Temperature',
                   help='Label at the colorbar. Default: Temperature')
    p.add_argument('-a', '--rotationangle', dest='angle', required=False, default=0,
                   help='Rotation angle. 0, 90, 180 or 270, default is 0')
    p.add_argument('-T', '--title', dest='title', required=False, default='',
                   help='Title above the image. If not defined, the filename will be used')

    args = p.parse_args()
    
    print("readis2.py  Copyright (C) 2021  Roelof Ymker\n\n"
          "This program comes with ABSOLUTELY NO WARRANTY;\n"
          "This is free software, and you are welcome to redistribute it under certain conditions;")

    if args.limits:
        limits = [float(args.limits.split(',')[0]), float(args.limits.split(',')[1])]
    else:
        limits = []

    if args.contourplot or args.contourplot.lower() == 'true' or args.contourplot == '1':
        contourplot = True
    else:
        contourplot = False

    if args.grid or args.grid.lower() == 'true' or args.grid == '1':
        grid = True
    else:
        grid = False

    data = read_is2_new(args.filename)

    show_thumbnail(data, title=args.title)
    plot_ir(data, colormap=args.colormap, limits=limits, contourplot=contourplot, tempscale=args.tempscale,
            saveas=args.saveas, grid=grid, label=args.label, rotate=int(args.angle), title=args.title)
    show_photo(data, title=args.title, rotate=int(args.angle))
    plt.show()

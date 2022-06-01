import os
import math
import bpy
import time

import numpy as np


# Top origin: 6.09446 m
# Top Cube: 3.48133 m

def angle_to_radiant(_angle):
    return _angle * (2 * math.pi / 360)


def quadratic_func_by_points(_p1, _p2, _p3):
    # https://chris35wills.github.io/parabola_python/
    x1, y1 = _p1
    x2, y2 = _p2
    x3, y3 = _p3
    denom = (x1 - x2) * (x1 - x3) * (x2 - x3)
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
    b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom

    # (x**3 == x³)
    return lambda _x: a*_x**2 + b*_x + c


def invers():
    return lambda _x: np.sqrt(-1/6 * _x + 1) * 3


def simple_inv():
    return lambda _x: np.sqrt(-1/height * _x + 1) * camera.location.y


# rendering creates full imgae then converts to depthmap/applies shader, must be possible to get faster
# set in code to render image or depth?

# Axis in Blender
X = 0
Y = 1
Z = 2


# render_[0-2]-([8-9]|[0-9]?[0-2]).png
# https://regexr.com/
# 'render_1-12.png', 'render_1-7.png', 'render_0-19.png', 'render_1-16.png', 'render_0-15.png', 'render_1-13.png'
# 'render_0-14.png', 'render_1-2.png', 'render_0-9.png', 'render_1-15.png', 'render_1-3.png', 'render_0-3.png'
# 'render_0-0.png', 'render_1-10.png', 'render_0-11.png', 'render_0-12.png', 'render_1-18.png', 'render_1-4.png'
# 'render_0-16.png', 'render_0-7.png', 'render_0-13.png', 'render_1-11.png', 'render_1-14.png', 'render_0-1.png'
# 'render_1-9.png', 'render_0-18.png', 'render_0-5.png', 'render_1-17.png', 'render_0-6.png', 'render_1-0.png'
# 'render_1-6.png', 'render_1-19.png', 'render_1-1.png', 'render_1-5.png', 'render_0-4.png', 'render_0-10.png'
# 'render_0-17.png', 'render_1-8.png', 'render_0-8.png', 'render_0-2.png'



# Blender Nodes
subject = bpy.data.objects['Model']
cam_rig = bpy.data.objects['CameraAnchor']  # Camera looks at this
camera = bpy.data.objects['Camera']
height = bpy.data.objects['Top'].location.z  # later curve top
file_type = bpy.context.scene.render.file_extension

# Dataset configuration
# Position camera to center object, set area to scan, move camera to mot west point and rotate around
vertical_slices = 30
horizontal_levels = 2
angle = angle_to_radiant(90)  # current camera position is center of angle
# Defining area of interest
vertical_step = angle / (vertical_slices - 1)  # Why -1? because I count the last value (90) too?
horizontal_step = height / horizontal_levels

output_dir = 'render_out'
file_prefix = "render"

# Set rig to the left border
cam_rig.rotation_euler[Z] = -(angle / 2)
camera_original_y = camera.location.y
rig_original_y = cam_rig.location.z

# Calculate curve [f] for the camera to follow
p1 = [camera.location.y, 0]
p2 = [0, height]
p3 = [camera.location.y/2, 0.9 * height]
# Calculate equation
# f = quadratic_func_by_points(p1, p2, p3)
f = simple_inv()

# Camo texture is left, lava is right
# Go up a notch
# print(f)
for latitude in range(horizontal_levels):
    # Go around, starting from left
    for longitude in range(vertical_slices):
        # ToDo get filetype from blender renderer
        bpy.context.scene.render.filepath = os.path.join(output_dir, file_prefix + f"_{latitude}-{longitude}{file_type}")
        bpy.ops.render.render(write_still=True)

        cam_rig.rotation_euler[Z] += vertical_step
    # Move the rig up a notch and offset camera a little to have a different angle
    cam_rig.location.z += horizontal_step
    camera.location.z += 0.1

    # x = latitude * horizontal_step
    # print(f"camera at: {x}, {f(x)}")
    # camera.location.y = f(x)
    # camera.location.z = x
    # Reset to left position
    cam_rig.rotation_euler[Z] = -(angle / 2)

cam_rig.location.z = rig_original_y
cam_rig.rotation_euler[Z] = 0

camera.location.y = camera_original_y
camera.location.z = 0

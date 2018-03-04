"""
This example script creates a box in the middle of a half room
"""

import sys
import random
import math
import mathutils
import bpy
import csv
import os

boop = 'D:/PycharmProjects/Lobster/src/'

if not (boop in sys.path):
    sys.path.append(boop)

import rendering.BlenderAPI as bld
""" ************* User specified stuff here ************* """
# Specify number of images to render

num_images = 20
# required file paths for the script to run
obj_path = 'D:\\PycharmProjects\\3DModels\\Tea\\Tea.obj'
texture_path = 'D:\\PycharmProjects\\3DModels\\Tea\\Tea.jpg'
render_folder = 'D:\\PycharmProjects\\3DModels\\Tea\\render'

csv_path = os.path.join(render_folder,'camera.csv')

# instantiate scene
scene = bld.BlenderRandomScene(bpy)
scene.load_subject_from_path(obj_path=obj_path, texture_path=texture_path)
scene.set_render()
scene.add_camera(cam)

with open(csv_path,'w') as csvfile:

    coord_writer = csv.writer(csvfile, delimiter=',')

    for i in range(num_images):
        # **********************  RENDER N SAVE **********************
        render_path = os.path.join(render_folder,'render%d.png'%i)
        scene.render_to_file(render_path)

import pathlib
import sys
import os
import unittest
import shutil

# Ensure source directory is in python path
src_dir = str(pathlib.Path(__file__).resolve().parents[2])
project_dir = str(pathlib.Path(__file__).resolve().parents[3])
#ocado_dir = str(pathlib.Path(__file__).resolve().parents[3])
#print(project_dir)
sys.path.append(src_dir)
sys.path.append(project_dir)

if not project_dir in sys.path:
    sys.path.append(project_dir)

if not src_dir in sys.path:
    sys.path.append(src_dir)

from ..render_pipeline import *

# #set up blender path
# #blender_path = 'blender' # for max
blender_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender' # for GPU04
# blender_path = "E:\Blender_Foundation\Blender\\blender" # for Pavel

class TestPipeline(unittest.TestCase):
    """
    Note:
    'example_run' provides a possible usage of the rendering pipeline and includes
    hard-coded paths that are configured for a particular machine. It therefore
    should not form part of the test suite. All functionality in example_run is tested
    elsewhere in this file.
    """

    def setUp(self):
        shutil.rmtree('dummy_dir', ignore_errors=True)
        os.mkdir('dummy_dir')

    def tearDown(self):
        shutil.rmtree('dummy_dir', ignore_errors=True)

    def test_validate_folders(self):
        folder_list = ['f1', 'f2']
        validate_folders('dummy_dir', folder_list)
        self.assertEqual(sorted(['f1', 'f2']), sorted(os.listdir('dummy_dir')))

    def test_validate_folders_no_create(self):
        folder_list = ['f1']
        os.mkdir(os.path.join('dummy_dir', folder_list[0]))
        validate_folders('dummy_dir', folder_list)
        self.assertEqual(['f1'], os.listdir('dummy_dir'))

    def test_destroy_folders(self):
        folder_list = ['f1']
        os.mkdir(os.path.join('dummy_dir', folder_list[0]))
        destroy_folders('dummy_dir', folder_list)
        self.assertEqual(len(os.listdir('dummy_dir')), 0)

    def test_generate_poses(self):
        """
        Tests the subprocess call made Blender to do the rendering.
        This test uses a sample workspace in the project 'test_data' folder
        for source object files. Resulting renders are saved in the usual
        'dummy_dir' and deleted afterwards.
        """
        workspace = os.path.join(project_dir, 'test_data', 'rendering_tests', 'pipeline_tests', 'render_workspace')
        print("workspace is ", workspace)
        # Assemble the arguments

        #blender_path = 'blender' # for max
        # blender_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender' # for GPU04
        obj_poses = os.path.join(workspace, 'dummy_dir')
        print("dummy dir is ", obj_poses)
        obj_set = os.path.join(workspace, "object_files", "two_set_model_format")
        renders_per_class = 1
        blender_attributes = {
            "attribute_distribution_params": [["num_lamps", "mid", 5], ["num_lamps","scale", 0.2], ["lamp_energy","mu", 500.0], ["lamp_size", "mu", 5], ["camera_radius", "sigmu", 0.1]],
             "attribute_distribution" : []
        }
        visualize_dump=False
        dry_run_mode=False
        n_of_pixels = 300
        #adjust_brightness =False,
        render_samples=128

        # Make the call
        generate_poses(src_dir, blender_path, obj_set, obj_poses, renders_per_class, blender_attributes, visualize_dump, dry_run_mode, n_of_pixels, render_samples)

        # Check for correct output
        # Check both models rendered
        self.assertEqual(sorted(os.listdir(obj_poses)), sorted(['Coconut', 'Liberte']))

        # Check for 1 render in each product folder
        print(os.listdir(os.path.join('dummy_dir')))
        print("content of Liberte is ", os.listdir(os.path.join(obj_poses, 'Liberte')))
        self.assertTrue( 'render0.png' in os.listdir(os.path.join(obj_poses, 'Liberte')) )
        self.assertTrue('render0.png' in os.listdir(os.path.join(obj_poses, 'Coconut')))

    def test_gen_merge(self):
        # Create an image
        foreground_path = os.path.join(project_dir, 'test_data', 'merging_tests', 'single_test', 'render1.png')
        foreground = Image.open(foreground_path)

        save_as = os.path.join('dummy_dir', 'output.jpg')
        gen_merge(foreground, save_as, pixels=300, adjust_brightness = True)

        self.assertEqual(os.listdir('dummy_dir'), ['output.jpg'])


    def test_full_run(self):
        # Prepare the workspace to run the tests
        workspace = os.path.join(project_dir, 'test_data', 'rendering_tests', 'pipeline_tests', 'render_workspace')
        temp_folders = [
            'generate_bg',
            'object_poses',
            'final_folder'
            ]
        destroy_folders(workspace, temp_folders)

        # Assemble the arguments


        blender_attributes = {
            "attribute_distribution_params": [["num_lamps","mid", 5], ["num_lamps","scale", 0.2], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
             "attribute_distribution" : []
        }

        arguments = {
            "obj_set": os.path.join(workspace, "object_files", "two_set_model_format"),
            "blender_path": blender_path,
            "renders_per_class": 2,
            "work_dir": workspace,
            "generate_background": False,
            "background_database": os.path.join(workspace, "bg_database","white"),
            "blender_attributes": blender_attributes,
            "n_of_pixels": 300,
            "adjust_brightness": True
            }

        full_run(**arguments)

        # we can't predict the final zip name, so just make sure there is a zip file
        # in the 'final zip' folder.
        self.assertTrue(os.listdir(os.path.join(workspace, 'final_zip'))[0].endswith('.zip'))

        destroy_folders(workspace, temp_folders)

        arguments2 = {
            "obj_set": os.path.join(workspace, "object_files", "two_set_model_format"),
            "blender_path": blender_path,
            "renders_per_class": 2,
            "work_dir": workspace,
            "generate_background":True,
            "background_database": os.path.join(workspace, "bg_database","white"),
            "blender_attributes": blender_attributes,
            "n_of_pixels": 300,
            "adjust_brightness": True
            }

        full_run_with_notifications(**arguments2)

        # we can't predict the final zip name, so just make sure there is a zip file
        # in the 'final zip' folder.
        self.assertTrue(os.listdir(os.path.join(workspace, 'final_zip'))[0].endswith('.zip'))


        destroy_folders(workspace, temp_folders)

    def test_full_run_error(self):

        workspace = os.path.join(project_dir, 'test_data', 'rendering_tests', 'pipeline_tests', 'render_workspace')
        temp_folders = [
            'generate_bg',
            'object_poses',
            'final_folder'
            ]
        destroy_folders(workspace, temp_folders)

        # Assemble the arguments


        blender_attributes = {
            "attribute_distribution_params": [["num_lamps","mid", 5], ["num_lamps","scale", 0.2], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
             "attribute_distribution" : []
        }

        arguments = {
            "obj_set": os.path.join(workspace, "object_files", "two_set_model_format"),
            "blender_path": blender_path,
            "renders_per_class": 2,
            "work_dir": workspace,
            "generate_background": False,
            "background_database": None,
            "blender_attributes": blender_attributes,
            "n_of_pixels": 300,
            "adjust_brightness": True
            }



        self.assertRaises(RenderPipelineError, lambda: full_run_with_notifications(**arguments))
        destroy_folders(workspace, temp_folders)

        arguments2 = {
            "obj_set": os.path.join(workspace, "object_files", "two_set_model_format"),
            "blender_path": blender_path,
            "renders_per_class": 2,
            "work_dir": workspace,
            "generate_background": False,
            "background_database": None,
            "blender_attributes": blender_attributes,
            "n_of_pixels": (300,),
            "adjust_brightness": True
            }

        self.assertRaises(RenderPipelineError, lambda: full_run_with_notifications(**arguments2))
        destroy_folders(workspace, temp_folders)

        arguments3 = {
            "obj_set": os.path.join(workspace, "object_files", "two_set_model_format"),
            "blender_path": blender_path,
            "renders_per_class": 2,
            "work_dir": os.path.join(workspace, "nonsense"),
            "generate_background": False,
            "background_database": None,
            "blender_attributes": blender_attributes,
            "n_of_pixels": 300,
            "adjust_brightness": True
            }

        self.assertRaises(RenderPipelineError, lambda: full_run_with_notifications(**arguments3))
        destroy_folders(workspace, temp_folders)


        arguments4 = {
            "obj_set": os.path.join(workspace, "object_files", "two_set_model_format"),
            "blender_path": blender_path,
            "renders_per_class": 2,
            "work_dir": os.path.join(workspace),
            "generate_background": False,
            "background_database": os.path.join(workspace, "bg_database","non_exists"),
            "blender_attributes": blender_attributes,
            "n_of_pixels": 300,
            "adjust_brightness": True
            }

        self.assertRaises(RenderPipelineError, lambda: full_run(**arguments4))
        destroy_folders(workspace, temp_folders)

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPipeline)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()

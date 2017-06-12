# standard libraries
import unittest
import os
import pandas
# from VAPr.in import ingester

# project-specific libraries
from VAPr.ingester import Ingester

__author__ = 'Mazzaferro'


class TestIngester(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.getcwd()
        self.files_input_dir = os.path.join(self.base_dir, 'test_files/test_input_dir')
        self.samples_input_dir = os.path.join(self.base_dir, 'test_files/test_input_sample_dir')
        self.design_file_files = os.path.join(self.base_dir, 'test_files/design_file_by_file_name.csv')
        self.design_file_dirs = os.path.join(self.base_dir, 'test_files/design_file_by_dir_name.csv')
        self.output_csv_path_files = os.path.join(self.base_dir, 'test_files/test_out_csv_path/des_file_files')
        self.output_csv_path_dirs = os.path.join(self.base_dir, 'test_files/test_out_csv_path/des_file_dirs')
        self.mapping_list_len = (12, 2)
        self.x_45_c1 = {'sample_names': ['X45'],
                        'num_samples_in_csv': 1,
                        'raw_vcf_file_full_path': os.path.join(self.base_dir, 'test_files/test_input_sample_dir/'
                                                                              'X45/c1.vcf'),
                        'csv_file_basename': 'c1_annotated',
                        'vcf_file_basename': 'c1.vcf',
                        'csv_file_full_path': os.path.join(self.base_dir, 'test_files/test_out_csv_path/'
                                                                          'des_file_dirs/X45'),
                        'vcf_sample_dir': os.path.join(self.base_dir, 'test_files/test_input_sample_dir/X45')}

        self.mini1 = {'sample_names': ['mini1.vcf'],
                      'num_samples_in_csv': 1,
                      'raw_vcf_file_full_path': os.path.join(self.base_dir, 'test_files/test_input_dir/mini1.vcf'),
                      'csv_file_basename': 'mini1_annotated',
                      'vcf_file_basename': 'mini1.vcf',
                      'csv_file_full_path': os.path.join(self.base_dir, 'test_files/test_out_csv_path/des_file_files/'),
                      'vcf_sample_dir': os.path.join(self.base_dir, 'test_files/test_input_dir/')}

    def test_input_design_file_dirs(self):
        organizer = Ingester(self.samples_input_dir, self.output_csv_path_dirs)
        design_df = pandas.read_csv(self.design_file_dirs)
        organizer.digest_design_file(design_df)
        print(organizer.mapping_list[0], self.x_45_c1)
        self.assertEqual(len(organizer.mapping_list), self.mapping_list_len[0])
        self.assertEqual(organizer.mapping_list[0], self.x_45_c1)
        for _map in organizer.mapping_list:
            self.assertTrue(os.path.isfile(_map['raw_vcf_file_full_path']))

    def test_input_design_files(self):
        organizer = Ingester(self.files_input_dir, self.output_csv_path_files)
        design_df = pandas.read_csv(self.design_file_files)
        organizer.digest_design_file(design_df)
        self.assertEqual(len(organizer.mapping_list), self.mapping_list_len[1])
        self.assertEqual(organizer.mapping_list[0], self.mini1)
        for _map in organizer.mapping_list:
            self.assertTrue(os.path.isfile(_map['raw_vcf_file_full_path']))




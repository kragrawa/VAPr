from __future__ import division, print_function
import os
import sys
import pandas
import logging
import vcf
from vapr.annovar import AnnovarWr apper
from vapr.parsers import VariantParsing
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    logger.handlers[0].stream = sys.stdout
except:
    pass


class ProjectData(object):

    supported_build_vers = ['hg19', 'hg18', 'hg38']

    def __init__(self,
                 input_dir,
                 output_dir,
                 annovar_path,
                 project_data,
                 split_vcf=False,
                 design_file=None,
                 build_ver=None):

        """
        Base class for the project instantiation classes that will run the necessary functions. Mostly a container.
        """

        self.input_dir = input_dir
        self.output_csv_path = output_dir
        self.design_file = design_file
        self.annovar = annovar_path
        self.project_data = project_data
        self.buildver = self.check_ver(build_ver)
        self.times_called = 0
        self.mapping = self.get_mapping()
        self.split = split_vcf

    def get_mapping(self):

        if self.design_file:
            design_df = pandas.read_csv(self.design_file)
            sample_to_vcf_map = self.check_file_existance_return_mapping(design_df)

        else:
            sample_to_vcf_map = self.check_file_existance_return_mapping_no_design_file()

        return sample_to_vcf_map

    def check_file_existance_return_mapping_no_design_file(self):
        self.times_called += 1
        print(self.times_called)

        vcf_files = [_vcf for _vcf in os.listdir(self.input_dir) if _vcf.endswith('vcf')]
        samples_available = []

        if len(vcf_files) < 1:
            raise IOError('No files found in input dir')

        for vcf_file in vcf_files:

            vcf_reader = vcf.Reader(filename=os.path.join(self.input_dir, vcf_file))
            samples = vcf_reader.samples
            if len(samples) > 1:
                logging.info('File %s is a multisample VCF, %i samples detected' % (vcf_file, len(samples)))
                dir_name = '_'.join(['samples'] + samples)

            else:
                dir_name = '_'.join(['sample'] + samples)

            samples_available.append(dir_name)

            try:
                os.mkdir(os.path.join(self.input_dir, dir_name))
            except OSError as e:
                logging.info("OS error: {0}, moving vcf file to existing directory".format(e))

            os.rename(os.path.join(self.input_dir, vcf_file), os.path.join(self.input_dir,
                                                                           dir_name,
                                                                           os.path.basename(vcf_file)))

        sample_to_vcf_map = dict.fromkeys(samples_available, {})

        for sample in samples_available:
            vcf_files = [i for i in os.listdir(os.path.join(self.input_dir, sample)) if i.endswith('.vcf')]
            sample_to_vcf_map[sample]['vcf_csv'] = [(vcf_file, os.path.splitext(os.path.basename(vcf_file))[0] +
                                                     '_annotated') for vcf_file in vcf_files]  # God bless listcomps
        return sample_to_vcf_map

    def check_file_existance_return_mapping(self, design_df):

        design_file_mapping = design_df.set_index('Sample_Names').T.to_dict()
        for sample in design_file_mapping.keys():
            if not os.path.exists(os.path.join(self.input_dir, sample)):
                raise NameError('Could not find directory named %s as provided in design file' % sample)

            vcf_files = [i for i in os.listdir(os.path.join(self.input_dir, sample)) if i.endswith('.vcf')]
            logging.info('Found %i unique vcf files for sample %s' % (len(set(vcf_files)), sample))

            design_file_mapping[sample]['vcf_csv'] = [(vcf_file, os.path.splitext(os.path.basename(vcf_file))[0] +
                                                      '_annotated') for vcf_file in vcf_files]  # God bless listcomps

        return design_file_mapping

    def check_ver(self, build_ver):

        if not build_ver:
            self.buildver = 'hg19'  # Default genome build version

        if build_ver not in self.supported_build_vers:
            raise ValueError('Build version must not recognized. Supported builds are'
                             ' %s, %s, %s' % (self.supported_build_vers[0],
                                              self.supported_build_vers[1],
                                              self.supported_build_vers[2]))
        else:
            self.buildver = build_ver

        return self.buildver

    """
        def split_vcf(self):
        if self.split:
            new_input_dir = os.path.join(self.input_dir, 'split_files')
            # self.input_dir = new_input_dir
            os.mkdir(os.path.join(new_input_dir))
            for sample in self.mapping.keys():
                os.mkdir(os.path.join(new_input_dir, sample))
                for file_pair in self.mapping[sample]['vcf_csv']:
                    vcf_reader = vcf.Reader(filename=os.path.join(self.input_dir, sample, file_pair[0]))

            vcf_writer = vcf.Writer(open('/dev/null', 'w'), vcf_reader)
            for record in vcf_reader:
                vcf_writer.write_record(record)
    """


class AnnotationProject(ProjectData):

    def __init__(self,
                 input_dir,
                 output_dir,
                 annovar_path,
                 project_data,
                 design_file=None,
                 build_ver=None):

        """ Class that implements the API and the major annotation/saving methods  """

        super(AnnotationProject, self).__init__(input_dir,
                                                output_dir,
                                                annovar_path,
                                                project_data,
                                                design_file=design_file,
                                                build_ver=build_ver)

        self.annovar_wrapper = AnnovarWrapper(self.input_dir,
                                              self.output_csv_path,
                                              self.annovar,
                                              self.project_data,
                                              self.mapping,
                                              design_file=self.design_file,
                                              build_ver=self.buildver)

        self.annotator_wrapper = VariantParsing(self.input_dir,
                                                self.output_csv_path,
                                                self.annovar,
                                                self.project_data,
                                                self.mapping,
                                                design_file=self.design_file,
                                                build_ver=self.buildver)

    def download_dbs(self, all_dbs=True, dbs=None):
        """ Wrapper around Annovar database downloading function """
        self.annovar_wrapper.download_dbs(all_dbs=all_dbs, dbs=dbs)

    def run_annovar(self, multisample=False):
        """ Wrapper around multiprocess Annovar annotation  """
        self.annovar_wrapper.run_annovar(multisample=multisample)

    def annotate_and_save(self, buffer_vars=False, verbose=2):
        """ Wrapper around annotation runner  """
        self.annotator_wrapper.annotate_and_saving(buffer_vars=buffer_vars, verbose=verbose)

    def parallel_annotation_and_saving(self, n_processes=4, verbose=1):
        """ Wrapper around parallel annotation multiprocess runner  """
        self.annotator_wrapper.parallel_annotation(n_processes=n_processes, verbose=verbose)
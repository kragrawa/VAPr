import vcf
import myvariant
import csv
import re
import itertools
from pymongo import MongoClient
import VAPr.vcf_parsing as vvp


class VariantParsing(object):

    def __init__(self, csv_file, vcf_file, collection_name, db_name):

        self.chunksize = 1000
        self.step = 25
        self.csv_file = csv_file
        self.vcf_file = vcf_file
        self.hgvs = HgvsParser(self.vcf_file)
        self.csv_parsing = CsvParser(self.csv_file)
        self.collection = collection_name
        self.db = db_name

    def push_to_db(self):

        while self.csv_parsing.num_lines > self.step*self.chunksize:

            list_hgvs_ids = self.hgvs.get_variants_from_vcf(self.step)
            myvariants_variants = self.get_dict_myvariant(list_hgvs_ids)
            csv_variants = self.csv_parsing.open_and_parse_chunks(self.step)

            merged_list = []
            for i, _ in enumerate(myvariants_variants):
                merged_list.append(self.merge_dict_lists(myvariants_variants[i], csv_variants[i]))

            self.export(merged_list)
            self.step += 1

        return 'Done'

    def export(self, list_docs):
        """
        Export data do a MongoDB server
        :param list_docs: list of dictionaries containing variant information
        :return: null
        """
        client = MongoClient()
        db = getattr(client, self.db)
        collection = getattr(db, self.collection)
        collection.insert_many(list_docs)

    @staticmethod
    def merge_dict_lists(*dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def get_dict_myvariant(self, variant_list):
        """
        Function designated to place the queries on myvariant.info servers.

        :param variant_list: list of HGVS variant ID's. Usually retrived beforehand using the method
        get_variants_from_vcf
        from the class VariantParsing.
        :return: list of dictionaries. Each dictionary contains data about a single variant.
        """

        mv = myvariant.MyVariantInfo()
        # This will retrieve a list of dictionaries
        variant_data = mv.getvariants(variant_list, as_dataframe=False)
        variant_data = self.remove_id_key(variant_data)
        return variant_data

    @staticmethod
    def remove_id_key(variant_data):

        for dic in variant_data:
            dic['hgvs_id'] = dic.pop("_id", None)
            dic['hgvs_id'] = dic.pop("query", None)

        return variant_data


class HgvsParser(object):

    def __init__(self, vcf_file):

        self.vcf = vcf_file
        self.chunksize = 1000

    def get_variants_from_vcf(self, step):
        """
        Retrieves variant names from a LARGE vcf file.
        :param step: ...
        :return: a list of variants formatted according to HGVS standards
        """
        list_ids = []
        reader = vcf.Reader(open(self.vcf, 'r'))

        for record in itertools.islice(reader, step * self.chunksize, (step + 1) * self.chunksize):
            if len(record.ALT) > 1:
                for alt in record.ALT:
                    list_ids.append(myvariant.format_hgvs(record.CHROM, record.POS,
                                                          record.REF, str(alt)))
            else:
                list_ids.append(myvariant.format_hgvs(record.CHROM, record.POS,
                                                      record.REF, str(record.ALT[0])))

        return self.complete_chromosome(list_ids[0:self.chunksize])

    @staticmethod
    def complete_chromosome(expanded_list):
        for i in range(0, len(expanded_list)):
            if 'M' in expanded_list[i]:
                one = expanded_list[i].split(':')[0]
                two = expanded_list[i].split(':')[1]
                if 'MT' not in one:
                    one = 'chrMT'
                expanded_list[i] = one + ':' + two
        return expanded_list


class CsvParser(object):

    def __init__(self, csv_file):

        self.csv_file = csv_file
        self.num_lines = sum(1 for _ in open(self.csv_file))
        self.chunksize = 1000
        self.columns = ['chr',
                        'start',
                        'end',
                        'ref',
                        'alt',
                        'func_knowngene',
                        'gene_knowngene',
                        'genedetail_knowngene',
                        'exonicfunc_knowngene',
                        'tfbsconssites',
                        'cytoband',
                        'genomicsuperdups',
                        '1000g20XX',
                        'esp6500si_all',
                        'cosmic70',
                        'nci60',
                        'otherinfo']

    def open_and_parse_chunks(self, step):

        listofdicts = []

        with open(self.csv_file, 'r') as csvfile:

            reader = csv.reader(csvfile, delimiter=',')
            header = self._normalize_header(next(reader))

            for i in itertools.islice(reader, step * self.chunksize, (step + 1) * self.chunksize):
                sparse_dict = dict(zip(header, i))
                dict_filled = {k: sparse_dict[k] for k in self.columns if sparse_dict[k] != '.'}
                modeled = AnnovarModels(dict_filled)
                listofdicts.append(modeled.final_dict)

        return listofdicts

    @staticmethod
    def _normalize_header(header):
        normalized = []

        for item in header:
            if item.startswith('1000g20'):
                normalized.append('1000g20XX')
            else:
                normalized.append(item.lower().replace('.', '_'))

        return normalized


class AnnovarModels(object):

    def __init__(self, dictionary):

        self.dictionary = dictionary
        self.existing_keys = self.dictionary.keys()
        self.final_dict = self.process()

    def process(self):
        for key in self.dictionary.keys():

            if self.dictionary['chr'] == 'chrM':
                self.dictionary['chr'] = 'chrMT'

            if key in ['1000g20XX', 'esp6500si_all', 'nci60']:
                self.dictionary[key] = float(self.dictionary[key])

            if key in ['start', 'end']:
                self.dictionary[key] = int(self.dictionary[key])

            if key == 'cytoband':
                cytoband_data = CytoBand(self.dictionary['cytoband'])
                self.dictionary['cytoband'] = cytoband_data.fill()

            if key in ['genomicsuperdups', 'tfbsconssites']:
                self.dictionary[key] = self.to_dict(key)

            if key == 'otherinfo':
                self.dictionary[key] = re.split(r'\t+', self.dictionary[key].rstrip('\t'))

        self.dictionary['genotype'] = self.parse_genotype()

        return self.dictionary

    def parse_genotype(self):

        parser = vvp.VCFGenotypeStrings()
        genotype_to_fill = parser.parse(self.dictionary['otherinfo'][-2], self.dictionary['otherinfo'][-1])

        gen_dic = {'genotype': genotype_to_fill.genotype,
                   'filter_passing_reads_count': genotype_to_fill.filter_passing_reads_count,
                   'genotype_lieklihoods': [genotype_to_fill.genotype_likelihoods[0].likelihood_neg_exponent,
                                            genotype_to_fill.genotype_likelihoods[1].likelihood_neg_exponent,
                                            genotype_to_fill.genotype_likelihoods[2].likelihood_neg_exponent],
                   'alleles': [genotype_to_fill.alleles[0].read_counts, genotype_to_fill.alleles[1].read_counts]
                   }

        return gen_dic

    def to_dict(self, key):
        as_dict = dict(item.split("=") for item in self.dictionary[key].split(";"))
        as_dict["Score"] = float(as_dict["Score"])
        return as_dict


class CytoBand(object):

    def __init__(self, cyto_band_name):

        self.letters = set('XY')
        self.name = cyto_band_name
        self.processed = self.fill()

    def fill(self):

        processed = {'Name': self.name}
        spliced = re.split('(\D+)', self.name)

        if any((c in self.letters) for c in self.name):
            processed['Chromosome'] = spliced[1][0]
            processed['Band'] = spliced[1][1]
        else:
            processed['Chromosome'] = int(spliced[0])
            processed['Band'] = spliced[1]

        processed['Region'] = spliced[2]

        if '.' in spliced:
            processed['Sub_Band'] = spliced[-1]
        return processed

import io
import tempfile
import unittest

import VAPr.vapr_core as ns_ann_project
import VAPr.chunk_processing as ns_test
import VAPr.tests.test_annovar_output_parsing as ns_test_help


# TODO: someday: determine how to harden tests against myvariant.info's live updates that change its output

class TestAnnotationJobParamsIndices(unittest.TestCase):
    def test_get_num_possible_indices(self):
        real_output = ns_test.AnnotationJobParamsIndices.get_num_possible_indices()
        self.assertEqual(8, real_output)


class TestFunctions(unittest.TestCase):
    _VCF_FILE_CONTENTS = """##fileformat=VCFv4.1
##FILTER=<ID=PASS,Description="All filters passed">
##fileDate=20150218
##reference=ftp://ftp.1000genomes.ebi.ac.uk//vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz
##source=1000GenomesPhase3Pipeline
##contig=<ID=1,assembly=b37,length=249250621>
##contig=<ID=2,assembly=b37,length=243199373>
##contig=<ID=3,assembly=b37,length=198022430>
##contig=<ID=4,assembly=b37,length=191154276>
##contig=<ID=5,assembly=b37,length=180915260>
##contig=<ID=6,assembly=b37,length=171115067>
##contig=<ID=7,assembly=b37,length=159138663>
##contig=<ID=8,assembly=b37,length=146364022>
##contig=<ID=9,assembly=b37,length=141213431>
##contig=<ID=10,assembly=b37,length=135534747>
##contig=<ID=11,assembly=b37,length=135006516>
##contig=<ID=12,assembly=b37,length=133851895>
##contig=<ID=13,assembly=b37,length=115169878>
##contig=<ID=14,assembly=b37,length=107349540>
##contig=<ID=15,assembly=b37,length=102531392>
##contig=<ID=16,assembly=b37,length=90354753>
##contig=<ID=17,assembly=b37,length=81195210>
##contig=<ID=18,assembly=b37,length=78077248>
##contig=<ID=19,assembly=b37,length=59128983>
##contig=<ID=20,assembly=b37,length=63025520>
##contig=<ID=21,assembly=b37,length=48129895>
##contig=<ID=22,assembly=b37,length=51304566>
##contig=<ID=GL000191.1,assembly=b37,length=106433>
##contig=<ID=GL000192.1,assembly=b37,length=547496>
##contig=<ID=GL000193.1,assembly=b37,length=189789>
##contig=<ID=GL000194.1,assembly=b37,length=191469>
##contig=<ID=GL000195.1,assembly=b37,length=182896>
##contig=<ID=GL000196.1,assembly=b37,length=38914>
##contig=<ID=GL000197.1,assembly=b37,length=37175>
##contig=<ID=GL000198.1,assembly=b37,length=90085>
##contig=<ID=GL000199.1,assembly=b37,length=169874>
##contig=<ID=GL000200.1,assembly=b37,length=187035>
##contig=<ID=GL000201.1,assembly=b37,length=36148>
##contig=<ID=GL000202.1,assembly=b37,length=40103>
##contig=<ID=GL000203.1,assembly=b37,length=37498>
##contig=<ID=GL000204.1,assembly=b37,length=81310>
##contig=<ID=GL000205.1,assembly=b37,length=174588>
##contig=<ID=GL000206.1,assembly=b37,length=41001>
##contig=<ID=GL000207.1,assembly=b37,length=4262>
##contig=<ID=GL000208.1,assembly=b37,length=92689>
##contig=<ID=GL000209.1,assembly=b37,length=159169>
##contig=<ID=GL000210.1,assembly=b37,length=27682>
##contig=<ID=GL000211.1,assembly=b37,length=166566>
##contig=<ID=GL000212.1,assembly=b37,length=186858>
##contig=<ID=GL000213.1,assembly=b37,length=164239>
##contig=<ID=GL000214.1,assembly=b37,length=137718>
##contig=<ID=GL000215.1,assembly=b37,length=172545>
##contig=<ID=GL000216.1,assembly=b37,length=172294>
##contig=<ID=GL000217.1,assembly=b37,length=172149>
##contig=<ID=GL000218.1,assembly=b37,length=161147>
##contig=<ID=GL000219.1,assembly=b37,length=179198>
##contig=<ID=GL000220.1,assembly=b37,length=161802>
##contig=<ID=GL000221.1,assembly=b37,length=155397>
##contig=<ID=GL000222.1,assembly=b37,length=186861>
##contig=<ID=GL000223.1,assembly=b37,length=180455>
##contig=<ID=GL000224.1,assembly=b37,length=179693>
##contig=<ID=GL000225.1,assembly=b37,length=211173>
##contig=<ID=GL000226.1,assembly=b37,length=15008>
##contig=<ID=GL000227.1,assembly=b37,length=128374>
##contig=<ID=GL000228.1,assembly=b37,length=129120>
##contig=<ID=GL000229.1,assembly=b37,length=19913>
##contig=<ID=GL000230.1,assembly=b37,length=43691>
##contig=<ID=GL000231.1,assembly=b37,length=27386>
##contig=<ID=GL000232.1,assembly=b37,length=40652>
##contig=<ID=GL000233.1,assembly=b37,length=45941>
##contig=<ID=GL000234.1,assembly=b37,length=40531>
##contig=<ID=GL000235.1,assembly=b37,length=34474>
##contig=<ID=GL000236.1,assembly=b37,length=41934>
##contig=<ID=GL000237.1,assembly=b37,length=45867>
##contig=<ID=GL000238.1,assembly=b37,length=39939>
##contig=<ID=GL000239.1,assembly=b37,length=33824>
##contig=<ID=GL000240.1,assembly=b37,length=41933>
##contig=<ID=GL000241.1,assembly=b37,length=42152>
##contig=<ID=GL000242.1,assembly=b37,length=43523>
##contig=<ID=GL000243.1,assembly=b37,length=43341>
##contig=<ID=GL000244.1,assembly=b37,length=39929>
##contig=<ID=GL000245.1,assembly=b37,length=36651>
##contig=<ID=GL000246.1,assembly=b37,length=38154>
##contig=<ID=GL000247.1,assembly=b37,length=36422>
##contig=<ID=GL000248.1,assembly=b37,length=39786>
##contig=<ID=GL000249.1,assembly=b37,length=38502>
##contig=<ID=MT,assembly=b37,length=16569>
##contig=<ID=NC_007605,assembly=b37,length=171823>
##contig=<ID=X,assembly=b37,length=155270560>
##contig=<ID=Y,assembly=b37,length=59373566>
##contig=<ID=hs37d5,assembly=b37,length=35477943>
##ALT=<ID=CNV,Description="Copy Number Polymorphism">
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=DUP,Description="Duplication">
##ALT=<ID=INS:ME:ALU,Description="Insertion of ALU element">
##ALT=<ID=INS:ME:LINE1,Description="Insertion of LINE1 element">
##ALT=<ID=INS:ME:SVA,Description="Insertion of SVA element">
##ALT=<ID=INS:MT,Description="Nuclear Mitochondrial Insertion">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=CN0,Description="Copy number allele: 0 copies">
##ALT=<ID=CN1,Description="Copy number allele: 1 copy">
##ALT=<ID=CN2,Description="Copy number allele: 2 copies">
##ALT=<ID=CN3,Description="Copy number allele: 3 copies">
##ALT=<ID=CN4,Description="Copy number allele: 4 copies">
##ALT=<ID=CN5,Description="Copy number allele: 5 copies">
##ALT=<ID=CN6,Description="Copy number allele: 6 copies">
##ALT=<ID=CN7,Description="Copy number allele: 7 copies">
##ALT=<ID=CN8,Description="Copy number allele: 8 copies">
##ALT=<ID=CN9,Description="Copy number allele: 9 copies">
##ALT=<ID=CN10,Description="Copy number allele: 10 copies">
##ALT=<ID=CN11,Description="Copy number allele: 11 copies">
##ALT=<ID=CN12,Description="Copy number allele: 12 copies">
##ALT=<ID=CN13,Description="Copy number allele: 13 copies">
##ALT=<ID=CN14,Description="Copy number allele: 14 copies">
##ALT=<ID=CN15,Description="Copy number allele: 15 copies">
##ALT=<ID=CN16,Description="Copy number allele: 16 copies">
##ALT=<ID=CN17,Description="Copy number allele: 17 copies">
##ALT=<ID=CN18,Description="Copy number allele: 18 copies">
##ALT=<ID=CN19,Description="Copy number allele: 19 copies">
##ALT=<ID=CN20,Description="Copy number allele: 20 copies">
##ALT=<ID=CN21,Description="Copy number allele: 21 copies">
##ALT=<ID=CN22,Description="Copy number allele: 22 copies">
##ALT=<ID=CN23,Description="Copy number allele: 23 copies">
##ALT=<ID=CN24,Description="Copy number allele: 24 copies">
##ALT=<ID=CN25,Description="Copy number allele: 25 copies">
##ALT=<ID=CN26,Description="Copy number allele: 26 copies">
##ALT=<ID=CN27,Description="Copy number allele: 27 copies">
##ALT=<ID=CN28,Description="Copy number allele: 28 copies">
##ALT=<ID=CN29,Description="Copy number allele: 29 copies">
##ALT=<ID=CN30,Description="Copy number allele: 30 copies">
##ALT=<ID=CN31,Description="Copy number allele: 31 copies">
##ALT=<ID=CN32,Description="Copy number allele: 32 copies">
##ALT=<ID=CN33,Description="Copy number allele: 33 copies">
##ALT=<ID=CN34,Description="Copy number allele: 34 copies">
##ALT=<ID=CN35,Description="Copy number allele: 35 copies">
##ALT=<ID=CN36,Description="Copy number allele: 36 copies">
##ALT=<ID=CN37,Description="Copy number allele: 37 copies">
##ALT=<ID=CN38,Description="Copy number allele: 38 copies">
##ALT=<ID=CN39,Description="Copy number allele: 39 copies">
##ALT=<ID=CN40,Description="Copy number allele: 40 copies">
##ALT=<ID=CN41,Description="Copy number allele: 41 copies">
##ALT=<ID=CN42,Description="Copy number allele: 42 copies">
##ALT=<ID=CN43,Description="Copy number allele: 43 copies">
##ALT=<ID=CN44,Description="Copy number allele: 44 copies">
##ALT=<ID=CN45,Description="Copy number allele: 45 copies">
##ALT=<ID=CN46,Description="Copy number allele: 46 copies">
##ALT=<ID=CN47,Description="Copy number allele: 47 copies">
##ALT=<ID=CN48,Description="Copy number allele: 48 copies">
##ALT=<ID=CN49,Description="Copy number allele: 49 copies">
##ALT=<ID=CN50,Description="Copy number allele: 50 copies">
##ALT=<ID=CN51,Description="Copy number allele: 51 copies">
##ALT=<ID=CN52,Description="Copy number allele: 52 copies">
##ALT=<ID=CN53,Description="Copy number allele: 53 copies">
##ALT=<ID=CN54,Description="Copy number allele: 54 copies">
##ALT=<ID=CN55,Description="Copy number allele: 55 copies">
##ALT=<ID=CN56,Description="Copy number allele: 56 copies">
##ALT=<ID=CN57,Description="Copy number allele: 57 copies">
##ALT=<ID=CN58,Description="Copy number allele: 58 copies">
##ALT=<ID=CN59,Description="Copy number allele: 59 copies">
##ALT=<ID=CN60,Description="Copy number allele: 60 copies">
##ALT=<ID=CN61,Description="Copy number allele: 61 copies">
##ALT=<ID=CN62,Description="Copy number allele: 62 copies">
##ALT=<ID=CN63,Description="Copy number allele: 63 copies">
##ALT=<ID=CN64,Description="Copy number allele: 64 copies">
##ALT=<ID=CN65,Description="Copy number allele: 65 copies">
##ALT=<ID=CN66,Description="Copy number allele: 66 copies">
##ALT=<ID=CN67,Description="Copy number allele: 67 copies">
##ALT=<ID=CN68,Description="Copy number allele: 68 copies">
##ALT=<ID=CN69,Description="Copy number allele: 69 copies">
##ALT=<ID=CN70,Description="Copy number allele: 70 copies">
##ALT=<ID=CN71,Description="Copy number allele: 71 copies">
##ALT=<ID=CN72,Description="Copy number allele: 72 copies">
##ALT=<ID=CN73,Description="Copy number allele: 73 copies">
##ALT=<ID=CN74,Description="Copy number allele: 74 copies">
##ALT=<ID=CN75,Description="Copy number allele: 75 copies">
##ALT=<ID=CN76,Description="Copy number allele: 76 copies">
##ALT=<ID=CN77,Description="Copy number allele: 77 copies">
##ALT=<ID=CN78,Description="Copy number allele: 78 copies">
##ALT=<ID=CN79,Description="Copy number allele: 79 copies">
##ALT=<ID=CN80,Description="Copy number allele: 80 copies">
##ALT=<ID=CN81,Description="Copy number allele: 81 copies">
##ALT=<ID=CN82,Description="Copy number allele: 82 copies">
##ALT=<ID=CN83,Description="Copy number allele: 83 copies">
##ALT=<ID=CN84,Description="Copy number allele: 84 copies">
##ALT=<ID=CN85,Description="Copy number allele: 85 copies">
##ALT=<ID=CN86,Description="Copy number allele: 86 copies">
##ALT=<ID=CN87,Description="Copy number allele: 87 copies">
##ALT=<ID=CN88,Description="Copy number allele: 88 copies">
##ALT=<ID=CN89,Description="Copy number allele: 89 copies">
##ALT=<ID=CN90,Description="Copy number allele: 90 copies">
##ALT=<ID=CN91,Description="Copy number allele: 91 copies">
##ALT=<ID=CN92,Description="Copy number allele: 92 copies">
##ALT=<ID=CN93,Description="Copy number allele: 93 copies">
##ALT=<ID=CN94,Description="Copy number allele: 94 copies">
##ALT=<ID=CN95,Description="Copy number allele: 95 copies">
##ALT=<ID=CN96,Description="Copy number allele: 96 copies">
##ALT=<ID=CN97,Description="Copy number allele: 97 copies">
##ALT=<ID=CN98,Description="Copy number allele: 98 copies">
##ALT=<ID=CN99,Description="Copy number allele: 99 copies">
##ALT=<ID=CN100,Description="Copy number allele: 100 copies">
##ALT=<ID=CN101,Description="Copy number allele: 101 copies">
##ALT=<ID=CN102,Description="Copy number allele: 102 copies">
##ALT=<ID=CN103,Description="Copy number allele: 103 copies">
##ALT=<ID=CN104,Description="Copy number allele: 104 copies">
##ALT=<ID=CN105,Description="Copy number allele: 105 copies">
##ALT=<ID=CN106,Description="Copy number allele: 106 copies">
##ALT=<ID=CN107,Description="Copy number allele: 107 copies">
##ALT=<ID=CN108,Description="Copy number allele: 108 copies">
##ALT=<ID=CN109,Description="Copy number allele: 109 copies">
##ALT=<ID=CN110,Description="Copy number allele: 110 copies">
##ALT=<ID=CN111,Description="Copy number allele: 111 copies">
##ALT=<ID=CN112,Description="Copy number allele: 112 copies">
##ALT=<ID=CN113,Description="Copy number allele: 113 copies">
##ALT=<ID=CN114,Description="Copy number allele: 114 copies">
##ALT=<ID=CN115,Description="Copy number allele: 115 copies">
##ALT=<ID=CN116,Description="Copy number allele: 116 copies">
##ALT=<ID=CN117,Description="Copy number allele: 117 copies">
##ALT=<ID=CN118,Description="Copy number allele: 118 copies">
##ALT=<ID=CN119,Description="Copy number allele: 119 copies">
##ALT=<ID=CN120,Description="Copy number allele: 120 copies">
##ALT=<ID=CN121,Description="Copy number allele: 121 copies">
##ALT=<ID=CN122,Description="Copy number allele: 122 copies">
##ALT=<ID=CN123,Description="Copy number allele: 123 copies">
##ALT=<ID=CN124,Description="Copy number allele: 124 copies">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##INFO=<ID=CIEND,Number=2,Type=Integer,Description="Confidence interval around END for imprecise variants">
##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS for imprecise variants">
##INFO=<ID=CS,Number=1,Type=String,Description="Source call set.">
##INFO=<ID=END,Number=1,Type=Integer,Description="End coordinate of this variant">
##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">
##INFO=<ID=MC,Number=.,Type=String,Description="Merged calls.">
##INFO=<ID=MEINFO,Number=4,Type=String,Description="Mobile element info of the form NAME,START,END<POLARITY; If there is only 5' OR 3' support for this call, will be NULL NULL for START and END">
##INFO=<ID=MEND,Number=1,Type=Integer,Description="Mitochondrial end coordinate of inserted sequence">
##INFO=<ID=MLEN,Number=1,Type=Integer,Description="Estimated length of mitochondrial insert">
##INFO=<ID=MSTART,Number=1,Type=Integer,Description="Mitochondrial start coordinate of inserted sequence">
##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="SV length. It is only calculated for structural variation MEIs. For other types of SVs; one may calculate the SV length by INFO:END-START+1, or by finding the difference between lengthes of REF and ALT alleles">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=TSD,Number=1,Type=String,Description="Precise Target Site Duplication for bases, if unknown, value will be NULL">
##INFO=<ID=AC,Number=A,Type=Integer,Description="Total number of alternate alleles in called genotypes">
##INFO=<ID=AF,Number=A,Type=Float,Description="Estimated allele frequency in the range (0,1)">
##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of samples with data">
##INFO=<ID=AN,Number=1,Type=Integer,Description="Total number of alleles in called genotypes">
##INFO=<ID=EAS_AF,Number=A,Type=Float,Description="Allele frequency in the EAS populations calculated from AC and AN, in the range (0,1)">
##INFO=<ID=EUR_AF,Number=A,Type=Float,Description="Allele frequency in the EUR populations calculated from AC and AN, in the range (0,1)">
##INFO=<ID=AFR_AF,Number=A,Type=Float,Description="Allele frequency in the AFR populations calculated from AC and AN, in the range (0,1)">
##INFO=<ID=AMR_AF,Number=A,Type=Float,Description="Allele frequency in the AMR populations calculated from AC and AN, in the range (0,1)">
##INFO=<ID=SAS_AF,Number=A,Type=Float,Description="Allele frequency in the SAS populations calculated from AC and AN, in the range (0,1)">
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth; only low coverage data were counted towards the DP, exome data were not used">
##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele. Format: AA|REF|ALT|IndelType. AA: Ancestral allele, REF:Reference Allele, ALT:Alternate Allele, IndelType:Type of Indel (REF, ALT and IndelType are only defined for indels)">
##INFO=<ID=VT,Number=.,Type=String,Description="indicates what type of variant the line represents">
##INFO=<ID=EX_TARGET,Number=0,Type=Flag,Description="indicates whether a variant is within the exon pull down target boundaries">
##INFO=<ID=MULTI_ALLELIC,Number=0,Type=Flag,Description="indicates whether a site is multi-allelic">
##bcftools_viewVersion=1.6+htslib-1.6
##bcftools_viewCommand=view -c1 -Oz -s HG00096 -o G1000_chr1_10000_20000.HG00096.vcf.gz G1000_chr1_10000_20000.vcf.gz; Date=Mon Nov  6 15:48:17 2017
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	HG00096
1	10177	rs367896724	A	AC	100	PASS	AC=1;AF=0.425319;AN=2;NS=2504;DP=103152;EAS_AF=0.3363;AMR_AF=0.3602;AFR_AF=0.4909;EUR_AF=0.4056;SAS_AF=0.4949;AA=|||unknown(NO_COVERAGE);VT=INDEL	GT	1|0
1	10352	rs555500075	T	TA	100	PASS	AC=1;AF=0.4375;AN=2;NS=2504;DP=88915;EAS_AF=0.4306;AMR_AF=0.4107;AFR_AF=0.4788;EUR_AF=0.4264;SAS_AF=0.4192;AA=|||unknown(NO_COVERAGE);VT=INDEL	GT	1|0
M	10616	rs376342519	CCGCCGTTGCAAAGGCGCGCCG	C	100	PASS	AC=2;AF=0.993011;AN=2;NS=2504;DP=2365;EAS_AF=0.9911;AMR_AF=0.9957;AFR_AF=0.9894;EUR_AF=0.994;SAS_AF=0.9969;VT=INDEL	GT	1|1
1	14464	rs546169444	A	T	100	PASS	AC=2;AF=0.0958466;AN=2;NS=2504;DP=26761;EAS_AF=0.005;AMR_AF=0.1138;AFR_AF=0.0144;EUR_AF=0.1859;SAS_AF=0.1943;AA=a|||;VT=SNP	GT	1|1
M	14930	rs75454623	A	G	100	PASS	AC=1;AF=0.482228;AN=2;NS=2504;DP=42231;EAS_AF=0.4137;AMR_AF=0.5231;AFR_AF=0.4811;EUR_AF=0.5209;SAS_AF=0.4857;AA=a|||;VT=SNP	GT	1|0
M	15211	rs78601809	T	G	100	PASS	AC=1;AF=0.609026;AN=2;NS=2504;DP=32245;EAS_AF=0.504;AMR_AF=0.6772;AFR_AF=0.5371;EUR_AF=0.7316;SAS_AF=0.6401;AA=t|||;VT=SNP	GT	0|1
1	15274	rs62636497	A	G,T	100	PASS	AC=1,1;AF=0.347244,0.640974;AN=2;NS=2504;DP=23255;EAS_AF=0.4812,0.5188;AMR_AF=0.2752,0.7205;AFR_AF=0.323,0.6369;EUR_AF=0.2922,0.7078;SAS_AF=0.3497,0.6472;AA=g|||;VT=SNP;MULTI_ALLELIC	GT	1|2
1	15820	rs2691315	G	T	100	PASS	AC=1;AF=0.410543;AN=2;NS=2504;DP=14933;EAS_AF=0.6052;AMR_AF=0.2939;AFR_AF=0.4849;EUR_AF=0.2714;SAS_AF=0.3354;AA=t|||;VT=SNP;EX_TARGET	GT	1|0
1	15903	rs557514207	G	GC	100	PASS	AC=1;AF=0.441094;AN=2;NS=2504;DP=7012;EAS_AF=0.8681;AMR_AF=0.415;AFR_AF=0.0431;EUR_AF=0.4652;SAS_AF=0.5327;AA=ccc|CC|CCC|deletion;VT=INDEL;EX_TARGET	GT	0|1
1	18849	rs533090414	C	G	100	PASS	AC=2;AF=0.951877;AN=2;NS=2504;DP=4700;EAS_AF=1;AMR_AF=0.9769;AFR_AF=0.8411;EUR_AF=0.9911;SAS_AF=0.9939;AA=g|||;VT=SNP	GT	1|1
"""

    # region _collect_chunk_annotations tests
    def test__collect_chunk_annotations_with_sample_info(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(ns_test_help.TestAnnovarTxtParser.ANNOVAR_ANNOTATION_CONTENT.encode('ascii'))
        temp_file.close()  # but DON'T delete yet

        input_params_tuple = (1, temp_file.name, 4, "dummy_name", "dummy_collection_name",
                              ns_ann_project.VaprAnnotator.DEFAULT_GENOME_VERSION, 1,
                              ['test_sample1', 'test_sample2'])
        expected_output = [
            {'chr': 'chrMT', 'start': 146, 'end': 146, 'ref': 'T', 'alt': 'C', 'func_knowngene': 'upstream;downstream',
             'gene_knowngene': 'JB137816;DQ582201', 'hgvs_id': 'chrMT:g.146T>C', 'samples': [
                {'sample_id': 'test_sample1', 'genotype': '1/1', 'genotype_subclass_by_class': {'homozygous': 'alt'},
                 'filter_passing_reads_count': 2, 'genotype_likelihoods': [90.0, 6.0, 0.0], 'AD': [0, 2]}],
             'dbsnp': {'_license': 'https://goo.gl/Ztr5rl', 'rsid': 'rs370482130'},
             'wellderly': {'_license': 'https://goo.gl/e8OO17', 'alleles': [
                 {'allele': 'C', 'freq': 0.0625}, {'allele': 'T', 'freq': 0.9375}]}},
            {'chr': 'chrMT', 'start': 150, 'end': 150, 'ref': 'T', 'alt': 'C', 'func_knowngene': 'upstream;downstream',
             'gene_knowngene': 'JB137816;DQ582201', 'hgvs_id': 'chrMT:g.150T>C', 'samples': [
                {'sample_id': 'test_sample2', 'genotype': '1/1', 'genotype_subclass_by_class': {'homozygous': 'alt'},
                 'filter_passing_reads_count': 2, 'genotype_likelihoods': [90.0, 6.0, 0.0], 'AD': [0, 2]}],
             'wellderly': {'_license': 'https://goo.gl/e8OO17', 'alleles': [
                 {'allele': 'C', 'freq': 0.83}, {'allele': 'T', 'freq': 0.17}]}},
            {'chr': 'chr1', 'start': 195, 'end': 195, 'ref': 'C', 'alt': 'T', 'func_knowngene': 'upstream;downstream',
             'gene_knowngene': 'JB137816;DQ582201', 'hgvs_id': 'chr1:g.195C>T', 'samples': [
                {'sample_id': 'test_sample1', 'genotype': '1/1', 'genotype_subclass_by_class': {'homozygous': 'alt'},
                 'filter_passing_reads_count': 2, 'genotype_likelihoods': [89.0, 6.0, 0.0], 'AD': [0, 2]},
                {'sample_id': 'test_sample2', 'genotype': '1/1', 'genotype_subclass_by_class': {'homozygous': 'alt'},
                 'filter_passing_reads_count': 3, 'genotype_likelihoods': [135.0, 9.0, 0.0], 'AD': [0, 3]}],
             'notfound': True},
            {'chr': 'chrMT', 'start': 410, 'end': 410, 'ref': 'A', 'alt': 'T', 'func_knowngene': 'upstream',
             'gene_knowngene': 'DQ582201,JB137816', 'hgvs_id': 'chrMT:g.410A>T', 'samples': [],
             'wellderly': {'_license': 'https://goo.gl/e8OO17', 'alleles': [
                 {'allele': 'A', 'freq': 0.0}, {'allele': 'T', 'freq': 1.0}]}}]
        real_output = ns_test._collect_chunk_annotations(input_params_tuple)
        self.assertListEqual(expected_output, real_output)

    def test__collect_chunk_annotations_no_sample_info(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(self._VCF_FILE_CONTENTS.encode('ascii'))
        temp_file.close()  # but DON'T delete yet

        input_params_tuple = (1, temp_file.name, 2, "dummy_name", "dummy_collection_name",
                              ns_ann_project.VaprAnnotator.DEFAULT_GENOME_VERSION, 1)
        expected_output = [{'notfound': True, 'hgvs_id': 'chrMT:g.10617_10637del'},
                           {'cadd': {'_license': 'http://goo.gl/bkpNhq', 'gerp': {'n': 0.848, 's': -1.7},
                                     'phred': 0.603},
                            'dbsnp': {'_license': 'https://goo.gl/Ztr5rl', 'rsid': 'rs546169444'},
                            'wellderly': {'_license': 'https://goo.gl/e8OO17',
                                          'alleles': [{'allele': 'A', 'freq': 0.87},
                                                      {'allele': 'T', 'freq': 0.13}]},
                            'hgvs_id': 'chr1:g.14464A>T'}]
        real_output = ns_test._collect_chunk_annotations(input_params_tuple)
        self.assertListEqual(expected_output, real_output)

    # endregion

    def test__get_hgvs_ids_from_vcf(self):
        # NB: first 2 variants in the vcf are ignored because test starts on chunk index = 1 (i.e., the second chunk)
        # and the chunk size is 2.  Likewise, since the test only processes a single 2-variant chunk, the last 6
        # variants are ignored.  This is as expected and demonstrates that the chunking functionality is working
        # correctly.  Note that the variant listed as coming from chromosome 'M' in vcf is rewritten as from
        # chromosome MT.
        input_vcf_stream = io.StringIO(self._VCF_FILE_CONTENTS)
        expected_output = ["chrMT:g.10617_10637del", "chr1:g.14464A>T"]
        real_output = ns_test._get_hgvs_ids_from_vcf(input_vcf_stream, 1, 2)
        self.assertListEqual(expected_output, real_output)

    # region _get_myvariantinfo_annotations_dict tests
    def test__get_myvariantinfo_annotations_dict(self):
        # TODO: someday: test for effect of verbose_level, genome build version?  What effects are expected?
        input_hgvs_ids = ["chrMT:g.146T>C", "chr1:g.195C>T"]
        expected_output = [{'dbsnp': {'_license': 'https://goo.gl/Ztr5rl', 'rsid': 'rs370482130'},
                            'wellderly': {'_license': 'https://goo.gl/e8OO17',
                                          'alleles': [{'allele': 'C', 'freq': 0.0625},
                                                      {'allele': 'T', 'freq': 0.9375}]},
                            'hgvs_id': 'chrMT:g.146T>C'},
                           {'notfound': True, 'hgvs_id': 'chr1:g.195C>T'}]
        real_output = ns_test._get_myvariantinfo_annotations_dict(
            input_hgvs_ids, ns_ann_project.VaprAnnotator.DEFAULT_GENOME_VERSION, verbose_level=0)
        self.assertListEqual(expected_output, real_output)

    # NB: I have no good way to test the error-after-retry case as it is triggered by errors I can't easily fudge
    # (like lack of internet connection).  I do not think testing it is worth the considerable mocking effort needed.

    def test__get_myvariantinfo_annotations_dict_fatal_error_immediately(self):
        # sending in a None value for the list of ids causes a ValueError that can't be recovered from
        with self.assertRaises(ValueError):
            ns_test._get_myvariantinfo_annotations_dict(
                None, ns_ann_project.VaprAnnotator.DEFAULT_GENOME_VERSION, verbose_level=0, num_failed_attempts=4)

    # endregion

    def test__remove_unwanted_keys(self):
        input_dicts_list = [{'query': 'chrMT:g.146T>C',
                             '_id': 'chrMT:g.146T>C',
                             'dbsnp': {'_license': 'https://goo.gl/Ztr5rl', 'rsid': 'rs370482130'},
                             'wellderly': {'_license': 'https://goo.gl/e8OO17',
                                           'alleles': [{'freq': 0.0625}, {'freq': 0.9375}]}},
                            {'query': 'chr1:g.195C>T', 'notfound': True}]

        expected_output = [{'dbsnp': {'_license': 'https://goo.gl/Ztr5rl', 'rsid': 'rs370482130'},
                            'wellderly': {'_license': 'https://goo.gl/e8OO17',
                                          'alleles': [{'freq': 0.0625}, {'freq': 0.9375}]},
                            'hgvs_id': 'chrMT:g.146T>C'},
                           {'notfound': True, 'hgvs_id': 'chr1:g.195C>T'}]
        real_output = ns_test._remove_unwanted_keys(input_dicts_list)
        self.assertListEqual(expected_output, real_output)

    # region _merge_annovar_and_myvariant_dicts tests
    def test__merge_annovar_and_myvariant_dicts(self):
        myvariantinfo_input_dict = {'dbsnp': {'_license': 'https://goo.gl/Ztr5rl', 'rsid': 'rs370482130'},
                                    'wellderly': {'_license': 'https://goo.gl/e8OO17',
                                                  'alleles': [{'freq': 0.0625}, {'freq': 0.9375}]},
                                    'hgvs_id': 'chrMT:g.146T>C'}
        annovar_input_dict = {'chr': 'chrMT', 'start': 146, 'end': 146, 'ref': 'T', 'alt': 'C',
                              'func_knowngene': 'upstream;downstream',
                              'gene_knowngene': 'JB137816;DQ582201', 'hgvs_id': 'chrMT:g.146T>C', 'samples': [
                {'sample_id': 'test_sample1', 'genotype': '1/1',
                 'genotype_subclass_by_class': {'homozygous': 'alt'},
                 'filter_passing_reads_count': 2, 'genotype_likelihoods': [90.0, 6.0, 0.0],
                 'AD': [0, 2]}
            ]}
        expected_output = {'chr': 'chrMT', 'start': 146, 'end': 146, 'ref': 'T', 'alt': 'C',
                           'func_knowngene': 'upstream;downstream',
                           'gene_knowngene': 'JB137816;DQ582201', 'hgvs_id': 'chrMT:g.146T>C', 'samples': [
                {'sample_id': 'test_sample1', 'genotype': '1/1',
                 'genotype_subclass_by_class': {'homozygous': 'alt'},
                 'filter_passing_reads_count': 2, 'genotype_likelihoods': [90.0, 6.0, 0.0],
                 'AD': [0, 2]}
            ], 'dbsnp': {'_license': 'https://goo.gl/Ztr5rl', 'rsid': 'rs370482130'},
                           'wellderly': {'_license': 'https://goo.gl/e8OO17',
                                         'alleles': [{'freq': 0.0625}, {'freq': 0.9375}]}}

        real_output = ns_test._merge_annovar_and_myvariant_dicts(myvariantinfo_input_dict, annovar_input_dict)
        self.assertDictEqual(expected_output, real_output)

    def test__merge_annovar_and_myvariant_dicts_error(self):
        myvariantinfo_input_dict = {'dbsnp': {'_license': 'https://goo.gl/Ztr5rl', 'rsid': 'rs370482130'},
                                    'wellderly': {'_license': 'https://goo.gl/e8OO17',
                                                  'alleles': [{'freq': 0.0625}, {'freq': 0.9375}]},
                                    'hgvs_id': 'chrMT:g.148T>C'}
        annovar_input_dict = {'chr': 'chrMT', 'start': 146, 'end': 146, 'ref': 'T', 'alt': 'C',
                              'func_knowngene': 'upstream;downstream',
                              'gene_knowngene': 'JB137816;DQ582201', 'hgvs_id': 'chrMT:g.146T>C', 'samples': [
                {'sample_id': 'test_sample1', 'genotype': '1/1',
                 'genotype_subclass_by_class': {'homozygous': 'alt'},
                 'filter_passing_reads_count': 2, 'genotype_likelihoods': [90.0, 6.0, 0.0],
                 'AD': [0, 2]}
            ]}

        with self.assertRaises(ValueError):
            ns_test._merge_annovar_and_myvariant_dicts(myvariantinfo_input_dict, annovar_input_dict)

    # endregion

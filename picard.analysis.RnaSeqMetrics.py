import os
import csv
import glob
import datetime

header = list()
admin = 'NA'
date = datetime.datetime.now().strftime("%m%d%y")

# test dir
# cwd = '/Users/ltrani/Desktop/git/qc/picard.analysis.RnaSeqMetrics/2856583'

# get cwd
cwd = os.getcwd()
os.chdir(cwd)

cwd_split = cwd.split('/')
for dir in cwd_split:
    if '285' in dir:
        woid = dir

metric_files = glob.glob('*_rna_metrics.txt')

if len(metric_files) == 0:
    print("No rna_metrics files found")
    exit()
if os.path.exists(woid +'.picard.analysis.metrics.tsv'):
    os.remove(woid + '.picard.analysis.metrics.tsv')

for file in metric_files:
    build = file.split('/')[0].split('_')[0]
    with open(file, 'r') as infiletxt, open( woid + '.picard.analysis.metrics.tsv', 'a') as outfiletsv:
        # process file
        for line in infiletxt:
            # print metric lines from metric files
            if 'PF_BASES' in line:
                if len(header) == 0:
                    header = line.strip().split("\t")
                    header = header[:-3]
                    header = ['Admin', 'WOID', 'QC Date', 'BUILD'] + header + ['PCT_SUM', 'ALIGNMENT_RATE']
                    outfile_writer = csv.writer(outfiletsv, delimiter='\t')
                    outfile_writer.writerow(header)

                # find metrics line, first line after PF_BASES
                data = next(infiletxt).strip().split("\t")

                # PCT_SUM: add column: PCT_CODING_BASES + PCT_UTR_BASES + PCT_INTRONIC_BASES
                # ALIGNMENT_RATE: PF_ALIGNED_BASES / PF_BASES
                pct_sum = float(data[16]) + float(data[17]) + float(data[18])
                align_rate = float(data[1]) / float(data[0])
                data = [admin, woid, date,  build] + data + [pct_sum, align_rate]
                outfile_writer = csv.writer(outfiletsv, delimiter='\t')
                outfile_writer.writerow(data)

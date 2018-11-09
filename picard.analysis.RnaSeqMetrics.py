import os
import csv
import glob

header = list()

cwd = '/Users/ltrani/Desktop/git/qc/picard.analysis.RnaSeqMetrics/2856583'

os.chdir(cwd)

metric_files = glob.glob('*_rna_metrics.txt')

if len(metric_files) == 0:
    print("No rna_metrics files found")
    exit()
if os.path.exists('picard.analysis.metrics.tsv'):
    os.remove('picard.analysis.metrics.tsv')

for file in metric_files:
    build = file.split('/')[0].split('_')[0]
    print(build)
    with open(file, 'r') as infiletxt, open('picard.analysis.metrics.tsv', 'a') as outfiletsv:
        # process file
        for line in infiletxt:
            # print metric lines from metric files
            if 'PF_BASES' in line:
                if len(header) == 0:
                    header = line.strip().split("\t")
                    header = header[:-3]
                    header.insert(0, 'BUILD')
                    outfile_writer = csv.writer(outfiletsv, delimiter='\t')
                    outfile_writer.writerow(header)

                # find metrics line, first line after PF_BASES
                data = next(infiletxt).strip().split("\t")
                # add build id
                data.insert(0, build)
                outfile_writer = csv.writer(outfiletsv, delimiter='\t')
                outfile_writer.writerow(data)
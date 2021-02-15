import csv
import os


def split(filehandler, delimiter=',', row_limit=100,
          output_name_template='output_%s.csv', output_path='.'):
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
        current_out_writer.writerow(row)


split(open('neg_tweet.csv', 'r'), output_name_template='neg_%s.csv')
split(open('pos_tweet.csv', 'r'), output_name_template='pos_%s.csv')

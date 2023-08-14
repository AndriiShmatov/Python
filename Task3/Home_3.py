import csv
import requests
import logging
import argparse
from datetime import datetime, timedelta
import os
from collections import Counter
import shutil


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    args = provide_parameters()
    logging.info('Parameters provided')

    file = get_data()
    logging.info('Data fetched from API')

    write_csv(file)
    logging.info('Data written to CSV file')

    data = read_file()
    logging.info('CSV file is read')

    filt = filters(args, data)
    logging.info('Data was filtered')

    change_filt = add_fields(filt)
    logging.info('Fields added to data')

    add_new_data(change_filt)
    logging.info('New data added to CSV file')

    old_dir = os.getcwd()
    create_destination_folder(args.destination_folder)
    os.chdir(args.destination_folder)
    # os.rename(os.path.join(old_dir, f'{args.filename}.csv'),
    #           os.path.join(args.destination_folder, f'{args.filename}.csv'))

    decade = rearrange_the_data(change_filt)
    logging.info('Data rearranged')

    create_sub_folders(decade)
    logging.info('Subfolders created')

    remove_the_data(args.destination_folder)
    logging.info('Data removed')

    log_full_folder_structure(args.destination_folder)

    archive_destination_folder(args.destination_folder)
    logging.info('File successfully archived')


def filters(args, data):
    if args.gender:
        return filter_data_by_gender(data, args.gender)
    elif args.n_rows:
        return filter_data_by_n_rows(data, args.n_rows)


def provide_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination_folder', required=True)
    parser.add_argument('--filename', default='output')
    parser.add_argument('log_level')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gender')
    group.add_argument('--n_rows', type=int)
    args = parser.parse_args()
    return args


def get_data():
    link = 'https://randomuser.me/api/?format=csv&results=50'
    resp = requests.get(url=link)
    return resp.text


def write_csv(csv_string):
    with open("output.csv", "w", encoding='utf-8') as text_file:
        text_file.write(csv_string)


def add_new_data(change_filt):
    with open("output.csv", "w", newline='', encoding='utf-8') as text_file:
        writer = csv.DictWriter(text_file, fieldnames=change_filt[0].keys())
        writer.writeheader()
        writer.writerows(change_filt)
    return writer


def read_file():
    with open('output.csv', 'r', encoding='utf-8') as csv_file:
        reader = list(csv.DictReader(csv_file))
    return reader


def filter_data_by_gender(data, gender):
    filtered_data = []
    for row in data:
        if row['gender'] == gender:
            filtered_data.append(row)
    return filtered_data


def filter_data_by_n_rows(data, n_rows):
    filtered_data = data[:n_rows]
    return filtered_data


def add_fields(filt):
    for i, row in enumerate(filt, start=1):
        row['global_index'] = i
        row['current_time'] = create_user_timezone(row['location.timezone.offset'])
        row['name.title'] = change_the_name_title(row['name.title'])
        row['dob.date'] = convert_time(row['dob.date'], '%m/%d/%y')
        row['registered.date'] = convert_time(row['registered.date'], '%m/%d/%y, %H:%M:%S')
    return filt


def create_user_timezone(row_time):
    user_time = row_time.split(':')
    current_time = datetime.now() + timedelta(hours=int(user_time[0]), minutes=int(user_time[1]))
    return current_time.strftime('%y-%m-%d %H-%M-%S')


def change_the_name_title(title):
    if title == 'Mr':
        return 'mister'
    elif title == 'Madame':
        return 'mademoiselle'
    elif title == 'Mrs':
        return 'missis'
    elif title == 'Ms':
        return 'miss'
    else:
        return title


def convert_time(user_date, time_format):
    return datetime.strptime(user_date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime(time_format)


def create_destination_folder(destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)


def rearrange_the_data(change_filt):
    dates = {}
    for date in change_filt:
        x = date['dob.date'][-2]
        if f'{x}0-th' not in dates:
            dates[f'{x}0-th'] = {}
        h = date['location.country']
        if f'{h}' not in dates[f'{x}0-th']:
            dates[f'{x}0-th'][h] = []
        dates[f'{x}0-th'][h].append(date)
    return dates


def create_sub_folders(data):
    for decade in data:
        os.makedirs(decade)
        for country in data[decade]:
            os.makedirs(f'{decade}\\{country}')
            name_files = create_name_of_the_file(data[decade][country])
            store_the_data(f'{decade}\\{country}\\{name_files}', data[decade][country])


def store_the_data(name_files, data):
    with open(name_files, 'w', encoding='utf-8') as text_file:
        csv_writer = csv.DictWriter(text_file, fieldnames=data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(data)


def create_name_of_the_file(user_data):
    max_age = int(max(user_data, key=lambda k: k['dob.age'])['dob.age'])
    reg_ages = [int(f['registered.age']) for f in user_data]
    average = sum(reg_ages)/len(reg_ages)
    popular_ids = [f['id.name'] for f in user_data]
    common_id = Counter(popular_ids).most_common(1)[0][0]
    return f'max_age_{max_age}_avg_registered_{average}_popular_id_{common_id}.csv'


def remove_the_data(decade):
    for row in os.listdir(decade):
        if row[0] <= '6':
            shutil.rmtree(f'{decade}/{row}')


def log_full_folder_structure(folder):
    for root, dirs, files in os.walk(folder):
        level = root.count(os.sep)
        indent = '    ' * level
        logging.info(f'{indent}Folder: {os.path.basename(root)}')
        for file in files:
            logging.info(f'    {indent}File: {file}')


def archive_destination_folder(destination_folder):
    os.chdir('D:/')
    shutil.make_archive('Archive_Task3', 'zip', base_dir=destination_folder)


if __name__ == '__main__':
    main()

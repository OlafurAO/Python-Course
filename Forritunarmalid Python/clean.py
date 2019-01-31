import shutil;
import sys;
import re;
import os;

#def clean_up(show_folder):

#Delves into the subdirectories and orders them into the
#appropriate folders in the show directory
def organize_directories(download_folder, show_folder, file_types):
    for subdir, dirs, files in os.walk(download_folder):
        for file in files:
            item_list = check_show_and_season(file, file_types);

            if (item_list == None or item_list[1] == None):
                continue;

            src = os.path.join(subdir, file);
            #src = os.path.abspath(src);

            if(item_list[0] == ''):
                item_list[0] = 'Frasier';

            if (int(item_list[1]) > 9):
                dest = os.path.join(show_folder, item_list[0], 'Season ' + item_list[1]);
            else:
                dest = os.path.join(show_folder, item_list[0], 'Season 0' + item_list[1]);

            #dest = os.path.abspath(dest);
            if('Sample' in dest):
                continue;

            print(dest)

            if not (os.path.exists(dest)):
                os.makedirs(dest);

            shutil.copy(src, dest);

#returns a list that includes the name of the show and
#the season number, returns None if it has no season number
#i.e. if it isn't a show
def check_show_and_season(item, file_types):
    if(item.endswith(file_types)):
        item = item.title();
        title = clean_title(item);
        season = find_season(item);
        item_list = [];

        item_list.append(title);
        item_list.append(season);

        if(season is None or item_list[1] is None or item_list[1] is '' or item_list[1] is ' '):
            return None;
        else:
            return item_list;
    else:
        return None;

#Finds what looks to be the season number and returns its value
def find_season(item):
    season = re.findall('S\d\d', item);
    if(season is None):
        season = re.findall('S\d', item);

        if(season is None):
            season = re.findall('\d\d\d\d\s', item);

            if('(' not in season and ')' not in season):
                season = str(season);
                total = '0';
                count = 0;
                for i in season:
                    if(i.isdigit()):
                        if(int(i) > 0 and count < 2):
                            total += i;
                            count += 1;
                return total;

            else:
                return None;
        else:
            season = str(season);
            total = '0';
            for i in season:
                if(i.isdigit()):
                    if(int(i) > 0):
                        total += i;

            return total;
    else:
        season = str(season);
        total = '';
        for i in season:
            if(i.isdigit()):
                if(int(i) > 0):
                    total += i;

        return total;

#Cleans all the rubbish from the title, like season number, periods, 'HDTV', 'XviD' etc.
def clean_title(item):
    item = item.title();
    if("'" in item):
        item = item.replace("'", '');
        item = item.title();
    if('.' in item):
        item = item.replace('.', ' ');
    if('_' in item):
        item = item.replace('_', ' ');
    if(' - ' in item):
        item = item.replace(' - ', ' ');
    if('-' in item):
        item = item.replace('-', ' ');
    if('  ' in item):
        item = item.replace('  ', ' ');
    if(' ' in item):
        item = item.replace(' ', ' ');
    if('(' in item):
        item = re.sub('(\(.*)$', '', item);
    if('!' in item):
        item = item.replace('!', item);
    if(re.search('\d-\d', item)):
        item = re.sub('\d-\d', '', item);
    if(re.search('Season\s\d', item)):
        item = re.sub('Season\s\d(.*)$', '', item);
    if(re.search('S\d\d', item)):
        item = re.sub('S\d\d(.*)$', '', item);
    if(re.search('S\d', item)):
        item = re.sub('S\d(.*)$', '', item);
    if(re.search('Season', item)):
        item = re.sub('Season(.*)$', '', item);
    if(re.search('Sería', item)):
        item = re.sub('Sería(.*)$', '', item);
    if(re.search('Seria', item)):
        item = re.sub('Seria(.*)$', '', item);
    if(re.search('\d\sSería', item)):
        item = re.sub('\d\sSería(.*)$', '', item);
    if(re.search('Sería\s\d', item)):
        item = re.sub('Sería\s\d(.*)$', '', item);
    if(re.search('\d\sSeria', item)):
        item = re.sub('\d\sSeria(.*)$', '', item);
    if(re.search('Seria\s\d', item)):
        item = re.sub('Seria\s\d(.*)$', '', item);
    if(re.search('\d\dX\d\d', item)):
        item = re.sub('\d\dX\d\d(.*)$', '', item);
    if(re.search('\d\d\d\d', item)):
        item = re.sub('\d\d\d\d(.*)$', '', item);

    return item.strip();

#Removes all the empty directories
def remove_empty_dirs(show_folder):
    for subdir, dirs, files in os.walk(show_folder):
        for d in dirs:
            if not(os.listdir(os.path.join(subdir, d))):
                os.removedirs(os.path.join(subdir, d));
    return;

def main():
    file_types = ('.mp4', '.avi', '.mkv', '.mov');

    download_folder, show_folder = sys.argv[1:];

    organize_directories(download_folder, show_folder, file_types);
    remove_empty_dirs(show_folder);
    return;

if __name__ == '__main__':
    main();
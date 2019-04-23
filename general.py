import os
import codecs
import string
import random
from domain_features import hardRules


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, "crawled.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Create a new file
def write_file(path, data):
    with codecs.open(path, 'w', "utf-8") as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with codecs.open(path, 'a', "utf-8") as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with codecs.open(file_name, 'r', "utf-8") as f:
        for line in f:
            url = line.replace('\n', '')
            if not hardRules(url):
                results.add(url)
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with codecs.open(file_name, "w", "utf-8") as f:
        for l in list(links):
            f.write(l + "\n")


def randomString(stringLength=8):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

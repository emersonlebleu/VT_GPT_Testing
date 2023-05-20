#Reads and writes to files
import os
from os import path
from settings import BASE_PATH

def new_soup(file_name='soup.txt', folder='bs_files'):
    #Creates a new file with the name and folder returns the file path
    file_path = os.path.join(BASE_PATH, folder, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    new_soup = open(file_path, 'w')
    new_soup.close()
    
    return file_path

def write_soup(soup_body, file_path):
    #Writes only the body of the soup to the file
    with open(file_path, 'w') as file:
        file.write(soup_body)

def read_soup_body(file_path):
    #Reads the soup from the file returns the text of the body
    with open(file_path, 'r') as file:
        body_html = file.read()
    return body_html

def write_output(text, file_name, folder='output_files'):
    file_path = os.path.join(BASE_PATH, folder, file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
    
    new_output_file = open(file_path, 'w')
    new_output_file.close()
    #Writes the text to the file
    with open(file_path, 'w') as file:
        file.write(text)

def read_output(file_name, folder='output_files'):
    #Reads the output from the file returns the text
    file_path = os.path.join(BASE_PATH, folder, file_name)
    with open(file_path, 'r') as file:
        output = file.read()
    return output
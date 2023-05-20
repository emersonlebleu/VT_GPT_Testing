#The main file for the program
from spider import Spider
from ai import Ai
from file_io import new_soup, write_soup, read_soup_body, write_output

#One spider for each site
spider = Spider()
url = 'http://labcorp.us-mkia-0nms-03592088-in-patientswithrelapsed-or-refractory-aml.alchemer.com/s3/?snc=1684532429_6467eccdc9def4.43205362'
html = spider.get_body_html(url)

file_path = new_soup('soup.txt', 'bs_files')
output_file = 'today_output.txt'
write_soup(html, file_path)
body_html = read_soup_body(file_path)

#One ai for each site
ai = Ai()
questions = ai.get_questions(body_html)
write_output(questions, output_file)

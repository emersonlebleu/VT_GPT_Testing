#The testing logic for the file (not functional testing data driven testing for prompt success)
from spider import Spider
from ai import Ai
from file_io import new_soup, write_soup, read_soup_body, write_output, read_output

#One spider for each site
spider = Spider()
url = 'http://labcorp.us-mkia-0nms-03592088-in-patientswithrelapsed-or-refractory-aml.alchemer.com/s3/?snc=1684532429_6467eccdc9def4.43205362'
html = spider.get_body_html(url)

#prompt5 test
file_path = new_soup('soup.txt', 'bs_files')
output_file = 'today_output.txt'
write_soup(html, file_path)
body_html = read_soup_body(file_path)
ai = Ai()

iter_num = 1
success_num = 0
errors = {}
number = 20

for num in range(number):
    questions = ai.get_questions(body_html)

    try:
        gpt_response_list = eval(questions)
        print(f'Prompt success: {iter_num}')
        success_num += 1
    except Exception as e:
        print(f'Prompt failed: {iter_num}')
        print(e) 
        errors[iter_num] = [questions, 'Failed']

    if num == number-1:
        break
    iter_num += 1    

print('Success rate: ' + str((success_num/iter_num)*100)+'%')
write_output(str(errors), 'results.txt')
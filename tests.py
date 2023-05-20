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

for num in range(1):
    questions = ai.get_questions(body_html)
    write_output(questions, output_file)

    gpt_response = read_output(file_name=output_file)

    try:
        gpt_response_list = eval(gpt_response)
        print('Prompt success')
        # print(gpt_response_list)
    except Exception as e:
        print('Prompt failed')
        print(e)
        print(gpt_response)
        break
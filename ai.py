#Sends and recieves from open ai, converts data into usable format
import openai
from settings import API_KEY

class Ai:
    def __init__(self):
        pass

    def get_questions(self, text='', model='gpt-3.5-turbo'):
        if text == '':
            return 'No text was provided.'
        
        prompt1 = f'''
            Given a survey text, I would like you to identify and group together contextually connected questions. The questions should be arranged in a list of lists format. Contextual connections should be determined based on whether the questions are addressing a similar topic or theme. Here is the text from the survey: {text}. Please provide the output in the following format for example: [[Question 1, subquestion 1, subquestion 2], [Question 2, subquestion 1]].\n'''

        prompt2 = f'''Dear GPT, I'm presenting you with a survey text. Your task is to analyze the text, extract the questions and categorize them into separate lists based on their hierarchical connection. A question is considered hierarchically connected to the next ones if they are subsidiary or detail-oriented questions relating to the main question. Here is the text: {text} I would appreciate it if you could provide the output in a list of lists format, such as: [[Question 1, subsidiary question, subsidiary question], [Question 2, subsidiary question, subsidiary question]].'''

        prompt3 = f'''Dear GPT, I am going to provide you with a survey text and I need your assistance in analyzing it. Your task involves extracting the survey questions and organizing them based on their contextual and hierarchical connections. If a question is followed by related, more specific questions, group them together. The questions should be arranged into separate lists inside a larger list, representing their grouping. For example, if a primary question 'Please describe your PI:' is followed by related questions like 'Name', 'Age', 'Years of experience', they should be grouped into a single list like [Please describe your PI:, Name, Age, Years of experience]. Now, here's the survey text: {text}. Please provide the output in the list of lists format, showcasing the related groupings of questions.'''
        
        prompt4 = f'''Dear GPT, I need your help in examining the text from a survey. The task involves extracting the questions from the survey text and structuring them into a list of lists based on their hierarchical relationship. If a main question is followed by subsequent, more specific questions, please group them together under the main question in a list. Each such grouping should be a separate list within a larger encompassing list.
            Here's an example for clarity: If a survey text reads 'Please describe your PI: Name, Age, Years' and 'How many of the following patients do you see each year? MM, AML, BMT', I would like the output to be [[Please describe your PI:, Name, Age, Years], [How many of the following patients do you see each year?, MM, AML, BMT]].
            Here's the survey text I'd like you to analyze: {text}. Please present the output in the format explained above.'''

        prompt5 = f'''Dear GPT, I need you to help with processing the survey text. Your task is to extract all the questions from this text and structure them in a specific way. When a question is followed by related sub-questions, treat them as a unit. Organize these units in a list of lists. For example, the text 'Please describe your PI: Name, Age, Years. How many of the following patients do you see each year? MM, AML, BMT' should be interpreted as: [['Please describe your PI:', 'Name', 'Age', 'Years'], ['How many of the following patients do you see each year?', 'MM', 'AML', 'BMT']].
            Now, apply this method to the following survey text: {text}. Ensure that each question string is between single quotation marks as demonstrated earlier.'''

        openai.api_key = API_KEY
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI that identifies the questions or actionable text from the text within questionnaires."},
                {"role": "user", "content": prompt5}
            ]
        )

        text_response = response['choices'][0]['message']['content'].strip()
        text_response = text_response[text_response.find('['):text_response.rfind(']')+1]

        #make sure parentheses are balanced
        parentheses_open = 0
        for x in text_response:
            if x != '[':
                break
            elif x == '[':
                parentheses_open += 1

        parentheses_close = 0
        #iterate backwards through string to find closing parentheses
        for x in text_response[::-1]:
            if x != ']':
                break
            elif x == ']':
                parentheses_close += 1

        #if parentheses are not balanced, add closing parentheses
        if parentheses_open > parentheses_close:
            text_response += ']' * (parentheses_open - parentheses_close)
        elif parentheses_open < parentheses_close:
            text_response = text_response[:(parentheses_close - parentheses_open) * -1]

        return text_response
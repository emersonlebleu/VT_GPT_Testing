#Sends and recieves from open ai, converts data into usable format
import openai
from settings import API_KEY

class Ai:
    def __init__(self):
        pass

    def get_questions(self, text='', model='gpt-3.5-turbo'):
        if text == '':
            return 'No text was provided.'

        prompt5 = f'''Dear GPT, I need you to help with processing the survey text. Your task is to extract all the questions from this text and structure them in a specific way. When a question is followed by related sub-questions, treat them as a unit. Organize these units in a list of lists. For example, the text 'Please describe your PI: Name, Age, Years. How many of the following patients do you see each year? MM, AML, BMT' should be interpreted as: [['Please describe your PI:', 'Name', 'Age', 'Years'], ['How many of the following patients do you see each year?', 'MM', 'AML', 'BMT']].
            Now, apply this method to the following survey text: {text}. Ensure that each question string is between single quotation marks as demonstrated earlier.'''

        openai.api_key = API_KEY
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an AI that identifies the questions or actionable text from the text within questionnaires and returns them in a properly formatted python list."},
                    {"role": "user", "content": prompt5}
                ]
            )
        except:
            text_response = None

        text_response = response['choices'][0]['message']['content'].strip()
        text_response = text_response[text_response.find('['):text_response.rfind(']')+1]

        #try one more time if the response is empty
        if text_response == '' or text_response == None:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an AI that identifies the questions or actionable text from the text within questionnaires and returns them in a properly formatted python list."},
                        {"role": "user", "content": prompt5}
                    ]
                )
            except:
                text_response = None
            text_response = response['choices'][0]['message']['content'].strip()
            text_response = text_response[text_response.find('['):text_response.rfind(']')+1]

        text_response = standardize_text(text_response)

        return text_response

def standardize_text(text):
    #make sure parentheses are balanced in the string if not add or remove parentheses as necessary
    opens = 0
    closes = 0
    special =['[', ']', ',', ' ']
    corrected_text = ''
    watching = False
    last_location = 0
    #remove any newlines
    text = text.replace('\n', '')
    #remove any multiple spaces replace with single space
    text = ' '.join(text.split())

    for i, char in enumerate(text):
        if not watching: 
            if char == special[0]:
                corrected_text += char
                opens += 1
            else:
                corrected_text += char
                watching = True
        else:
            if char == special[0]:
                #find the last non special character and make sure the format is correct
                for j in range(len(corrected_text)-1, 0, -1):
                    if corrected_text[j] == special[1]:
                        closes -= 1
                    if corrected_text[j] not in special:
                        corrected_text = corrected_text[:j+1] + '], '
                        corrected_text += char
                        opens += 1
                        closes += 1
                        break
                #turn off watching
                watching = False
            else:
                corrected_text += char
                if char == special[1]:
                    closes += 1
    #ensure that opens matches closes if it doesnt add the appropriate number of closes
    if opens > closes:
        for i in range(opens-closes):
            corrected_text += ']'
    elif closes > opens:
        for i in range(closes-opens):
            corrected_text = corrected_text[:len(corrected_text)-1]

    return corrected_text
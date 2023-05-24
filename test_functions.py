from ai import standardize_text

#testing file
def test_standardization():
    test_string = '''[['please tell me the following', 'name', 'age', 'years', ['how many of the following patients do you see each year', 'mm', 'aml', 'bmt']]'''
    desired_result = '''[['please tell me the following', 'name', 'age', 'years'], ['how many of the following patients do you see each year', 'mm', 'aml', 'bmt']]'''
    result = standardize_text(test_string)
    assert result == desired_result, 'Standardization senario 1 failed: Missing closing bracket only'
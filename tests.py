import pytest
from model import Question

@pytest.fixture
def sample_question():
    q = Question("Which of the following is a prime number?", max_selections=1)
    q.add_choice("7", is_correct=True)
    q.add_choice("4", is_correct=False)
    q.add_choice("9", is_correct=False)
    return q

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_remove_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)
    question.remove_choice_by_id(1)
    
    assert len(question.choices) == 0

def test_remove_multiple_choices():
    question = Question(title='q1')
    
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_add_multiple_choices():
    q = Question('Sample?')
    q.add_choice('A')
    q.add_choice('B', is_correct=True)
    assert len(q.choices) == 2
    assert any(c.is_correct for c in q.choices)

def test_choice_id_increment():
    question = Question('ID check?')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    assert c2.id == c1.id + 1

def test_invalid_choice_text_empty():
    question = Question('Test empty choice text')
    with pytest.raises(Exception):
        question.add_choice('')

def test_duplicate_correct_choices_allowed():
    question = Question('Multiple correct?', max_selections=2)
    c1 = question.add_choice('A', True)
    c2 = question.add_choice('B', True)
    result = question.select_choices([c1.id, c2.id])
    assert sorted(result) == sorted([c1.id, c2.id])

def test_invalid_choice_text_too_long():
    question = Question('Test long choice text')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_set_correct_choices():
    question = Question('Set correct')
    c1 = question.add_choice('A')
    c2 = question.add_choice('B')
    question.set_correct_choices([c2.id])
    assert c2.is_correct
    assert not c1.is_correct

def test_select_correct_choices():
    question = Question('Pick the correct', max_selections=2)
    c1 = question.add_choice('Correct 1', True)
    c2 = question.add_choice('Correct 2', True)
    c3 = question.add_choice('Wrong', False)
    selected = question.select_choices([c1.id, c3.id])
    assert c1.id in selected
    assert c3.id not in selected

def test_max_selections_limit():
    question = Question('Pick one', max_selections=1)
    c1 = question.add_choice('A', True)
    c2 = question.add_choice('B', False)
    with pytest.raises(Exception):
        question.select_choices([c1.id, c2.id])

def test_fixture_selection_correct(sample_question):
    correct_ids = sample_question._correct_choice_ids()
    selected = sample_question.select_choices(correct_ids)
    assert set(selected) == set(correct_ids)

def test_fixture_limit_selection(sample_question):
    correct_ids = sample_question._correct_choice_ids()
    extra = sample_question.add_choice("21", False)
    with pytest.raises(Exception):
        sample_question.select_choices([*correct_ids, extra.id])
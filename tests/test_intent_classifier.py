import pytest
import os
from codebot import intent_classifier

def test_bayesian_intent_classifier():
    classifier = intent_classifier.bayesian_classifier_factory()

    assert classifier.classify('No dont do that') == 'Rejection'
    assert classifier.classify('yes thats right') == 'Confirmation'
    assert classifier.classify('Stop the checking process') == 'Exit'
    assert classifier.classify('ignore this error') == 'No_correction_now'
    assert classifier.classify('ignore this forever') == 'No_correction_forever'
    assert classifier.classify('I want to correct this error') == 'Correction'

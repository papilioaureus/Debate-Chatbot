import pytest
#from your_model_module import DebateModel

@pytest.fixture
def model():
    """Fixture to initialize the model before each test."""
    return DebateModel()

def test_prediction(model):
    """Test the prediction output of the model."""
    input_data = "This is a test statement for debate."
    prediction = model.predict(input_data)
    assert isinstance(prediction, str), "Prediction should be a string."
    assert len(prediction) > 0, "Prediction should not be empty."

import nltk
from nltk.tokenize import word_tokenize
import graphviz

# Sample conversation
conversation = [
    ("Person", "Hi there!"),
    ("Chatbot", "Hello! How can I help you today?"),
    ("Person", "I'd like to know about your products."),
    ("Chatbot", "Sure, we offer a variety of products. What specifically are you interested in?"),
    # More conversation lines here...
]

# Initialize NLTK
nltk.download('punkt')

# Process conversation and generate sequence diagram


def generate_sequence_diagram(conversation):
    diagram = graphviz.Digraph(format='png')
    prev_actor = None
    arrow_counter = 1
    for actor, message in conversation:
        if actor != prev_actor:
            diagram.node(actor, color="blue" if actor == "Person" else "green")
        diagram.node(message)
        if prev_actor is not None:
            diagram.edge(prev_actor, actor, label=str(arrow_counter), color="blue" if prev_actor ==
                         "Person" else "green")  # Arrow pointing from previous speaker to current speaker
            arrow_counter += 1
        diagram.edge(actor, message, label=str(arrow_counter), color="blue" if actor ==
                     "Person" else "green")  # Arrow pointing from current speaker to message
        arrow_counter += 1
        prev_actor = actor
    diagram.render('sequence_diagram')


generate_sequence_diagram(conversation)

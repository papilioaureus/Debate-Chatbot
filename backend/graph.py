from pyvis.network import Network
import csv
import os
import webbrowser

def create_interactive_graph(csv_path='interactions/interactions.csv'):
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            user_query, chatbot_response = row
            if user_query and chatbot_response:
                net.add_node(user_query, title=user_query, group=1)
                net.add_node(chatbot_response, title=chatbot_response, group=2)
                net.add_edge(user_query, chatbot_response)

    # Set options using a JSON string
    net.set_options("""
    {
      "nodes": {
        "borderWidth": 2,
        "shape": "dot",
        "font": {
          "size": 15
        }
      },
      "edges": {
        "color": {
          "inherit": true
        },
        "smooth": false
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -80000,
          "centralGravity": 0.3,
          "springLength": 95
        },
        "minVelocity": 0.75
      }
    }
    """)

    # Instead of net.show(), write the HTML to a file and then open it
    output_path = os.path.join(os.getcwd(), 'interactions_graph.html')
    net.save_graph(output_path)
    webbrowser.open('file://' + output_path)

# Example usage
create_interactive_graph()

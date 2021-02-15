from matplotlib import pyplot as plt

def bar_graph_save(labels, data, title):
    plt.title(title)
    plt.bar(labels, data, color=['purple', 'black'])
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    plt.savefig('graph.png')
    plt.clf()



def pie_chart_save(labels, data, title):
    plt.title(title)
    plt.pie(data, labels=labels, shadow=True, autopct='%1.1f%%')
    plt.axis('equal')
    plt.savefig('graph.png')
    plt.clf()

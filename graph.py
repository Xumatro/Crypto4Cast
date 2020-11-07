from matplotlib import pyplot


# Plot a basic graph of our data.
def plot_from_json(data, show_grid, filename, dpi):
    # Set "entries" to the number of data entries in the data, counting backwards.
    entries = [*range(-len(data)+1, 0), 0]
    
    values = []
    # Loop through all the data and append the average of this day to the "values" list.
    for entry in data:
        values.append(entry['average'])

    # Plot the graph and save it to a file.
    pyplot.plot(entries, values)
    pyplot.xlabel("Days")
    pyplot.ylabel("Value")
    pyplot.title("Value of coin")
    pyplot.grid(show_grid)
    pyplot.savefig(filename, dpi=dpi)

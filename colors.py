def get_key_color(gradient, key):
    return gradient[key]


# TODO make a better gradient - maybe rainbow?
def linear_gradient(start_color, end_color, n):
    """
    Returns a gradient list of n colors between RGB colors.
    """
    # Initilize a list of the output colors with the starting color
    gradient_list = [start_color]
    # Calculate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(start_color[j] + (float(t) / (n - 1)) * (end_color[j] - start_color[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        gradient_list.append(curr_vector)

    return gradient_list
import pandas as pd
import math
import plotly.graph_objects as go

def tuple_dict_to_df(dict):
    """
    Input:
        dict: dictionary with each key as a tuple (source, target)
        and each value as the corresponding value
    Output:
        dataframe with rows 'source', 'target', and 'value'
        corresponding to the first value in the key, second value in the key,
        and the actual value
    """

    source = [k[0] for k in dict.keys()]
    target = [k[1] for k in dict.keys()]
    value = [dict[k] for k in dict.keys()]

    dict2 = {'source': source, 'target': target, 'value': value}
    df = pd.DataFrame(dict2)

    return df

def has_numbers(inputString):
    """
    input: a string
    output: true if it has any numerical characters, false otherwise
    """
    return any(char.isdigit() for char in inputString)
    # returns true if value has any numbers, false if otherwise
    # helper function for checking if biographes contain any birth years

def round_down(x):
    """
    input: a numeric
    output: the input rounded down to the nearest 10
    """
    return math.floor(x / 10.0) * 10
    # helper function to round a number down to the nearest 10, will be used to round to decade

def clear_low_values(dict, n):
    """
    input: dictionary dict, an int n
    output: the same dict, but with any values below n removed
    """
    keys_to_pop = []
    for key, value in dict.items():
        if value < n:
            keys_to_pop.append(key)

    for k in keys_to_pop:
        dict.pop(k)
    # need to pop keys all at once later because popping while iterating is no good

    return dict
def create_sankey(input_df, src, targ, vals, *cols, **kwargs):
    """
    Inputs
        input_df - dict with >=2 columns of input
        src - column name of source column
        targ - column name of target column
        vals - column name of values column
        *cols - optional input, list of any other columns to be considered alongside src and targ
        **kwargs - optional input, width & height of graph
    Outputs:
        the plot, also opens it in browser
    """

    # aggregate_columns is always called on the input df
    # it has no effect if input_df only has two non-value columns (only source and target)

    column_list = [src, targ]

    if len(cols) > 0:
        column_list += [c for c in cols][0]

    column_list.append(vals)

    # this is so that aggregate_columns only runs on the columns provided in the df
    df_to_use = input_df[column_list]
    # aggregate_columns will take in the src and targ column names
    # so that the df it outputs will have similar column names to the input df
    input_df = aggregate_columns(df_to_use, src, targ, vals)

    input_dict = {}
    for index, row in input_df.iterrows():
        input_dict[(row[src], row[targ])] = row[vals]

    labels = list(set([n[0] for n in set(input_dict.keys())] + [n[1] for n in set(input_dict.keys())]))
    # creates set of labels, set cast is to ensure there are no dupes

    indices = [labels.index(l) for l in labels]
    # creates numerical indices for each label to feed sankey

    source = [indices[labels.index(l[0])] for l in input_dict.keys()]
    target = [indices[labels.index(l[1])] for l in input_dict.keys()]
    value = [input_dict[l] for l in input_dict.keys()]
    # isolates the 2 values in each key, and assigns them indices

    link = {'source': source, 'target': target, 'value': value}

    node = {'label': labels, 'pad': 5, 'thickness': 20}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    width = kwargs.get('width', 800)
    height = kwargs.get('height', 400)
    fig.update_layout(
        autosize=False,
        width=width,
        height=height)

    fig.show()
    return fig
    # creates actual sankey diagram

# test values for testing aggregate_columns found below


def aggregate_columns(df, src_name, targ_name, vals_name):
    """
    Args:
        input: input dataframe "df" with the last column being a numerical values column
            and every other column being a key
        src: string name that is the intended name of the source column
        targ: string name that is the intended name of the target column
        vals - string name that is the intended name of the values column
    output: new dataframe with a value for each pair of inputs
    """

    # list of every column name except the values column
    # next part creates list of unique values for each column other than the values column
    # so we want to exclude the values column
    col = [d for d in df.columns if d != vals_name]

    unique_values = []
    agg_values = {}
    for c in col:
        unique_values.append(list(set(df[c])))

    # unique_values ends up being a 2d list, with each inner list containing unique values in one column

    for i in range(len(unique_values) - 1):
        j = i + 1
        src = unique_values[i]
        targ = unique_values[j]
        for s in src:
            for t in targ:
                agg_values[(s, t)] = 0


    # populates the dict agg_values with keys that are each a unique pairing from 2 adjacent columns
    # with the source being the left column and the target being the right one
    # each is initialized to 0

    print(df.head().to_string())
    for index, row in df.iterrows():
        r = list(row)
        for i in range(len(r) - 2): # last column is values so we want to ignore it completely
            j = i + 1
            # i is the column index of source, j is the column index of target
            agg_values[r[i], r[j]] += r[-1]

    # in each row, for each pairing of columns
    # add the value to the value represented by the pairing in agg_values

    keys_to_delete = []
    for key, value in agg_values.items():
        if value == 0:
            keys_to_delete.append(key)

    for k in keys_to_delete:
        del agg_values[k]

    # some of the column pairings never actually show up in the data, so they are removed

    source, target = [k[0] for k in agg_values.keys()], [k[1] for k in agg_values.keys()]
    value = [agg_values[k] for k in agg_values.keys()]

    dict = {src_name: source, targ_name: target, vals_name: value}
    df2 = pd.DataFrame(dict)

    return df2

"""def main():
    l1 = ['u', 'u', 'u', 'v']
    l2 = ['x', 'y', 'y', 'x']
    l3 = ['p', 'p', 'q', 'p']
    values = 10, 20, 15, 15

    dict = {'l1': l1, 'l2': l2, 'l3': l3, 'values': values}
    df = pd.DataFrame(dict)
    create_sankey(df, 'l1', 'l2', 'values')

if __name__ == '__main__':
    main()"""



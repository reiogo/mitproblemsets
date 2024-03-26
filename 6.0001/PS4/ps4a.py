# Problem Set 4A
# Name: <Ray O>
# Collaborators:
# Time Spent: x:xx
def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    # initialize variables
    perm_list = []
    var1 = ''
    var2 = ''
    var3 = ''
    # if sequence is single char:
    if len(sequence) == 1:
        # return list of the seq
        perm_list.append(sequence)
        return perm_list 
    # else: 
    else:
        # for loop with recursive call
        for k in get_permutations(sequence[1:]):
        # append seq to list: first letter of the seq + recursive call
        # and the recursive call + first letter of the seq
            var1 = sequence[0] + k
            perm_list.append(var1)
            var2 = k + sequence[0]
            perm_list.append(var2)
            # for loop over length of sequence, inserting the first element into the seq\
            # append the str to list
            for m in range(len(k)):
                var3 = k[:m] + sequence[0] + k[m:]
                if var3 not in perm_list:
                    perm_list.append(var3)
        return perm_list

if __name__ == '__main__':
#    #EXAMPLE
    print('------------------------------------------------------------------')
    example_input1 = 'abc'
    print('Input:', example_input1)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input1))

    example_input2 = 'dmv'
    print('Input:', example_input2)
    print('Expected Output:', ['dmv', 'dvm', 'mdv', 'mvd', 'vdm', 'vmd'])
    print('Actual Output:', get_permutations(example_input2))
    

    example_input3 = 'xy'
    print('Input:', example_input3)
    print('Expected Output:', ['xy', 'yx'])
    print('Actual Output:', get_permutations(example_input3))

    example_input4 = '123'
    print('Input:', example_input4)
    print('Expected Output:', ['123', '132', '213', '231', '312', '321'])
    print('Actual Output:', get_permutations(example_input4))
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)





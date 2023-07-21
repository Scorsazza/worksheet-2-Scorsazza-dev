# The data list consists of several entries of the form:
# [score, name], where score is the value you need to sort, and name is a string
# For example, to access the score of the first element of data is data[0][0]
# And the second element of data is data[1][0]
# So this function should sort on the first element

def sort(data):
 n = len(data)

 for i in range(n - 1):
    for j in range(0, n - i - 1):
        for j in range(0, n - i - 1):
            if data[j][0] > data[j +1][0]:
                data[j], data[j + 1] = data[j+1], data[j]
 return data
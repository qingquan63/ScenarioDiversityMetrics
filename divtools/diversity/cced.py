def continuous_edit_distance(seq1, seq2):
    """
    Calculate the Continuous Edit Distance (CCED) between two sequences.
    This function uses dynamic programming to compute the distance.
    """

    # Initialize the matrix with zeros
    dp = [[0 for x in range(len(seq2) + 1)] for x in range(len(seq1) + 1)]

    # Fill in the matrix
    for i in range(len(seq1) + 1):
        for j in range(len(seq2) + 1):
            if i == 0: # first sequence is empty
                dp[i][j] = j   # j insertions
            elif j == 0: # second sequence is empty
                dp[i][j] = i   # i deletions
            elif seq1[i-1] == seq2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],   # Insert
                                   dp[i][j-1],   # Remove
                                   dp[i-1][j-1]) # Replace

    return dp[len(seq1)][len(seq2)]

# Example usage
seq1 = "gamer"
seq2 = "game"
distance = continuous_edit_distance(seq1, seq2)
print("Continuous Edit Distance:", distance)


def continuous_edit_distance(s1, s2):
    """
    Calculate the Continuous Edit Distance between two strings.

    This is a basic implementation that allows for continuous edits over sequences of characters.
    The cost of operations (insert, delete, replace) is set uniformly here, but can be modified.
    """
    # Create a matrix to store distances
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    # Initialize the first row and column of the matrix
    for i in range(len(s1) + 1):
        dp[i][0] = i
    for j in range(len(s2) + 1):
        dp[0][j] = j

    # Compute distances
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            # Check if the characters are the same
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Compute costs for different operations
                insert_cost = dp[i][j - 1] + 1
                delete_cost = dp[i - 1][j] + 1
                replace_cost = dp[i - 1][j - 1] + 1
                # Find the minimum cost
                dp[i][j] = min(insert_cost, delete_cost, replace_cost)

    # The bottom-right corner of the matrix contains the final distance
    return dp[-1][-1]

# Example usage
s1 = "kitten"
s2 = "sitting"
ced = continuous_edit_distance(s1, s2)

print(ced)

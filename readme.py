

def x_sequence(n):
  """
  Returns the 1,X sequence up to the nth step.

  Args:
    n: The number of steps.

  Returns:
    A list of the terms in the sequence.
  """

  sequence = []
  for i in range(1, n + 1):
    if i == 1:
      sequence.append("1,X")
    elif i == 2:
      sequence.append("1,1")
    else:
      previous_two_terms = sequence[-2:]
      sequence.append(previous_two_terms[0] + previous_two_terms[1])

  return sequence



sequence = x_sequence(1092)
print(sequence)
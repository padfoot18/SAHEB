def sentences_to_indices(X, word_to_index, max_len):
    """
    Converts an array of sentences (strings) into an array of indices corresponding to words in the sentences.
    The output shape should be such that it can be given to `Embedding()` (described in Figure 4). 
    
    Arguments:
    X -- array of sentences (strings), of shape (m, 1)
    word_to_index -- a dictionary containing the each word mapped to its index
    max_len -- maximum number of words in a sentence. You can assume every sentence in X is no longer than this. 
    
    Returns:
    X_indices -- array of indices corresponding to words in the sentences from X, of shape (m, max_len)
    """
    
    # Make translation table to replace puctuation
    replace_char = {key: None for key in string.punctuation}
    replace_char['"'] = None
    table = str.maketrans(replace_char)
    stop_words = set(stopwords.words('english'))
    
    
    m = X.shape[0]                                   # number of training examples
    
    # Initialize X_indices as a numpy matrix of zeros and the correct shape (≈ 1 line)
    X_indices = np.zeros(shape=(m, max_len))
    
    for i in range(m):                               # loop over training examples
        
        # Remove punctuation
        X[i] = X[i].translate(table)
        
        # Convert the ith training sentence in lower case and split is into words. You should get a list of words.
        sentence_words = X[i].lower().split()        
        
        # Initialize j to 0
        j = 0
        
        # Store indices of unknown words in list and then replace it by
        # the average of all words
        unknown_words_index = []
        
        # Loop over the words of sentence_words
        for w in sentence_words:
            # Skip Stopwords
            if w in stop_words:
              continue
            # Set the (i,j)th entry of X_indices to the index of the correct word.
            if w in word_to_index:
              X_indices[i, j] = word_to_index[w]
            else:
              # Handle unknown key (keep it as zeros)
              pass
            # Increment j to j + 1
            j += 1            
    
    return X_indices
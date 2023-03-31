import sys
import tensorflow as tf
import numpy as np
from unirep import babbler64 as babbler

def get_embedding(mutations_name):
   
    SEQ = 'MQYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE'
    AA = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    AA_dict = dict((k,v) for k,v in enumerate(AA))
    mutations = np.genfromtxt('./assets/mutation_input/'+mutations_name+'.csv', delimiter=",").astype(int)
    print(mutations)
    
    # Set seeds
    tf.set_random_seed(42)
    np.random.seed(42)

    MODEL_WEIGHT_PATH = "./64_weights"

    batch_size = 12
    b = babbler(batch_size=batch_size, model_path=MODEL_WEIGHT_PATH)
    
    avg_hidden = np.zeros((len(mutations),64))
    final_hidden = np.zeros((len(mutations),64))
    final_cell = np.zeros((len(mutations),64))
    
    for i in range(len(mutations)):
        pos1, mut1, pos2, mut2 = mutations[i]
        mutant = list(SEQ)
        mutant[pos1] = AA_dict[mut1]
        if pos2>0:
            mutant[pos2] = AA_dict[mut2]  
        mutant = ''.join(mutant)
        avg_hidden[i], final_hidden[i], final_cell[i] = b.get_rep(mutant)
        
    for arr, prefix in zip([avg_hidden, final_hidden, final_cell], ['avg_hidden_', 'final_hidden_', 'final_cell_']):
        np.savetxt('./assets/embedding_output/'+prefix+mutations_name+'.csv', arr, delimiter=",")

mutations_name = sys.argv[1].strip()
get_embedding(mutations_name)
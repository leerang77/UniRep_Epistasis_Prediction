import subprocess
from itertools import product, combinations

import numpy as np

def runner():
    SEQ = 'MQYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE'
    AA = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 
          'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    AA_dict = dict((k,v) for v,k in enumerate(AA))
    SEQ = list(map(AA_dict.get, list(SEQ)))

    # Test
    mutations = []
    for pos1 in range(1):
        for mut1 in range(4):
            if mut1!=SEQ[pos1]:
                mutations.append([pos1, mut1, -1, -1])
    mutations = np.array(mutations)

    np.savetxt("./assets/mutation_input/test.csv", mutations, delimiter=",")
    run_process("test")

    # Single mutation
    mutations = []
    for pos1 in range(1,len(SEQ)):
        for mut1 in range(len(AA)):
            if mut1!=SEQ[pos1]:
                mutations.append([pos1, mut1, -1, -1])
    mutations = np.array(mutations)
    fnm = 'single_mutations'
    np.savetxt('./assets/mutation_input/'+fnm+'.csv', mutations, delimiter=',')
    run_process(fnm)

    # Double mutation
    residues_list = combinations(list(range(1,len(SEQ))),2)
    for cnt, residues in enumerate(residues_list):
        mutations = []
        for mut1 in range(20):
            for mut2 in range(20):
                if mut1!=SEQ[residues[0]] and mut2!=SEQ[residues[1]]:
                    mutations.append([residues[0],mut1,residues[1],mut2])
        mutations = np.array(mutations)
        fnm = "double_mutations_{0:d}_{1:d}".format(residues[0],residues[1])
        np.savetxt('./assets/mutation_input/'+fnm+'.csv', mutations, delimiter=',')
        run_process(fnm)
        write_files_to_run(fnm, cnt)


def write_files_to_run(fnm, cnt):
    fnm_list = ['run_files_{0:d}'.format(i) for i in range(1,4)]
    index = cnt//495
    with open(fnm_list[index], 'a+') as f:
        f.write('sbatch ./assets/sbatch_scripts/'+fnm+'.sh \n')


def run_process(fnm):
    with open('./assets/sbatch_scripts/'+fnm+'.sh', 'w+') as f:
        partitions = ['sched_mit_arupc_long',
                    'sched_mit_arupc',
                    'sched_any',
                    'sched_mit_hill',
                    'newnodes']
        f.write('#!/bin/bash \n')
        f.write('#SBATCH --job-name='+fnm+' \n')
        f.write('#SBATCH --nodes=1 \n')
        f.write('#SBATCH --cpus-per-task=2 \n')
        f.write('#SBATCH --time=12:00:00 \n')
        f.write('#SBATCH --partition='+','.join(partitions)+' \n')
        f.write('#SBATCH --mem-per-cpu=2000 \n')
        f.write('#SBATCH -o /nobackup1c/users/leerang/UniRep/output/output_%j.txt \n')
        f.write('#SBATCH -e /nobackup1c/users/leerang/UniRep/error/error_%j.txt \n\n')
        f.write('cd /nobackup1c/users/leerang/UniRep')
        f.write('module add /home/software/modulefiles/singularity/3.7.0 \n')
        f.write('singularity exec -B /nobackup1c/users/leerang/UniRep ./UniRep.sif python3 embedding_getter.py '+fnm)
        

if __name__ == '__main__':
    runner()
    #result = subprocess.run(["python", "embedding_getter.py", "test.csv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(result.stdout)
    #print(result.stderr)
    #print(result.returncode)
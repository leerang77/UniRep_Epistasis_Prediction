## Predicting epistatic interaction for protein stability

### Summary
Protein sequence embeddings learned from large unsupervised deep learning models have been shown to capture the fundamental "language" of protein. If so, supervised learning models built on such embeddings might be able to predict epistatic interactions between residues that have not been seen during the training. Olson et al. published deep mutational scanning data of GB1 protein. The data include the folding stability changes from the wildtype by every possible single mutantion (total of 1,045 mutants) and double mutation (total of 535,917 mutants) at 55 residues of GB1. Without the a priori information transfer from the embeddings, a model that is trained directly on the 1,045 single mutations cannot possibly have any information about the epistatic interactions between the residues. Here, we test if a model trained on deep-learning embeddings of the single mutants can predict the epistatic interactions between the residues. We used the UniRep embedding by Alley et al and built a Lasso linear regression model on top. 

#### Summary of what was done
UniRep docker container was cloned from [github repository](https://github.com/churchlab/UniRep). The embedding can only be calculated one at a time, so parallel computing was necessary to calculate the embeddings of 536,962 mutants. Custom script was used to batch the mutants, calculate the embeddings, and write to output files. To run the jobs on MIT engaging cluster, Singularity image of the docker container was created and used. The stability data for GB1 mutants was obtained in an excel file from the supplementary materials of Olson et al. The data and embeddings were used to train a Lasso regression model for stability prediction.

#### To reproduce
Clone this repository. Download and unzip data from google drive [link](https://drive.google.com/file/d/1MSmOt9F-kxa4Mh3EotLL1eY7iSbSKCtY/view?usp=share_link). Launch Project.ipynb. If you want to generate the embeddings, then use the .py files in /Utils folder. More details to be added later.

#### References
1. Olson, C. Anders, Nicholas C. Wu, and Ren Sun. A comprehensive biophysical description of pairwise epistasis throughout an entire protein domain. Current biology 24.22, 2643-2651 (2014). https://doi.org/10.1016/j.cub.2014.09.072
2. Alley, E.C., Khimulya, G., Biswas, S. et al. Unified rational protein engineering with sequence-based deep representation learning. Nat Methods 16, 1315–1322 (2019). https://doi.org/10.1038/s41592-019-0598-1

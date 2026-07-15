import os

# To get the datasets ready for training, run the following script. It will divide the datasets into train-validation-test sets and produce pickled data ready for training.
Choet_Dataset = {
    'MESOS': 'Apache',
    'USERGRID': 'Apache',
    'TISTUD': 'Appcelerator',
    'APSTUD': 'Appcelerator',
    'TIMOB': 'Appcelerator',
    'BAM': 'Atlassian',
    'CLOV': 'Atlassian',
    'JRESERVER': 'Atlassian',
    'DURACLOUD': 'Duraspace',
    'DM': 'Lsstcorp',
    'MDL': 'Moodle',
    'MULE': 'Mulesoft',
    'MULESTUDIO': 'Mulesoft',
    'XD': 'Spring'
}

Porru_Dataset = {
    'MESOS': 'Apache',
    'TISTUD': 'Appcelerator',
    'APSTUD': 'Appcelerator',
    'TIMOB': 'Appcelerator',
    'DNN': 'DNNSoftware',
    'MULE': 'Mulesoft',
    'NEXUS': 'Sonatype',
    'XD': 'Spring'
}

Tawosi_Dataset = {
    'MESOS': 'Apache',
    'ALOY': 'Apache',
    'TISTUD': 'Appcelerator',
    'APSTUD': 'Appcelerator',
    'CLI': 'Appcelerator',
    'DAEMON': 'Appcelerator',
    'TIDOC': 'Appcelerator',
    'TIMOB': 'Appcelerator',
    'CLOV': 'Atlassian',
    'CONFCLOUD': 'Atlassian',
    'CONFSERVER': 'Atlassian',
    'DNN': 'DNNSoftware',
    'DURACLOUD': 'Duraspace',
    'FAB': 'Hyperledger',
    'STL': 'Hyperledger',
    'DM': 'Lsstcorp',
    'COMPASS': 'MongoDB',
    'SERVER': 'MongoDB',
    'EVG': 'MongoDB',
    'MDL': 'Moodle',
    'MULE': 'Mulesoft',
    'NEXUS': 'Sonatype',
    'XD': 'Spring'
}

# List of the pretrained datasets. We will use them to pre-train Deep-SE before training it for story point estimation.
dataPres = [
    'Apache',
    'Appcelerator',
    'Duraspace',
    'Atlassian',
    'Moodle',
    'Lsstcorp',
    'Mulesoft',
    'Spring',
    'DNNSoftware',
    'Hyperledger',
    'MongoDB',
    'Sonatype'
]


# To choose with the dataset to use 
datasetDict_ = 'Porru_Dataset'  # 'Choet_Dataset' | 'Tawosi_Dataset' | 'Porru_Dataset' | 'Pretrain_Dataset'
data_path = '../../datasets/' + datasetDict_ + '/'


# if datasetDict_ = 'Pretrain_Dataset' --> Meaning we will use the datasets for pre-training Deep-SE.
#                                          Before we will train the model for story point estimation, 
#                                          we will pre-train it using the datasets in dataPres list.
if datasetDict_ == 'Pretrain_Dataset':
    # Preprocess pre-train data: load, divide, and build dictionary and produce pickled data ready for pre-training
    for dataPre in dataPres:
        cmd = 'python preprocess_pretrain.py -path ' + data_path + ' -repo ' + dataPre
        print(cmd)
        os.system(cmd)
else: # After we pre-train Deep-SE, we will train it for story point estimation using the datasets in datasetDict_.
    if datasetDict_ == 'Choet_Dataset':
        datasetDict = Choet_Dataset
    elif datasetDict_ == 'Tawosi_Dataset':
        datasetDict = Tawosi_Dataset
    elif datasetDict_ == 'Porru_Dataset':
        datasetDict = Porru_Dataset

    #  Divide the datasets to train-validation-test sets. It produces text files in which each bug is labelled with
    #  one of the three sets. This file is used by preprocess_storypoint.py to split the datasets.
    for project, repo in datasetDict.items():

        # Provide an instruction, teh instruction bellow has a meanimg:
        # "Hai Python, jalankan file preprocess_storypoint.py. Dataset yang akan diproses ada di folder ../../datasets/datasetDict/.(Variabel data_path) "
        # "Gunakan dataset [varaiabel project]_deep-se.csv."
        cmd = 'python divide_data_sortdate.py -path ' + data_path + ' -project ' + project + '_deep-se'

        # Process the instruction in the cmd variable
        os.system(cmd) # The output: 
        # os.system(r"C:\Users\Anya\OneDrive\Documents\GitHub\AgileEffortEstimation-baselien-model-\Deep-SE\data\divide_data_sortdate.py")

        # The 'divide_data_sortdate.py' will:
        # Ex
        # input: MESOS_deep-se.csv.
        #        | issuekey | title       | description        | storypoint |
        #        | -------- | ----------- | ------------------ | ---------: |
        #        | MESOS-1  | Fix login   | Cannot login       |          3 |
        #        | MESOS-2  | Improve UI  | Dashboard redesign |          5 |
        #        | MESOS-3  | Memory leak | Heap increases     |          8 |
        #        | MESOS-4  | Add API     | REST API           |          2 |
        #        | MESOS-5  | Update docs | Documentation      |          1 |

        # output: files/MESOS_3sets.txt, which contains the train-validation-test sets for each bug in the dataset.
        #         
        #         train valid test
        #           1     0     0
        #           1     0     0
        #           1     0     0
        #           0     1     0
        #           0     0     1

    # Bellow has the same logic as the loop above, but for processing the text data into numeric data
    for project, repo in datasetDict.items():
        
        # The instruction
        cmd = 'python preprocess_storypoint.py -path ' + data_path + ' -project ' + project + '_deep-se -repo ' + repo

        # Excecute the instruction in the cmd variable
        os.system(cmd)
        # os.system(r"C:\Users\Anya\OneDrive\Documents\GitHub\AgileEffortEstimation-baselien-model-\Deep-SE\data\preprocess_storypoint.py")
        # The 'preprocess_storypoint.py' will:
        # Ex
        # input: MESOS_deep-se.csv.
        #        | issuekey | title       | description        | storypoint |
        #        | -------- | ----------- | ------------------ | ---------: |
        #        | MESOS-1  | Fix login   | Cannot login       |          3 |
        #        | MESOS-2  | Improve UI  | Dashboard redesign |          5 |
        #        | MESOS-3  | Memory leak | Heap increases     |          8 |
        #        | MESOS-4  | Add API     | REST API           |          2 |

        #        files/MESOS_3sets.txt, which contains the train-validation-test sets for each bug in the dataset.
        #         
        #         train valid test
        #           1     0     0
        #           1     0     0
        #           0     0     1
        #           0     1     0
        #           0     0     1

        # Output:

        # Train dataset:
        # train_t = [ [1,2,3], [4,5] ]  --> [1, 2, 3] = Fix login, [4,5] = Improve UI 
        # train_d = [ [8,9,2], [20,10]] --> [8,9,2] = Cannot login, [20, 10]   Dashboard redesign
        # train_labels = [3,5]

        # Validation dataset:
        # valid_t = [ [6,7] ]
        # valid_d = [[40,50,60]]
        # valid_labels = [8]

        # test dataset:
        # test_t = [ [70,80] ]
        # test_d = [[90,100]]
        # test_labels = [2]






# The Pipeline:                        

# run_script.py
#       │
#       ▼
# divide_data_sortdate.py
#       │
#       ▼
# preprocess_storypoint.py _
#                           │
#                           ├──────────────► load_raw_text.py
#                           │               (loads the dataset)
#                           │
#                           └──────────────► preprocess.py
#                                           (processes the text)
#       │
#       ▼
# Produces .pkl.gz

This is the CRFSuite implementation of Jeehyun Kim, Sonia Sen, Joanna Zhang team for Natural Language Processing Assignment 4.

To run:
```
$ chmod +x install.sh 
$ chmod +x evalit.sh
$ chmod +x run.sh

$ ./install.sh
$ ./run.sh
```

1. The install.sh script installs CRFSuite created by Naoaki Okazaki and the ark-tweet NLP POS tagger.

2. The run.sh script the runs the POS tagger on the training and unlabeled data, cleans the data for processing and then calls the evalit.sh script

3. The evalit.sh script (called by run.sh) starts the feature extraction procedure, trains a model usign CRFSuite using the features that have been extracted, uses CRFSuite to tag the unlabeled data, then outputs the data in a format readily available for submission to Kaggle.


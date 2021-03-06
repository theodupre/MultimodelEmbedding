# Automatic transcription using embedding latent space

This work adresses the problem of automatic transcription of musical audio pieces to midi sheets. We propose a method
based on recent research by Dorfer et al. [[Link]](https://github.com/GuiMarion/MultimodelEmbedding/blob/master/Papers/Article_Dorfer.pdf) that learns joint embedding spaces for short excerpts of musical audio and
their respective counterparts in midi scores, using multimodal convolutional neural networks. The dataset is based on Pianomidi.de, a midi sheet collection of classical music played on piano and splitted by Poliner and Ellis [2006] comprising 314
midi scores from 25 composers.

## Report

The report associated with this project can be found [here]

## How to use

### Dependecies

```shell
pip3 install numpy
pip3 install torch torchvision
pip3 install pypianoroll
pip3 install midi2audio
pip3 install pyFluidSynth
pip3 install librosa
pip3 install tqdm


```

### Usage

#### Running Train.py

This program trains our neural network model on data. 


```shell

Usage: Train.py [options]

  -h, —help            show this help message and exit
  -e EPOCHS, —epochs=EPOCHS
                        Number of Epochs
  -g GPU, —gpu=GPU     ID of the GPU, run in CPU by default.
  -o OUTPATH, —outPath=OUTPATH
                        Path for the temporary folder.
  -l LEARNING_RATE, —learning_rate=LEARNING_RATE
                        Value of the starting learning rate
```

#### Running EvalModel.py

This program runs a series of test that can be found in our report (see Report section).


EvalModel
```shell

Usage: EvalModel.py [options]

  -h, —help            show this help message and exit
  -t TESTFOLDER, —testFolder=TESTFOLDER
                        Path for the folder containing the songs to detect, by
                        default it’s DataBaseForTest/
  -o OUTPATH, —outPath=OUTPATH
                        Path for the temporary folder.
  -g GPU, —gpu=GPU     ID of the GPU, run in CPU by default.
```



## Authors

* **Guilhem Marion** 
* **Valérian Fraisse** 
* **Clément Le Moine Veillon**
* **Félix Rohrlich**
* **Gabriel Dias Neto**


## License

This project is open source.

## Acknowledgments

We would like to thank Mathieu Prang, PhD student at IRCAM and Philippe Esling, associate professor at IRCAM and Sorbonne Université, for their help and support during this project.
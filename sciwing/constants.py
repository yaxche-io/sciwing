import os
import pathlib

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_UP_DIR = os.path.dirname(os.path.dirname(__file__))
HOME_DIR = pathlib.Path("~").expanduser()


PATHS = dict(
    DATA_DIR=os.path.join(HOME_DIR, ".sciwing.data_cache"),
    MODELS_CACHE_DIR=os.path.join(HOME_DIR, ".sciwing.model_cache"),
    AWS_CRED_DIR=os.path.join(HOME_DIR, ".sciwing.aws"),
    OUTPUT_DIR=os.path.join(HOME_DIR, ".sciwing.output_cache"),
    CONFIGS_DIR=os.path.join(ROOT_DIR, "config"),
    REPORTS_DIR=os.path.join(HOME_DIR, ".sciwing.reports_cache"),
    TESTS_DIR=os.path.join(ROOT_UP_DIR, "tests"),
    TEMPLATES_DIR=os.path.join(ROOT_DIR, "_templates"),
    DATASETS_DIR=os.path.join(ROOT_DIR, "datasets"),
    EMBEDDING_CACHE_DIR=os.path.join(HOME_DIR, ".sciwing.embedding_cache"),
)


FILES = dict(
    SECT_LABEL_FILE=os.path.join(PATHS["DATA_DIR"], "sectLabel.train.data"),
    GENERIC_SECTION_TRAIN_FILE=os.path.join(
        PATHS["DATA_DIR"], "genericSect.train.data"
    ),
    PARSCIT_TRAIN_FILE=os.path.join(PATHS["DATA_DIR"], "parsCit.train.data"),
    CORA_FILE=os.path.join(PATHS["DATA_DIR"], "cora.data"),
    SCIENCE_IE_TRAIN_FOLDER=os.path.join(PATHS["DATA_DIR"], "scienceie_train"),
    SCIENCE_IE_DEV_FOLDER=os.path.join(PATHS["DATA_DIR"], "scienceie_dev"),
    ELMO_OPTIONS_FILE=os.path.join(
        PATHS["EMBEDDING_CACHE_DIR"], "elmo_2x4096_512_2048cnn_2xhighway_options.json"
    ),
    ELMO_WEIGHTS_FILE=os.path.join(
        PATHS["EMBEDDING_CACHE_DIR"], "elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"
    ),
)


DATA_FILE_URLS = dict(
    SECT_LABEL_FILE="https://sciwing.s3.amazonaws.com/sectLabel.train.data",
    GENERIC_SECTION_TRAIN_FILE="https://sciwing.s3.amazonaws.com/genericSect.train.data",
    PARSCIT_TRAIN_FILE="https://sciwing.s3.amazonaws.com/parsCit.train.data",
    SCIENCE_IE_TRAIN_FOLDER="https://sciwing.s3.amazonaws.com/scienceie_dev.zip",
    SCIENCE_IE_DEV_FOLDER="https://sciwing.s3.amazonaws.com/scienceie_train.zip",
    CORA_FILE="https://sciwing.s3.amazonaws.com/cora.data",
    TRAIN_SCIENCE_IE_CONLL_FILE="https://sciwing.s3.amazonaws.com/train_science_ie_conll.txt",
    DEV_SCIENCE_IE_CONLL_FILE="https://sciwing.s3.amazonaws.com/dev_science_ie_conll.txt",
)


EMBEDDING_FILE_URLS = dict(
    PARSCIT_EMBEDDINGS="https://sciwing.s3.amazonaws.com/vectors_with_unk.tar.gz",
    ELMO_OPTIONS_FILE="https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/"
    "2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_options.json",
    ELMO_WEIGHTS_FILE="https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/"
    "2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5",
    GLOVE_FILE="http://nlp.stanford.edu/data/glove.6B.zip",
    SCIBERT_SCIVOCAB_UNCASED="https://s3-us-west-2.amazonaws.com/ai2-s2-research/scibert/pytorch_models/scibert_scivocab_uncased.tar",
    SCIBERT_SCIVOCAB_CASED="https://s3-us-west-2.amazonaws.com/ai2-s2-research/scibert/pytorch_models/scibert_scivocab_cased.tar",
    SCIBERT_BASEVOCAB_UNCASED="https://s3-us-west-2.amazonaws.com/ai2-s2-research/scibert/pytorch_models/scibert_basevocab_uncased.tar",
    SCIBERT_BASEVOCAB_CASED="https://s3-us-west-2.amazonaws.com/ai2-s2-research/scibert/pytorch_models/scibert_basevocab_cased.tar",
)

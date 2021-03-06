import pytest
from sciwing.modules.lstm2seqencoder import Lstm2SeqEncoder
from sciwing.modules.embedders.vanilla_embedder import VanillaEmbedder
import torch
import torch.nn as nn
import numpy as np
import itertools

is_additional_embedding = [True, False]
lstm2encoder_options = itertools.product([True, False], ["sum", "concat"], [1, 2])
lstm2encoder_options = list(lstm2encoder_options)


@pytest.fixture(params=lstm2encoder_options)
def setup_lstm2seqencoder(request):
    EMBEDDING_DIM = 100
    VOCAB_SIZE = 1000
    BATCH_SIZE = 2
    HIDDEN_DIM = 1024
    NUM_TIME_STEPS = 10
    BIDIRECTIONAL = request.param[0]
    COMBINE_STRATEGY = request.param[1]
    NUM_LAYERS = request.param[2]
    EMBEDDING = nn.Embedding.from_pretrained(torch.zeros([VOCAB_SIZE, EMBEDDING_DIM]))
    tokens = np.random.randint(0, VOCAB_SIZE - 1, size=(BATCH_SIZE, NUM_TIME_STEPS))
    tokens = torch.LongTensor(tokens)

    embedder = VanillaEmbedder(embedding=EMBEDDING, embedding_dim=EMBEDDING_DIM)

    encoder = Lstm2SeqEncoder(
        emb_dim=EMBEDDING_DIM,
        embedder=embedder,
        dropout_value=0.0,
        hidden_dim=HIDDEN_DIM,
        bidirectional=BIDIRECTIONAL,
        combine_strategy=COMBINE_STRATEGY,
        rnn_bias=False,
        num_layers=NUM_LAYERS,
    )

    return (
        encoder,
        {
            "EMBEDDING_DIM": EMBEDDING_DIM,
            "VOCAB_SIZE": VOCAB_SIZE,
            "BATCH_SIZE": BATCH_SIZE,
            "HIDDEN_DIM": HIDDEN_DIM,
            "COMBINE_STRATEGY": COMBINE_STRATEGY,
            "BIDIRECTIONAL": BIDIRECTIONAL,
            "tokens": tokens,
            "EXPECTED_HIDDEN_DIM": 2 * HIDDEN_DIM
            if COMBINE_STRATEGY == "concat" and BIDIRECTIONAL
            else HIDDEN_DIM,
            "TIME_STEPS": NUM_TIME_STEPS,
            "NUM_LAYERS": NUM_LAYERS,
        },
    )


class TestLstm2SeqEncoder:
    def test_hidden_dim(self, setup_lstm2seqencoder):
        encoder, options = setup_lstm2seqencoder
        tokens = options["tokens"]
        batch_size = options["BATCH_SIZE"]
        num_time_steps = options["TIME_STEPS"]
        expected_hidden_size = options["EXPECTED_HIDDEN_DIM"]
        encoding = encoder({"tokens": tokens})
        assert encoding.size() == (batch_size, num_time_steps, expected_hidden_size)

    def test_encoder_produces_zero_encoding(self, setup_lstm2seqencoder):
        encoder, options = setup_lstm2seqencoder
        tokens = options["tokens"]
        batch_size = options["BATCH_SIZE"]
        num_time_steps = options["TIME_STEPS"]
        expected_hidden_size = options["EXPECTED_HIDDEN_DIM"]
        encoding = encoder({"tokens": tokens})
        assert torch.all(
            torch.eq(
                encoding, torch.zeros(batch_size, num_time_steps, expected_hidden_size)
            )
        )

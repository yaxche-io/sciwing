import pytest
import torch
from sciwing.metrics.precision_recall_fmeasure import PrecisionRecallFMeasure
from sciwing.utils.class_nursery import ClassNursery


@pytest.fixture
def setup_data_basecase():
    predicted_probs = torch.FloatTensor([[0.1, 0.9], [0.7, 0.3]])
    labels = torch.LongTensor([1, 0]).view(-1, 1)
    idx2labelname_mapping = {0: "good class", 1: "bad class"}

    expected_precision = {0: 1.0, 1: 1.0}
    expected_recall = {0: 1.0, 1: 1.0}
    expected_fmeasure = {0: 1.0, 1: 1.0}
    expected_macro_precision = 1.0
    expected_macro_recall = 1.0
    expected_macro_fscore = 1.0
    expected_num_tps = {0: 1.0, 1: 1.0}
    expected_num_fps = {0: 0.0, 1: 0.0}
    expected_num_fns = {0: 0.0, 1: 0.0}
    expected_micro_precision = 1.0
    expected_micro_recall = 1.0
    expected_micro_fscore = 1.0

    accuracy = PrecisionRecallFMeasure(idx2labelname_mapping=idx2labelname_mapping)
    return (
        predicted_probs,
        labels,
        accuracy,
        {
            "expected_precision": expected_precision,
            "expected_recall": expected_recall,
            "expected_fscore": expected_fmeasure,
            "expected_macro_precision": expected_macro_precision,
            "expected_macro_recall": expected_macro_recall,
            "expected_macro_fscore": expected_macro_fscore,
            "expected_num_tps": expected_num_tps,
            "expected_num_fps": expected_num_fps,
            "expected_num_fns": expected_num_fns,
            "expected_micro_precision": expected_micro_precision,
            "expected_micro_recall": expected_micro_recall,
            "expected_micro_fscore": expected_micro_fscore,
        },
    )


@pytest.fixture
def setup_data_one_true_class_missing():
    """
    The batch of instances during training might not have all
    true classes. What happens in that case??
    The test case here captures the situation
    :return:
    """
    predicted_probs = torch.FloatTensor([[0.8, 0.1, 0.2], [0.2, 0.5, 0.3]])
    idx2labelname_mapping = {0: "good class", 1: "bad class", 2: "average_class"}
    labels = torch.LongTensor([0, 2]).view(-1, 1)

    expected_precision = {0: 1.0, 1: 0.0, 2: 0.0}
    expected_recall = {0: 1.0, 1: 0.0, 2: 0.0}
    expected_fscore = {0: 1.0, 1: 0.0, 2: 0.0}

    accuracy = PrecisionRecallFMeasure(idx2labelname_mapping=idx2labelname_mapping)

    return (
        predicted_probs,
        labels,
        accuracy,
        {
            "expected_precision": expected_precision,
            "expected_recall": expected_recall,
            "expected_fscore": expected_fscore,
        },
    )


@pytest.fixture
def setup_data_to_test_length():
    predicted_probs = torch.FloatTensor([[0.1, 0.8, 0.2], [0.2, 0.3, 0.5]])
    labels = torch.LongTensor([0, 2]).view(-1, 1)
    idx2labelname_mapping = {0: "good class", 1: "bad class", 2: "average_class"}

    accuracy = PrecisionRecallFMeasure(idx2labelname_mapping=idx2labelname_mapping)

    expected_length = 3

    return predicted_probs, labels, accuracy, expected_length


@pytest.fixture
def setup_data_for_all_zeros():
    predicted_probs = torch.FloatTensor([[0.9, 0.1], [0.3, 0.7]])
    labels = torch.LongTensor([1, 0]).view(-1, 1)
    idx2labelname_mapping = {0: "good class", 1: "bad class"}

    expected_precision = {0: 0.0, 1: 0.0}
    expected_recall = {0: 0.0, 1: 0.0}
    expected_fmeasure = {0: 0.0, 1: 0.0}
    expected_macro_precision = 0.0
    expected_macro_recall = 0.0
    expected_macro_fscore = 0.0
    expected_num_tps = {0: 0.0, 1: 0.0}
    expected_num_fps = {0: 1.0, 1: 1.0}
    expected_num_fns = {0: 1.0, 1: 1.0}
    expected_micro_precision = 0.0
    expected_micro_recall = 0.0
    expected_micro_fscore = 0.0

    accuracy = PrecisionRecallFMeasure(idx2labelname_mapping=idx2labelname_mapping)
    return (
        predicted_probs,
        labels,
        accuracy,
        {
            "expected_precision": expected_precision,
            "expected_recall": expected_recall,
            "expected_fscore": expected_fmeasure,
            "expected_macro_precision": expected_macro_precision,
            "expected_macro_recall": expected_macro_recall,
            "expected_macro_fscore": expected_macro_fscore,
            "expected_num_tps": expected_num_tps,
            "expected_num_fps": expected_num_fps,
            "expected_num_fns": expected_num_fns,
            "expected_micro_precision": expected_micro_precision,
            "expected_micro_recall": expected_micro_recall,
            "expected_micro_fscore": expected_micro_fscore,
        },
    )


class TestAccuracy:
    def test_print_confusion_matrix_works(self, setup_data_basecase):
        predicted_probs, labels, accuracy, expected = setup_data_basecase
        labels_mask = torch.zeros_like(predicted_probs).type(torch.ByteTensor)
        accuracy.print_confusion_metrics(
            predicted_probs=predicted_probs, labels=labels, labels_mask=labels_mask
        )

    def test_accuracy_basecase(self, setup_data_basecase):
        predicted_probs, labels, accuracy, expected = setup_data_basecase
        expected_precision = expected["expected_precision"]
        expected_recall = expected["expected_recall"]
        expected_fmeasure = expected["expected_fscore"]

        label_mask = torch.zeros_like(labels).type(torch.ByteTensor)
        iter_dict = {"label": labels, "label_mask": label_mask}
        forward_dict = {"normalized_probs": predicted_probs}
        accuracy.calc_metric(iter_dict=iter_dict, model_forward_dict=forward_dict)
        accuracy_metrics = accuracy.get_metric()

        precision = accuracy_metrics["precision"]
        recall = accuracy_metrics["recall"]
        fscore = accuracy_metrics["fscore"]

        for class_label, precision_value in precision.items():
            assert precision_value == expected_precision[class_label]

        for class_label, recall_value in recall.items():
            assert recall_value == expected_recall[class_label]

        for class_label, fscore_value in fscore.items():
            assert fscore_value == expected_fmeasure[class_label]

    def test_accuracy_one_true_class_missing(self, setup_data_one_true_class_missing):
        predicted_probs, labels, accuracy, expected = setup_data_one_true_class_missing
        expected_precision = expected["expected_precision"]
        expected_recall = expected["expected_recall"]
        expected_fscore = expected["expected_fscore"]

        label_mask = torch.zeros_like(predicted_probs).type(torch.ByteTensor)
        iter_dict = {"label": labels, "label_mask": label_mask}
        forward_dict = {"normalized_probs": predicted_probs}
        accuracy.calc_metric(iter_dict=iter_dict, model_forward_dict=forward_dict)
        accuracy_metrics = accuracy.get_metric()

        precision = accuracy_metrics["precision"]
        recall = accuracy_metrics["recall"]
        fscore = accuracy_metrics["fscore"]

        for class_label, precision_value in precision.items():
            assert precision_value == expected_precision[class_label]

        for class_label, recall_value in recall.items():
            assert recall_value == expected_recall[class_label]

        for class_label, fscore_value in fscore.items():
            assert fscore_value == expected_fscore[class_label]

    def test_macro_scores_basecase(self, setup_data_basecase):
        predicted_probs, labels, accuracy, expected = setup_data_basecase
        expected_macro_precision = expected["expected_macro_precision"]
        expected_macro_recall = expected["expected_macro_recall"]
        expected_macro_fscore = expected["expected_macro_fscore"]
        expected_num_tps = expected["expected_num_tps"]
        expected_num_fps = expected["expected_num_fps"]
        expected_num_fns = expected["expected_num_fns"]
        expected_micro_precision = expected["expected_micro_precision"]
        expected_micro_recall = expected["expected_micro_recall"]
        expected_micro_fscore = expected["expected_micro_fscore"]

        label_mask = torch.zeros_like(predicted_probs).type(torch.ByteTensor)
        iter_dict = {"label": labels, "label_mask": label_mask}
        forward_dict = {"normalized_probs": predicted_probs}
        accuracy.calc_metric(iter_dict=iter_dict, model_forward_dict=forward_dict)
        metrics = accuracy.get_metric()

        macro_precision = metrics["macro_precision"]
        macro_recall = metrics["macro_recall"]
        macro_fscore = metrics["macro_fscore"]
        num_tps = metrics["num_tp"]
        num_fps = metrics["num_fp"]
        num_fn = metrics["num_fn"]
        micro_precision = metrics["micro_precision"]
        micro_recall = metrics["micro_recall"]
        micro_fscore = metrics["micro_fscore"]

        assert macro_precision == expected_macro_precision
        assert macro_recall == expected_macro_recall
        assert macro_fscore == expected_macro_fscore
        assert num_tps == expected_num_tps
        assert num_fps == expected_num_fps
        assert num_fn == expected_num_fns
        assert micro_precision == expected_micro_precision
        assert micro_recall == expected_micro_recall
        assert micro_fscore == expected_micro_fscore

    def test_accuracy_all_zeros(self, setup_data_for_all_zeros):
        predicted_probs, labels, accuracy, expected = setup_data_for_all_zeros
        expected_precision = expected["expected_precision"]
        expected_recall = expected["expected_recall"]
        expected_fmeasure = expected["expected_fscore"]

        label_mask = torch.zeros_like(predicted_probs).type(torch.ByteTensor)
        iter_dict = {"label": labels, "label_mask": label_mask}
        forward_dict = {"normalized_probs": predicted_probs}
        accuracy.calc_metric(iter_dict=iter_dict, model_forward_dict=forward_dict)
        accuracy_metrics = accuracy.get_metric()

        precision = accuracy_metrics["precision"]
        recall = accuracy_metrics["recall"]
        fscore = accuracy_metrics["fscore"]

        for class_, precision_value in precision.items():
            assert precision_value == expected_precision[class_]

        for class_, recall_value in recall.items():
            assert recall_value == expected_recall[class_]

        for class_, fscore_value in fscore.items():
            assert fscore_value == expected_fmeasure[class_]

    def test_macro_scores_all_zeros(self, setup_data_for_all_zeros):
        predicted_probs, labels, accuracy, expected = setup_data_for_all_zeros
        expected_macro_precision = expected["expected_macro_precision"]
        expected_macro_recall = expected["expected_macro_recall"]
        expected_macro_fscore = expected["expected_macro_fscore"]
        expected_micro_precision = expected["expected_micro_precision"]
        expected_micro_recall = expected["expected_micro_recall"]
        expected_micro_fscore = expected["expected_micro_fscore"]
        expected_num_tps = expected["expected_num_tps"]
        expected_num_fps = expected["expected_num_fps"]
        expected_num_fns = expected["expected_num_fns"]

        label_mask = torch.zeros_like(predicted_probs).type(torch.ByteTensor)
        iter_dict = {"label": labels, "label_mask": label_mask}
        forward_dict = {"normalized_probs": predicted_probs}
        accuracy.calc_metric(iter_dict=iter_dict, model_forward_dict=forward_dict)
        accuracy_metrics = accuracy.get_metric()

        macro_precision = accuracy_metrics["macro_precision"]
        macro_recall = accuracy_metrics["macro_recall"]
        macro_fscore = accuracy_metrics["macro_fscore"]
        micro_precision = accuracy_metrics["micro_precision"]
        micro_recall = accuracy_metrics["micro_recall"]
        micro_fscore = accuracy_metrics["micro_fscore"]
        num_tps = accuracy_metrics["num_tp"]
        num_fp = accuracy_metrics["num_fp"]
        num_fn = accuracy_metrics["num_fn"]

        assert macro_precision == expected_macro_precision
        assert macro_recall == expected_macro_recall
        assert macro_fscore == expected_macro_fscore
        assert micro_precision == expected_micro_precision
        assert micro_recall == expected_micro_recall
        assert micro_fscore == expected_micro_fscore
        assert num_tps == expected_num_tps
        assert num_fp == expected_num_fps
        assert num_fn == expected_num_fns

    def test_precision_recall_fmeasure_in_class_nursery(self):
        assert ClassNursery.class_nursery.get("PrecisionRecallFMeasure") is not None

import joblib
import logging


class Score:
    """
    Class to hold metrics for binary classification, including true positives (TP), false positives (FP),
    true negatives (TN), and false negatives (FN).
    """

    def __init__(self, TP=0, FP=0, TN=0, FN=0):
        self.TP = TP  # True Positives
        self.FP = FP  # False Positives
        self.TN = TN  # True Negatives
        self.FN = FN  # False Negatives


class DockerModel:
    """
    Class for loading and predicting using a pre-trained model, handling feedback to update metrics,
    and providing those metrics.
    """
    result = {}  # Dictionary to store input data

    def __init__(self, model_name="models/binary-lr.joblib"):
        """
        Initialize DockerModel with metrics and model name.
        :param model_name: Path to the pre-trained model.
        """
        self.scores = Score(0, 0, 0, 0)
        self.loaded = False
        self.model_name = model_name

    def load(self):
        """
        Load the model from the provided path.
        """
        self.model = joblib.load(self.model_name)
        logging.info(f"Model {self.model_name} Loaded")

    def predict(self, X, features_names=None, meta=None):
        """
        Predict the target using the loaded model.
        :param X: Features for prediction.
        :param features_names: Names of the features, optional.
        :param meta: Additional metadata, optional.
        :return: Predicted target values.
        """
        self.result['shape_input_data'] = str(X.shape)
        logging.info(f"Received request: {X}")
        if not self.loaded:
            self.load()
            self.loaded = True
        predictions = self.model.predict(X)
        return predictions

    def send_feedback(self, features, feature_names, reward, truth, routing=""):
        """
        Provide feedback on predictions and update the metrics.
        :param features: Features used for prediction.
        :param feature_names: Names of the features.
        :param reward: Reward signal, not used in this context.
        :param truth: Ground truth target values.
        :param routing: Routing information, optional.
        :return: Empty list as return value is not used.
        """
        predicted = self.predict(features)
        logging.info(f"Predicted: {predicted[0]}, Truth: {truth[0]}")
        if int(truth[0]) == 1:
            if int(predicted[0]) == int(truth[0]):
                self.scores.TP += 1
            else:
                self.scores.FN += 1
        else:
            if int(predicted[0]) == int(truth[0]):
                self.scores.TN += 1
            else:
                self.scores.FP += 1
        return []  # Ignore return statement as its not used

    def calculate_metrics(self):
        """
        Calculate the accuracy, precision, recall, and F1-score.
        :return: accuracy, precision, recall, f1_score
        """
        total_samples = self.scores.TP + self.scores.TN + self.scores.FP + self.scores.FN

        # Check if there are any samples to avoid division by zero
        if total_samples == 0:
            logging.warning("No samples available to calculate metrics.")
            return 0, 0, 0, 0  # Return zeros for all metrics if no samples

        accuracy = (self.scores.TP + self.scores.TN) / total_samples

        # Check if there are any positive predictions to calculate precision
        positive_predictions = self.scores.TP + self.scores.FP
        precision = self.scores.TP / positive_predictions if positive_predictions != 0 else 0

        # Check if there are any actual positives to calculate recall
        actual_positives = self.scores.TP + self.scores.FN
        recall = self.scores.TP / actual_positives if actual_positives != 0 else 0

        # Check if precision and recall are non-zero to calculate F1-score
        if precision + recall == 0:
            f1_score = 0
        else:
            f1_score = 2 * (precision * recall) / (precision + recall)

        # Return the calculated metrics
        return accuracy, precision, recall, f1_score

    def metrics(self):
        """
        Generate metrics for monitoring.
        :return: List of dictionaries containing accuracy, precision, recall, and f1_score.
        """
        accuracy, precision, recall, f1_score = self.calculate_metrics()
        return [
            {"type": "GAUGE", "key": "accuracy", "value": accuracy},
            {"type": "GAUGE", "key": "precision", "value": precision},
            {"type": "GAUGE", "key": "recall", "value": recall},
            {"type": "GAUGE", "key": "f1_score", "value": f1_score},
        ]

    def tags(self):
        """
        Retrieve metadata when generating predictions
        :return: Dictionary the intermediate information
        """
        return self.result

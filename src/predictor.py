from property import PropertyDetails, numeric_features, PropertyInput
import numpy
import math

class PriceEstimator:
    def __init__(self, entries: list[PropertyDetails]):
        self.theta = None
        self.intercept = None
        self.coefficients = None

        all_types = sorted({e.property_type for e in entries if e.property_type})
        type_categories = all_types[1:]  # drop_first -> baseline = all_types[0]
        self.baseline_type = all_types[0] if all_types else None

        # store the full column layout so prediction can reproduce it later
        self.feature_names = numeric_features() + [f"type_{t}" for t in type_categories]

        X = []
        y = []

        for entry in entries:
            row = []

            # numeric values (None -> 0.0; better: skip/impute, see notes)
            for f in numeric_features():
                value = getattr(entry, f)

                row.append(float(value) if not math.isnan(value) else 0.0)

            # one-hot for property type
            for t in type_categories:
                row.append(1.0 if entry.property_type == t else 0.0)

            X.append(row)
            y.append(entry.price_eur)

        self.X = numpy.array(X, dtype=float)
        self.y = numpy.array(y, dtype=float)

    def fit(self):
        X_b = numpy.c_[numpy.ones(self.X.shape[0]), self.X]

        theta, *_ = numpy.linalg.lstsq(X_b, self.y, rcond=None)

        self.theta = theta
        self.intercept = theta[0]
        self.coefficients = theta[1:]

        return theta

    def estimate_price(self, property_input: PropertyInput) -> float:
        if self.theta is None:
            raise RuntimeError("Call fit() before estimate_price()")

        row = []

        # numeric values, same order as training
        for f in numeric_features():
            value = getattr(property_input, f)
            row.append(float(value) if value is not None else 0.0)

        # one-hot the property type against the SAME categories used in fit
        # self.feature_names holds the trained layout, e.g. ["...", "type_House", "type_Villa"]
        for name in self.feature_names:
            if name.startswith("type_"):
                category = name[len("type_"):]  # "type_House" -> "House"
                row.append(1.0 if property_input.property_type == category else 0.0)

        # prepend the intercept's 1, then multiply by theta
        x = numpy.array([1.0] + row)
        return float(x @ self.theta)
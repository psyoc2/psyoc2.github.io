import pandas as pd

class SentimentAnalyzer:
    def __init__(self, dataset_path):
        """
        Initialize the SentimentAnalyzer with the dataset path.
        """
        self.dataset_path = dataset_path
        self.data = None
        self.load_dataset()

    def load_dataset(self):
        """
        Load the financial news sentiment dataset from the given path.
        """
        try:
            self.data = pd.read_csv(self.dataset_path)
            print("Dataset loaded successfully.")
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.data = None

    def get_sentiment_for_stock(self, stock_symbol):
        """
        Retrieve the average sentiment score for a given stock symbol.
        
        Args:
            stock_symbol (str): The stock ticker (e.g., "AAPL", "GOOGL").
        
        Returns:
            float: Average sentiment score for the stock.
        """
        if self.data is None:
            raise ValueError("Dataset not loaded. Cannot perform sentiment analysis.")

        # Filter rows containing the stock symbol in the "text" column
        stock_data = self.data[self.data["text"].str.contains(stock_symbol, case=False, na=False)]

        if stock_data.empty:
            print(f"No sentiment data found for {stock_symbol}.")
            return None

        # Calculate and return the average sentiment score
        avg_sentiment = stock_data["label"].mean()  # `label` is the sentiment column
        return avg_sentiment

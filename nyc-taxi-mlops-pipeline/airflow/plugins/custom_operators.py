from airflow.models.baseoperator import BaseOperator

class PrintOperator(BaseOperator):
    def __init__(self, message: str, **kwargs):
        super().__init__(**kwargs)
        self.message = message

    def execute(self, context):
        print(self.message)

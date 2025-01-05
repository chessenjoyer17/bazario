import logging

from bazario_app.application.ports.transaction import Transaction


class MockTransaction(Transaction):
    def commit(self) -> None:
        logging.info("Transaction committed")

    def rollback(self) -> None:
        logging.info("Transaction rolled back")

import lightning as L
import torch
from transformers import BertForSequenceClassification, BertTokenizer

from data.dataset import TextClassificationData


class LitTextClassification(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = BertForSequenceClassification.from_pretrained(
            "bert-base-uncased"
        ).train()

    def training_step(self, batch):
        output = self.model(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            labels=batch["label"],
        )
        self.log("train_loss", output.loss)
        return output.loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.model.parameters(), lr=1e-5)


if __name__ == "__main__":
    model = LitTextClassification()
    data = TextClassificationData()
    trainer = L.Trainer(max_epochs=3)
    trainer.fit(model, data)

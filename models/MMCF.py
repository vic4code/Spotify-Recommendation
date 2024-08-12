import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from transformers import AutoModel, AutoTokenizer


class DAE(pl.LightningModule):
    def __init__(self, conf, embedding_model_name="mteb/sentence-transformers"):
        super(DAE, self).__init__()

        self.n_input = conf.n_input
        self.n_hidden = conf.hidden
        self.learning_rate = conf.lr
        self.reg_lambda = conf.reg_lambda
        self.keep_prob = conf.keep_prob
        self.input_keep_prob = conf.input_keep_prob

        # Load pretrained MTEB embedding model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
        self.embedding_model = AutoModel.from_pretrained(embedding_model_name)

        # Define the layers for main autoencoder
        self.encoder_layer = nn.Linear(
            self.n_input + self.embedding_model.config.hidden_size, self.n_hidden
        )
        self.decoder_layer = nn.Linear(
            self.n_hidden, self.n_input + self.embedding_model.config.hidden_size
        )

        # Define separate layers for title embedding autoencoder
        self.title_encoder_layer = nn.Linear(
            self.embedding_model.config.hidden_size, self.n_hidden
        )
        self.title_decoder_layer = nn.Linear(
            self.n_hidden, self.embedding_model.config.hidden_size
        )

        # Initialize weights
        self.init_weights()

    def init_weights(self):
        nn.init.xavier_uniform_(self.encoder_layer.weight)
        nn.init.xavier_uniform_(self.title_encoder_layer.weight)
        if hasattr(self.decoder_layer, "weight"):
            self.decoder_layer.weight.data = self.encoder_layer.weight.data.T
        if hasattr(self.title_decoder_layer, "weight"):
            self.title_decoder_layer.weight.data = (
                self.title_encoder_layer.weight.data.T
            )

    def title_encoder(self, x):
        encoded = torch.sigmoid(self.title_encoder_layer(x))
        return F.dropout(encoded, p=self.keep_prob, training=self.training)

    def title_decoder(self, x):
        decoded = torch.sigmoid(self.title_decoder_layer(x))
        return decoded

    def encoder(self, x):
        encoded = torch.sigmoid(self.encoder_layer(x))
        return F.dropout(encoded, p=self.keep_prob, training=self.training)

    def decoder(self, x):
        decoded = torch.sigmoid(self.decoder_layer(x))
        return decoded

    def l2_loss(self):
        l2 = (
            torch.sum(self.encoder_layer.weight**2)
            + torch.sum(self.decoder_layer.weight**2)
            + torch.sum(self.encoder_layer.bias**2)
            + torch.sum(self.decoder_layer.bias**2)
            + torch.sum(self.title_encoder_layer.weight**2)
            + torch.sum(self.title_decoder_layer.weight**2)
            + torch.sum(self.title_encoder_layer.bias**2)
            + torch.sum(self.title_decoder_layer.bias**2)
        )
        return l2

    def forward(self, trk_positions, art_positions, titles):
        # Convert titles to embeddings
        title_embeddings = self.get_title_embeddings(titles)

        # Process title embeddings through its own autoencoder
        title_encoded = self.title_encoder(title_embeddings)
        title_decoded = self.title_decoder(title_encoded)

        # Concatenate title embeddings with other features
        combined_input = torch.cat([trk_positions, art_positions, title_decoded], dim=1)

        # Autoencoder process for combined features
        encoded = self.encoder(combined_input)
        decoded = self.decoder(encoded)
        return decoded

    def get_title_embeddings(self, titles):
        # Tokenize titles and convert to embeddings
        inputs = self.tokenizer(
            titles, return_tensors="pt", padding=True, truncation=True, max_length=128
        )
        outputs = self.embedding_model(**inputs)
        embeddings = outputs.last_hidden_state.mean(
            dim=1
        )  # Mean pooling of token embeddings
        return embeddings

    def training_step(self, batch, batch_idx):
        trk_positions, art_positions, y_positions, titles, trk_val, art_val = batch

        # Forward pass
        y_pred = self(trk_positions, art_positions, titles)

        # Loss calculation
        l2 = self.l2_loss()
        loss = torch.mean(
            -torch.sum(
                y_positions * torch.log(y_pred + 1e-10)
                + 0.55 * (1 - y_positions) * torch.log(1 - y_pred + 1e-10),
                dim=1,
            )
        )
        loss += self.reg_lambda * l2

        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer

    def save_model(self, path):
        torch.save(self.state_dict(), path)

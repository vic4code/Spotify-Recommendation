import json

import lightning as L
import numpy as np
import torch
from datasets import load_dataset
from torch.utils.data import DataLoader, Dataset, random_split
from transformers import BertTokenizer


class MPDDataset(Dataset):
    def __init__(self, data_dir, filename, batch_size):
        with open(data_dir + "/" + filename) as data_file:
            data_tr = json.load(data_file)
        self.num_tracks = len(data_tr["track_uri2id"])
        self.num_items = self.num_tracks + len(data_tr["artist_uri2id"])
        self.max_title_len = data_tr["max_title_len"]
        self.num_char = data_tr["num_char"]
        self.playlists = data_tr["playlists"]
        self.class_divpnt = data_tr["class_divpnt"]

        del data_tr
        self.batch_size = batch_size
        self.train_idx = 0

    def __len__(self):
        return len(self.playlists)

    def __getitem__(self, idx):
        train_trk, train_art, train_title = self.playlists[idx]
        trks = torch.tensor(train_trk).unsqueeze(1)
        playlist_trk = torch.full_like(trks, fill_value=idx, dtype=torch.int)
        trk_positions = torch.cat((playlist_trk, trks), dim=1)

        arts = torch.tensor(train_art).unsqueeze(1)
        playlist_art = torch.full_like(arts, fill_value=idx, dtype=torch.int)
        art_positions = torch.cat((playlist_art, arts), dim=1)

        return trk_positions, art_positions, train_title

    def collate_fn(self, batch):
        trk_positions = [item[0] for item in batch]
        art_positions = [item[1] for item in batch]
        titles = [item[2] for item in batch]

        # Concatenate and convert to torch tensor
        trk_positions = torch.cat(trk_positions)
        art_positions = torch.cat(art_positions)
        y_positions = torch.cat((trk_positions, art_positions), dim=0)
        trk_val = torch.ones(len(trk_positions), dtype=torch.float32)
        art_val = torch.ones(len(art_positions), dtype=torch.float32)

        return trk_positions, art_positions, y_positions, titles, trk_val, art_val


class MPDDataModule(L.LightningDataModule):
    def __init__(
        self,
        train_data_dir,
        train_filename,
        test_data_dir,
        test_filename,
        batch_size,
        num_workers=4,
    ):
        super().__init__()
        self.train_data_dir = train_data_dir
        self.train_filename = train_filename
        self.test_data_dir = test_data_dir
        self.test_filename = test_filename
        self.batch_size = batch_size
        self.num_workers = num_workers

    def setup(self, stage=None):
        # Set up the datasets for different stages (train, val, test)
        if stage == "fit" or stage is None:
            self.train_dataset = MPDDataset(
                self.train_data_dir, self.train_filename, self.batch_size
            )

        if stage == "test" or stage is None:
            self.test_dataset = MPDDataset(
                self.test_data_dir, self.test_filename, self.batch_size
            )

    def train_dataloader(self):
        # Return DataLoader for the training dataset
        return torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            collate_fn=self.train_dataset.collate_fn,
            shuffle=True,
            num_workers=self.num_workers,
        )

    def test_dataloader(self):
        # Return DataLoader for the test dataset
        return torch.utils.data.DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            collate_fn=self.test_dataset.collate_fn,
            shuffle=False,
            num_workers=self.num_workers,
        )


if __name__ == "__main__":

    # Initialize the Dataset
    dataset = MPDDataset(
        data_dir="./data/modeling", filename="train.json", batch_size=2
    )

    # Initialize the DataLoader
    dataloader = DataLoader(
        dataset, batch_size=2, collate_fn=dataset.collate_fn, shuffle=True
    )

    # Iterate over the data using the DataLoader
    for batch in dataloader:
        trk_positions, art_positions, y_positions, titles, trk_val, art_val = batch
        # Process each batch of data or pass it to the model

        breakpoint()

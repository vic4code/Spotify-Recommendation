import lightning as L
import torch
import yaml

from models.MMCF import DAE
from utils.dataset import MPDDataModule


def main(args):

    yaml_file = args.config_file
    with open(yaml_file, "r") as f:
        logger.info(f"Loading the config file in {os.path.abspath(f.name)}...")
        config = yaml.load(f, Loader=yaml.Loader)

    model = DAE()
    data = MPDDataModule()
    trainer = L.Trainer(max_epochs=3)
    trainer.fit(model, data)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--config_file", default="configs/config.yaml")
    args = parser.parse_args()

    main(args)

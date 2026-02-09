from common.transform import transform_to_iceberg
from steam.model import SteamGame

transform_to_iceberg(
    SteamGame, "warehouse/raw/steam_data", "bronze.test4", ["steam_appid"]
)

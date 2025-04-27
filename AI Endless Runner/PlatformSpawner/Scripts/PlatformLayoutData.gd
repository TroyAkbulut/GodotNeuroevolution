extends TileMap
class_name PlatformData

@export var tileWidth : int
@export var pixelWidthPerTile : int

func GetTotalPixelWidth() -> int:
	return tileWidth * pixelWidthPerTile

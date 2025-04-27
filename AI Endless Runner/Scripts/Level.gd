class_name Level
extends Node

@export var levelID : int
@export var startNode : Node2D

var levelData : LevelData

func _ready():
	levelData = LevelManager.GetLevelData(self.levelID)

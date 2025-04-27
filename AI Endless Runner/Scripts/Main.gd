extends Node

@export var levels : Array[LevelData]

@onready var mainScene = $MainScene


# Called when the node enters the scene tree for the first time.
func _ready():
	LevelManager.mainScene = self.mainScene
	LevelManager.levels = self.levels
	LevelManager.LoadLevel(1)

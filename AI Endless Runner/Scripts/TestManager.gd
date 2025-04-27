extends Node

@export var platformTester : Node
@export var playerTester : Node

func _physics_process(delta):
	if not platformTester.is_physics_processing() and not playerTester.is_physics_processing():
		LevelManager.LoadLevel(1)

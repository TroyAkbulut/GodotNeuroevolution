extends Label

@export var platformManager : Node2D

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta):
	text = "%10.3f" % platformManager.speed

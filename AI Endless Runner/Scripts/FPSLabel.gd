extends Label

func _physics_process(delta):
	text = "FPS: {}".format([Engine.get_frames_per_second()], "{}")

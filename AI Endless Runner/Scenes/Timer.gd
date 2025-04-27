extends Timer

var frameHistory: Array[int] = []

func _on_timeout():
	#frameHistory.append(int(Engine.get_frames_per_second()))
	if len(frameHistory) == 100:
		print(frameHistory)

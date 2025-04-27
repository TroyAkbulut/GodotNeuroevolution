extends CharacterBody2D
class_name Player

@onready var sprite : AnimatedSprite2D = $AnimatedSprite2D
var animationToPlay = "idle"

var playerManager : PlayerManager

const SPEED = 300.0
const JUMP_VELOCITY = -400.0

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var playerID : int = -1
var alive : bool = true
var finalScore: float = 0

func _physics_process(delta):
	# Add the gravity.
	if not is_on_floor():
		velocity.y += (gravity + playerManager.platformManager.speed*60*(gravity/abs(JUMP_VELOCITY))) * delta 
		animationToPlay = "jump"
		
	position.x -= playerManager.platformManager.speed
	sprite.play(animationToPlay)

func Left():
	sprite.set_flip_h(true)
	animationToPlay = "run"
	velocity.x = -1 * (SPEED + playerManager.platformManager.speed*60)

func Right():
	sprite.set_flip_h(false)
	animationToPlay = "run"
	velocity.x = SPEED + playerManager.platformManager.speed*60
	
func Jump():
	if is_on_floor():
		animationToPlay = "jump"
		velocity.y = JUMP_VELOCITY - playerManager.platformManager.speed*60

func OnDeath():
	sprite.stop()
	alive = false
	finalScore = playerManager.platformManager.speed
	self.set_physics_process(false)
